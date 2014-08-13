#coding=utf-8
import sys, os
import subprocess
import random
import urllib2, json
import Irc, Logger, Tracking
import time
import HTMLParser


# commands
commands = {}

lreq = None

def balance(req,_):
    """
    admin"""
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

def active(req,_):
    """active users"""
    req.reply('Active users: ' + str(len(Tracking.activeusrs[req.target])))
commands['active'] = active

lastsoak = 0

def soak(req,arg):
    """
    admin"""
    #try:
    global lastsoak
    if '!' in req.source:
        req.source = req.nick
    activeu = []
    for d in Tracking.activeusrs[req.target].keys():
        i = d.split('!',1)[0]
        if i in Tracking.registered:
            if Tracking.registered[i] and i != req.source:
                activeu.append(i)
    val = int(arg[0])/len(activeu)
    if val < 2:            #minimum
        req.serv.send('PRIVMSG','Doger','!tip ' + req.source + ' ' + str(int(arg[0])))
        req.say('Returning tip - not enough to go around')
        return
    if lastsoak + 10 > time.time():
        req.serv.send('PRIVMSG','Doger','!tip ' + req.source + ' ' + str(int(arg[0])))
        req.say('Returning tip - trying not to flood Doger')
        return
    req.say(req.source + ' is soaking ' + str(len(activeu)) + ' shibes with Ɖ' + str(val) + ': ' + ','.join(activeu))
    lastsoak = time.time()
    while activeu != []:
        req.serv.send('PRIVMSG','Doger','mtip ' + (' ' + str(val) + ' ').join(activeu[:14]) + ' ' + str(val))
        time.sleep(2)
        activeu = activeu[14:]
    #except:
     #   raise Exception('not enough to go around')
commands['soak'] = soak

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
