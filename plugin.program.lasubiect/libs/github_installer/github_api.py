# -*- coding: utf-8 -*-

'''*
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
*'''

import re
import sys
import kodi
import urllib
import random
try:
	from libs import requests
	from libs import dom_parser
except:
	path = kodi.vfs.join(kodi.get_path(), "libs")
	sys.path.append(path)
	import requests
from enum import enum


class githubException(Exception):
	pass

base_url = "https://api.github.com"
content_url = "https://raw.githubusercontent.com/%s/master/%s"
page_limit = 100

SORT_ORDER = enum(REPO=0, PLUGIN=1, PROGRAM=2, SKIN=3, SERVICE=4, SCRIPT=5, OTHER=100)


def search(q, method=False):
	if method=='user':
		return call("/search/repositories", query={"per_page": page_limit, "q": "user:%s" % q})
	if method=='title':
		return call("/search/repositories", query={"per_page": page_limit, "q": "in:name+%s" % q})
	else:
		return call("/search/repositories", query={"per_page": page_limit, "q": q})

def sort_results(results):
	re_plugin = re.compile("^plugin\.", re.IGNORECASE)
	re_service = re.compile("^service\.", re.IGNORECASE)
	re_script = re.compile("^script\.", re.IGNORECASE)
	re_repository = re.compile("^repository\.", re.IGNORECASE)
	re_program = re.compile("^(program\.)|(plugin\.program)", re.IGNORECASE)
	re_skin = re.compile("^skin\.", re.IGNORECASE)
	def sort_results(name):
		index = SORT_ORDER.OTHER
		if re_program.search(name): index = SORT_ORDER.PROGRAM
		elif re_plugin.search(name): index = SORT_ORDER.PLUGIN
		elif re_repository.search(name): index = SORT_ORDER.REPO
		elif re_service.search(name): index = SORT_ORDER.SERVICE
		elif re_script.search(name): index = SORT_ORDER.SCRIPT
		return index, name

	return sorted(results, key = lambda x: sort_results(x['name']))

def web_search(q):
	from HTMLParser import HTMLParser
	class MLStripper(HTMLParser):
		def __init__(self):
			self.reset()
			self.fed = []
		def handle_data(self, d):
			self.fed.append(d)
		def get_data(self):
			return ''.join(self.fed)

	def strip_tags(html):
		s = MLStripper()
		s.feed(html)
		return s.get_data()
	base_url = "https://github.com/search"
	q = "%s extension:zip language:Python path:addon.xml language:Python" % q
	params = {"q":q, "type":"Repositories", "ref":"advsearch"}
	results = {"items": []}
	r = requests.get(base_url, params=params)
	links = dom_parser.parse_dom(r.text, 'a', {"class": "v-align-middle"})
	for link in links:
		link = strip_tags(link)
		temp = link.split("/")
		results["items"] += [{"owner": {"login": temp[0]}, "name": temp[1], "full_name": link}]
	return results

def find_xml(full_name):
	return call(content_url % (full_name, 'addon.xml'), web=True)

def find_zips(user, repo=None):
	if repo is None:
		#return call("/search/code?per_page=100&q=user:%s+filename:*.zip" % user)
		return call("/search/code", query={"per_page": page_limit, "q":"user:%s+filename:*.zip" % user})
	else:
		return call("/search/code", query={"per_page": page_limit, "q":"user:%s+repo:%s+filename:*.zip" % (user, repo)})
		#return call("/search/code?per_page=100&q=user:%s+repo:%s+filename:*.zip" % (user, repo))

def find_zip(user, addon_id):
	results = []
	#response = call("/search/code?q=user:%s+filename:%s*.zip" % (user, addon_id))
	response = call("/search/code", query={"q": "user:%s+filename:%s*.zip" % (user, addon_id)})
	if response is None: return False, False, False
	if response['total_count'] > 0:
		test = re.compile("%s-.+\.zip$" % addon_id)
		
		''' Sort results by version major, minor, point extracted by regex here '''
		
		version_regex = re.compile("-(\d+)\.(\d+)\.(\d+)\.zip$")
		def sort_results(name):
			try:
				map(int, version_regex.search(name).groups())
			except:
				return -1, -1, -1
		response['items'].sort(key=lambda k: sort_results(k['name']))
		for r in response['items']:
			if test.match(r['name']):
				url = content_url % (r['repository']['full_name'], r['path'])
				return url, r['name'], r['repository']['full_name']
	return False, False, False
			

def get_download(url):
	r = call(url, append_base=False)
	return r['download_url']

def call(uri, query=None, params=False, append_base=True, web=False):
	if web:
		r = requests.get(uri)
		if r.status_code == requests.codes.ok:
			r.encoding = 'utf-8'
			return r.text
		else:
			raise githubException("Status %s: %s" % (r.status_code, r.text))
	kodi.sleep(random.randint(50, 250)) # random delay 50-250 ms
	url = base_url + uri if append_base else uri
	if query is not None:
		query = urllib.urlencode(query)
		for r in [('%3A', ":"), ("%2B", "+")]:
			f,t = r
			query = query.replace(f,t)
		url = url + '?' + query
	if kodi.get_setting('github_key'):
		headers = {"Authorization": "token %s" % kodi.get_setting('github_key')}
	else:
		headers = {}	
	
	if params:
		r = requests.get(url, params, headers=headers)
	else:
		r = requests.get(url, headers=headers)
	if r.status_code == requests.codes.ok:
		return r.json()
	elif r.status_code == 401:
		kodi.notify("Unauthorized", "Bad credentials")
		kodi.log(r.text)
		return None
	elif r.status_code == 403:
		import time
		retry = int(r.headers['X-RateLimit-Reset']) - int(time.time())
		kodi.notify("Rate limit exceeded", "Retry in %s" % retry)
		kodi.log(r.text)
		return None
	elif r.status_code == 422:
		kodi.notify("No results found", "Review search terms")
		kodi.log(r.text)
		return None
	else:
		kodi.close_busy_dialog()
		raise githubException("Status %s: %s" % (r.status_code, r.text))
