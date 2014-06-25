# coding=utf8
import traceback, sys, re, time

import Irc, Commands

hooks = {}

def end_of_motd(serv, *_):
	for channel in serv.autojoin:
		serv.send("JOIN", channel)
hooks["376"] = end_of_motd

def ping(serv, *_):
	serv.send("PONG")
hooks["PING"] = ping

def whois_reply(serv,source,target,text,*_):
	Commands.Tracking.who_rep(text)
hooks['330'] = whois_reply

class Request(object):
	def __init__(self, serv, target, source):
		self.serv = serv
		self.target = target
		self.source = source
		self.nick = Irc.get_nickname(source)

	def privmsg(self, targ, text):
		while len(text) > 350:
			self.say(text[:349].replace('\n',' '))
			text = text[350:]
		self.serv.send("PRIVMSG", targ, text)

	def reply(self, text):
		self.privmsg(self.target, self.nick + ": " + text)

	def reply_private(self, text):
		self.privmsg(self.nick, self.nick + ": " + text)

	def say(self, text):
		self.privmsg(self.target, text)

	def me(self, text):
		self.serv.send('PRIVMSG',self.target,'\x01ACTION '+text+'\x01')

def message(serv, source, target, text):
	host = Irc.get_host(source)
	Commands.Tracking.activity(source,target,serv)
	'''if target == serv.nick and source.split('!',1)[0] == 'Doger' and 'has tipped you' in text:
		try:
			req = Request(serv, target, source)
			val = int(text.split('you ',1)[1][2:].split(' ',1)[0])
			req.say('tipped ' + str(val))
			#Commands.soak(req,val)
		except:
			print 'soaker error' '''
	if Commands.lreq and target == serv.nick and source.split('!',1)[0] == 'Doger':
		Commands.balancerepl(text)
	if text[0] == '!' or target == serv.nick:
		if serv.is_ignored(host):
			print(serv.nick + ": (ignored) <" + Irc.get_nickname(source) + "> " + text)
			return
		print(serv.nick + ": <" + Irc.get_nickname(source) + "> " + text)
		t = time.time()
		score = serv.flood_score.get(host, (t, 0))
		score = max(score[1] + score[0] - t, 0) + 4
		if score > 40 and not serv.is_admin(source):
			serv.ignore(host, 240)
			serv.send("PRIVMSG", Irc.get_nickname(source), "You're sending commands too quickly. Your host is ignored for 240 seconds")
			return
		serv.flood_score[host] = (t, score)
		if text[0] == '!':
			text = text[1:]
		src = Irc.get_nickname(source)
		if target == serv.nick:
			reply = src
		else:
			reply = target
		if text.find(" ") == -1:
			command = text
			args = []
		else:
			command, args = text.split(" ", 1)
			args = args.split(" ")
		if command[0] != '_':
			cmd = Commands.commands.get(command.lower(), None)
			if not cmd.__doc__ or cmd.__doc__.find("admin") == -1 or serv.is_admin(source):
				if cmd:
					req = Request(serv, reply, source)
					try:
						ret = cmd(req, args)
					except Exception as e:
						type, value, tb = sys.exc_info()
						traceback.print_tb(tb)
						req.reply(repr(e))
hooks["PRIVMSG"] = message
