# coding=utf8
import sys
import subprocess
import Irc, Logger

commands = {}

def ping(req, _):
	"""%ping - Pong"""
	req.reply("Pong")
commands["ping"] = ping

def fortune(req, _):
	"""output of fortune-mod"""
	req.say(subprocess.check_output("fortune"))

def convert(req,arg):
	"""cryptocoin tickers"""
	