# Embedded file name: /home/ubuntu/python-irc-framework/Commands.py
import sys, os
import subprocess
import random
import urllib2, json
import Irc, Logger, Tracking
import time


# commands
commands = {}

def help(req, arg):
    """list of commands"""
    if len(arg) > 0:
        if arg[0] == 'list':
            req.reply_private('Commands: !' + ', !'.join(commands.keys()) + '. Type !help full for documantation on these commands.')
        elif arg[0] == 'full':
            req.reply_private('Commands: ' + ''.join(('!' + nam + ': ' + cmd.__doc__ + ', ') if 'admin' not in cmd.__doc__ else '' for nam,cmd in commands.items()))
        elif arg[0] in commands.keys():
            if 'admin' not in commands.get(arg[0]).__doc__:
                req.reply('!' + arg[0] + ' : ' + commands[arg[0]].__doc__)
            else:
                req.reply('You can\'t use that command!!')
    else:
        req.reply('I am a bot created by TheDoctorisaDoge. To leave him a message: !docmsg <message> . Other help commands: !help list , !help full , !help <command>')
commands['help'] = help

def ping(req, _):
    """ping - pong"""
    #print 'test.........'
    req.reply('Pong')
commands['ping'] = ping

def fortune(req, _):
    """output of fortune-mod"""
    req.say(subprocess.check_output('fortune'))
commands['fortune'] = fortune

def address(req, arg):
    """balance of given address"""
    try:
        balance = urllib2.urlopen('http://dogechain.info/chain/Dogecoin/q/addressbalance/' + arg[0]).read()
        req.reply('Balance: ' + balance)
    except:
        req.reply('There was an error')
commands['address'] = address

def network(req, _):
    """blockchain info"""
    try:
        blocks = urllib2.urlopen('http://dogechain.info/chain/Dogecoin/q/getblockcount').read()
        diff = urllib2.urlopen('http://dogechain.info/chain/Dogecoin/q/getdifficulty').read()
        coins = urllib2.urlopen('http://dogechain.info/chain/Dogecoin/q/totalbc').read()
        progress = float(coins) / 1000000000
        req.say('Blocks: ' + blocks + ', Difficulty: ' + diff + ', Total coins mined: ' + coins + ' (' + str(progress) + '%)')
    except:
        req.reply('There was an error')
commands['network'] = network

def progress(req, _):
    """distance to the moon"""
    try:
        coins = urllib2.urlopen('http://dogechain.info/chain/Dogecoin/q/totalbc').read()
        progress = float(coins) / 1000000000
        req.say('We are ' + str(progress) + '% to the moon')
    except:
        req.reply('There was an error')
commands['progress'] = progress

def throw(req, arg):
    """throws an object"""
    itm = urllib2.urlopen("http://itvends.com/vend").read()
    if len(arg) > 0:
        req.me('throws ' + itm + ' at ' + arg[0])
    else:
        req.me('throws ' + req.nick)
commands['throw'] = throw

def rickroll(req, _):
    """rickrolls channel"""
    req.say("We're no strangers to love...")
commands['rick'] = rickroll

def ticker(req, arg):
    """ticker from coinmarketcap"""
    try:
        dat = json.loads(urllib2.urlopen('http://coinmarketcap.northpole.ro/api/' + arg[0] + '.json').read())
        req.say(dat['name'] + ' price: $' + dat['price'] + ', Market cap: ' + dat['marketCap'] + ', Volume: ' + dat['volume24'])
    except:
        req.reply('Error retreiving ticker')
commands['ticker'] = ticker

def send(req,_):
    """sends random item to moon"""
    try:
		itm = urllib2.urlopen("http://itvends.com/vend").read()
		req.me('sends '+itm+' to the MOOOOOOOON!!!')
    except:
		print "vending error"
commands['send'] = send

def lick(req,arg):
    """licks someone and report their 'taste'"""
    try:
        arg.append(req.source)
        itm = urllib2.urlopen("http://itvends.com/vend").read()
        req.me('licks ' + arg[0])
        req.say(arg[0] + ' tastes like ' + itm)
    except:
        print "vending error"
commands['lick'] = lick

def active(req,_):
    """active users"""
    req.reply('Active users: ' + str(len(Tracking.activeusrs[req.target])) + ': ' + ','.join(i.split('!',1)[0] for i in Tracking.activeusrs[req.target].keys()))
commands['active'] = active

curpuz = int(open('currentpuzz','r').read())

def puzzle(req,_):
    """shows current puzzle"""
    global curpuz
    try:
        puzzledat = json.loads(open('puzzles.txt','r').read())
        puzzleque = puzzledat[str(curpuz)]['q']
        assert puzzleque != ''
    except:
        puzzleque = 'no more puzzles. in the mean time, check out http://joezeng.com/quetzalcoatl'
    req.say('Current puzzle: ' + puzzleque + ' - !ans <answer>')
commands['puzzle'] = puzzle

def puzzlea(req,arg):
    """answer current puzzle"""
    global curpuz
    try:
        puzzledat = json.loads(open('puzzles.txt','r').read())
        puzzleans = puzzledat[str(curpuz)]['a']
    except:
        print 'puzzle error'
    if arg[0].lower() == puzzleans.lower():
        req.say('%tip ' + req.nick + ' 50 -- ' + req.nick + ' got the correct answer! Use !puzzle to get the next puzzle!')
        curpuz += 1
        cpfile = open('currentpuzz','w')
        cpfile.write(str(curpuz))
        cpfile.close()
    else:
        req.reply('Incorrect')
commands['ans'] = puzzlea

def rules(req,arg ):
    """displays a rule from the chan rules"""
    try:
        r = 'No ' + ["Illegal activities (including discussion) pursuant to Freenode's policies.", 'Scamming.', 'Impersonation.', 'Spamming and/or flooding.', 'Operating malicious bots/scripts.', 'Posting malicious links.', 'Continually purveying misinformation despite warning(s).', 'Publishing or sharing personal information of others (without permission).', "Promotion of market-manipulation or 'pump & dump' schemes.", "Unconstructive/excessive promotion of 'altcoins' (alternative coins).", 'Continual advertising/promotion despite warning(s).', 'Posting pornographic or highly inapprorpiate/explicit content.', 'Hate speech/Derogatory terms.', 'Personally attacking others.', 'Flame wars. Flaming is the act of sending messages that are deliberately hostile and insulting.', 'Continual trolling despite warning(s).', 'Excessive use of profanity, vulgarity or sexual terms despite warning(s).', 'Starting or participating in discussions to incite drama or negativity.', 'Backset moderating/"mini modding". In some cases it would be appropriate to warn users for breaking rules - e.g. when operators are afk.', 'Begging. Please take this to #dogebeg.', 'Ignoring operators. This rule acts as a guideline and will not be directly enforced with consequences.'][int(arg[0])+1]
        req.say(r)
    except:
        print 'rule error'
commands['rule'] = rules

def easy(req,_):
    """staples easy button"""
    req.say("That was easy.")
commands['easybutton'] = easy

def soak(req,arg):
    """
    admin"""
    try:
        activeu = []
        for d in Tracking.activeusrs[req.target].keys():
            i = d.split('!',1)[0]
            if i in Tracking.registered:
                if Tracking.registered[i]:
                    activeu.append(i)
        val = int(arg[0])/len(activeu)
        req.say('Now soaking ' + str(len(activeu)) + ' shibes with ' + str(val))
        req.say('%mtip ' + (' ' + str(val) + ' ').join(activeu) + ' ' + str(val))
    except:
        print 'soak error'
commands['soak'] = soak

lreq = None

def balance(req,_):
    """balance of DogeSrv"""
    global lreq
    lreq = req
    req.serv.send('PRIVMSG','Doger','balance')
commands['dsbal'] = balance

def balancerepl(msg):
    global lreq
    try:
        bal = msg.split('Your balance is ',1)[1]
        assert bal != msg
        lreq.say('My balance is ' + bal)
        lreq = None
    except:
        print 'balance error'

def eightball(req,arg):
    """8 ball"""
    req.reply(random.choice(['yes','no','maybe','somewhat likely','not likely','possibly','quite possible','very unlikely','absolutely not','ask someone else','i don\'t know','ummmmmmmmmm']))
commands['8ball'] = eightball


def poll(req,_):
    """shows current poll"""
    try:
        polldat = eval(open('polldata','r').read())
        req.say('Current poll: ' + polldat['question'] + ': ' + ','.join(polldat['valid']) + ' - !polla <answer>')
    except:
        print 'poll error'
commands['poll'] = poll

def pollans(req,arg):
    """answer a poll"""
    try:
        polldat = eval(open('polldata','r').read())
        if arg[0].lower() in polldat['valid']:
            polldat['answers'][req.nick] = arg[0].lower()
        pollfile = open('polldata','w')
        pollfile.write(repr(polldat))
        pollfile.close()
    except:
        print 'poll error'
commands['polla'] = pollans

def pollstat(req,_):
    """stats of current poll"""
    try:
        polldat = eval(open('polldata','r').read())
        stat = {}
        for i in polldat['answers'].values():
            if i not in stat:
                stat[i] = 0
            stat[i] = stat[i] + 1
        req.say(', '.join((str(a) + ': ' + str(b)) for a,b in stat.items()))
    except:
        print 'poll error'
commands['pollstat'] = pollstat
    
def pollset(req,arg):
    """
    admin"""
    try:
        opolldat = open('polldata','r').read()
        opollfile = open('pastpolls.txt','a')
        opollfile.write('\n' + opolldat)
        opollfile.close()
        polldat = {}
        polldat['question'] = ' '.join(arg[:-1])
        polldat['valid'] = eval(arg[-1])
        polldat['answers'] = {}
        pollfile = open('polldata','w')
        pollfile.write(repr(polldat))
        pollfile.close()
    except:
        print 'poll error'
commands['pollset'] = pollset

def telldoc(req,arg):
    """send TheDoctorisaDoge (my creator) a message"""
    fil = open('docnotes.txt','a')
    fil.write(' '.join(arg) + '\n')
    fil.close()
    req.reply('Success')
commands['docmsg'] = telldoc

def mydoge(req,_):
    req.say('http://imgur.com/kILItcK')
commands['dog'] = mydoge


def load(req, arg):
    """
    admin"""
    for mod in arg:
        reload(sys.modules[mod])

    req.reply('Done')
commands['reload'] = load

def _exec(req, arg):
    """
    admin"""
    try:
        req.reply(repr(eval(' '.join(arg))))
    except SyntaxError:
        exec ' '.join(arg)
commands['exec'] = _exec

def die(req, arg):
    """
    admin"""
    os.system('killall python')
commands['die'] = die

def ignore(req, arg):
    """
    admin"""
    req.serv.ignore(arg[0], int(arg[1]))
commands['ignore'] = ignore