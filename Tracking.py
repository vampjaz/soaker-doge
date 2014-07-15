import time

# User activity tracking
exemptusrs = ['dogesrv','doger','dogexm','activeshibes','hardc0re','tipulator','codicai','dogetip','blasterbot','dogedicer','keksbotz','doge_soaker','dogeai']
activeusrs = {}
registered = {}

def activity(nick,chan,serv):
    snick = nick.split('!',1)[0].lower()
    if snick in exemptusrs:
        print 'exempt user'
    else:
        now = time.time()
        lastac = now - 600      # 10 minutes is activity
        if snick not in registered.keys():
            registered[snick] = False
            serv.send('WHOIS',snick)
        if chan not in activeusrs.keys():
            activeusrs[chan] = {}
        activeusrs[chan][nick] = now
        for j in activeusrs.keys():
            for i in activeusrs[j].keys():
                if activeusrs[j][i] < lastac:
                    del activeusrs[j][i]

def who_rep(nick):
    registered[nick] = True

def acct_notify(user,acct):
    registered[user.split('!')[0]] = acct!='*'