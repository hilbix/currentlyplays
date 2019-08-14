#!/usr/bin/env python3

import sys

import json
import codecs
import urllib
import itertools

import logging

logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.DEBUG)

logging	= logging.getLogger('spotify')

def log(*args, **kw):
	logging.info(*args, **kw)

class OopsException(Exception):
	def throw(self):
		raise self

def OOPS(s):
	OopsException(s).throw()

def prepend(s, iter):
	for a in iter:
		yield s+str(a)

utf8reader	= codecs.getreader('utf-8')

class MissingValueException(Exception):
	def __init__(self, id, help):
		super().__init('missing argument: '+id)
		self.id		= id
		self.help	= help

class Arg(object):
	def __init__(self, name, help, default=None):
		self.name	= name
		self.help	= help
		self.value	= default

	def set(self, val):
		self.value	= val

	def get(self):
		if self.value is None:	raise MissingValueException(self.id, self.help)
		return self.value

class ArgumentException(Exception):
	pass

class MalformedArgumentException(ArgumentException):
	def __init__(self, message):
		super().__init__(message)

class UnknownArgumentException(ArgumentException):
	def __init__(self, id):
		super().__init__('unknown argument: '+id)

class Spotify(object):
	setup		= Arg('setup', 'Setup file', '~/.spotify.json')

	auth_url	= Arg('auth', 'URL used for authentication; use {id}, {uri} and {nonce}', 'https://accounts.spotify.com/authorize?response_type=code&scope=user-read-currently-playing&client_id={id}&redirect_uri=(uri)&state={nonce}')
	token_url	= Arg('token', 'POST-URL to get tokens', 'https://accounts.spotify.com/api/token')
	validate_nonce	= Arg('nonce', 'Use nonce?', 1)

	client_id	= Arg('id', 'Client ID from https://developer.spotify.com/my-applications/')
	client_secret	= Arg('key', 'Client Secret from https://developer.spotify.com/my-applications/')
	redirect_uri	= Arg('uri', 'Redirect URI from https://developer.spotify.com/my-applications/')

	def allargs(self):
		for a in dir(self):
			b	= getattr(self, a)
			if isinstance(b, Arg):
				yield b

	def __init__(self):
		self.__allargs__ = { x.name:x for x in self.allargs() }

	def usage(self):
		for a in self.__allargs__.values():
			yield "{}={}".format(a.name, a.value)
			yield "\t{}".format(a.help)

	def arg(self, s):
		"str looks like arg=value, sets Arg to given value"

		try:
			k,v = s.split('=', 1)
		except ValueError:
			raise MalformedArgumentException("Arguments must have the form key=value")

		for a in self.allargs():
			if a.name == k:
				a.set(v)
				return

		raise UnknownArgumentException(k)

	def args(self, a):
		for arg in a:
			self.arg(arg)

	def args_or_usage(self, a):
		try:
			self.args(a)
		except ArgumentException as e:
			yield '\n'.join(itertools.chain(['Exception: '+str(e),'', "List of arguments:"], prepend('\t', self.usage())))

	def next(self):
		while True:
			try:
				self.init()
			except MissingValueException as e:
				yield Ask(e.id, e.help)

	def _get(self, rest, parm={}, retry=0):
		url	= self.auth_url.get().format(parm)
		OOPS(url)
		for _ in range(retry+1):
			try:
				log("request {}", url)
				req	= urllib.request.Request(url)
				req.add_header('Authorization', 'Bearer ' + self.__key)
				res	= urllib.request.urlopen(req)
				log("got {}", len(res))
				return json.load(utf8reader(res))

			except Exception as err:
				log('URL failed: {} ({})'.format(url, err))
				time.sleep(2)
		OOPS(url)

def main(*args):
	api	= Spotify()
	#api.arg('setup=~/.spotify.json')
	yield from api.args_or_usage(args)
	for act in api.next():
		log(act)

if __name__ == '__main__':
	for usage in main(*sys.argv[1:]):
		print(usage, file=sys.stderr)
		sys.exit(23)

