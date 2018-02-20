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
import xbmc
import kodi
import xbmcgui
import downloader
import zipfile
import github_api
import re
import shutil
from BeautifulSoup import BeautifulSoup
try:
	from libs import requests
except:
	path = kodi.vfs.join(kodi.get_path(), "libs")
	sys.path.append(path)
	import requests
from enum import enum

class installerException(Exception):
	pass

tva_user = 'tvaddonsco'

# Define source types
SOURCES = enum(DEFAULT=0, REPO=1, ZIP=2, SUPER=3, NATIVE=4)

def update_addons():
	return
	save_file = kodi.vfs.join(kodi.get_profile(), "install.log")
	if vfs.exists(save_file):
		temp = kodi.load_data(save_file, format='json', compress=True)
	else:
		temp = {}
	kodi.open_busy_dialog()
	v = kodi.get_kodi_version()
	from sqlite3 import dbapi2
	dbf = kodi.vfs.join("special://profile/Database", "Addons20.db")
	if v >= 17:
		dbf = kodi.vfs.join("special://profile/Database", "Addons27.db")
		SQL = """SELECT installed.addonID, addons.version from installed 
				 JOIN addons on installed.addonID=addons.addonID
				 WHERE origin = '' and enabled=1"""
		with dbapi2.connect(dbf) as dbh:
			dbc = dbh.cursor()
			dbc.execute(SQL)
			for a in dbc.fetchall():
				if a[0] in temp:
					kodi.log(temp[a[0]])
	else:
		dbf = kodi.vfs.join("special://profile/Database", "Addons20.db")

	kodi.close_busy_dialog()
	
	kodi.notify("Update complete", 'Update complete')

class GitHub_Installer():
	required_addons = []
	unmet_addons = []
	met_addons = []
	available_addons = []
	sources = {}
	install_error = False
	source_table = {}
	completed = []
	def __init__(self, addon_id, url, full_name, destination, master=False):
		kodi.open_busy_dialog()
		v = kodi.get_kodi_version()
		
		# Grab a list of KNOWN addons from the database. Unfortunately Jarvis requires direct database access for the installed flag
		if v >= 17:
			response = kodi.kodi_json_request("Addons.GetAddons", { "installed": False, "properties": ["path", "dependencies"]})
			for a in response['result']['addons']:
				self.available_addons += [a['addonid']]
				self.source_table[a['addonid']] = a['path']
		else:
			from sqlite3 import dbapi2
			dbf = kodi.vfs.join("special://profile/Database", "Addons20.db")
			with dbapi2.connect(dbf) as dbh:
				dbc = dbh.cursor()
				dbc.execute("SELECT addon.addonID, broken.addonID is Null AS enabled, addon.path FROM addon LEFT JOIN broken on addon.addonID=broken.addonID WHERE enabled=1")
				for a in dbc.fetchall():
					self.available_addons += [a[0]]
					self.source_table[a[0]] = a[2]
			dbh.close()
		self._addon_id = addon_id
		self._url = url
		self._full_name = full_name
		self._user, self.repo = full_name.split("/")
		self._master = master
		self._destination = destination
		
		# Add the final addon target to the sources list with type of zip
		# Initiate install routine
		self.sources[addon_id] = {"type": SOURCES.ZIP, "url": url}
		self.install_addon(addon_id, url, full_name, master)
		
		# Enable installed addons
		for addon_id in self.completed:
			self.enable_addon(addon_id)
		kodi.close_busy_dialog()
		if self.install_error:
			kodi.notify("Install failed", self._addon_id)
		else:		
			kodi.notify("Install complete", self._addon_id)

	def build_dependency_list(self, addon_id, url, full_name, master):
		user, repo = full_name.split("/")
		if master:
			kodi.log('Finding dependencies from master')
			self.sources[addon_id] = {"type": SOURCES.REPO, "url": url}
			xml_str = github_api.find_xml(full_name)
			xml = BeautifulSoup(xml_str)
		else:
			kodi.log('Finding dependencies from zip')
			downloader.download(url, addon_id + ".zip", self._destination, True)
			src_file = kodi.vfs.join("special://home/addons", addon_id)
			kodi.vfs.join(src_file, "addon.xml")
			xml = kodi.vfs.read_file(kodi.vfs.join(src_file, "addon.xml"), soup=True)

		for dep in xml.findAll('import'):
			test = dep['addon']
			try:
				if dep['optional'].lower() == 'true': continue
			except:
				pass
			if test in ['xbmc.python', 'xbmc.gui'] or kodi.get_condition_visiblity('System.HasAddon(%s)' % test) == 1: continue
			self.required_addons += [test]
			if test not in self.available_addons: 
				self.unmet_addons += [test]
			else:
				self.sources[test] = {"type": SOURCES.DEFAULT, "url": self.source_table[test]}
				kodi.log("%s dependency met in %s" % (test, self.source_table[test]))
		
		def user_resolver(user, unmet):
			dep_url, dep_filename, dep_full_name = github_api.find_zip(user, unmet)
			if dep_url:
				kodi.log("%s found in %s repo" % (unmet, user))
				self.met_addons.append(unmet)
				self.sources[unmet] = {"type": SOURCES.ZIP, "url": dep_url}
				kodi.log("%s dependency met in %s" % (unmet, dep_url))
				return True
			return False
		
		def	github_resolver(unmet):
			results = github_api.web_search(unmet)
			c = kodi.dialog_select("GitHub Search Results for %s" % unmet, [r['full_name'] for r in results['items']])
			if c is not False:
				dep = results['items'][c]
				dep_url = url = "https://github.com/%s/archive/master.zip" % (dep['full_name'])
				self.met_addons.append(unmet)
				dep_filename = "%s.zip" % unmet
				self.sources[unmet] = {"type": SOURCES.REPO, "url": dep_url}
				kodi.log("%s dependency met in %s" % (unmet, dep_url))
				self.install_addon(unmet, dep_url, dep['full_name'], master=True)
				
				return True
			return False
		
		def sr_resolver(unmet):
			url = 'https://cdimage.debian.org/mirror/addons.superrepo.org/v7/addons/%s' % unmet
			response = requests.get(url)
			if response.status_code == 200:
				for match in re.finditer('href="([^"]+)"', response.text):
					if match.group(1).endswith('zip'):
						f = match.group(1)
						dep_url = url + '/' + f
						self.met_addons.append(unmet)
						self.sources[unmet] = {"type": SOURCES.ZIP, "url": dep_url}
						kodi.log("%s dependency met in %s" % (unmet, dep_url))
						return True
			return False		
		
		
		for unmet in self.unmet_addons:
			# Now attempt to locate dependencies from available sources
			# The addons that can be found in any enabled repos will be installed at the end.
			
			# check if this exists in users root repo
			if user_resolver(user, unmet): continue
			
			# check if this exists in tva root repo
			if user_resolver(tva_user, unmet): continue
			
			# check if this exists on github
			#if github_resolver(unmet): continue
			
			# check if this exists on superrepo
			if sr_resolver(unmet): continue
			
		self.unmet_addons = list(set(self.unmet_addons) - set(self.met_addons))
		if len(self.unmet_addons):
			self.install_error = True
			kodi.close_busy_dialog()
			kodi.raise_error("", "Unmet Dependencies:", "See log or install manually", ','.join(self.unmet_addons))

	def install_addon(self, addon_id, url, full_name, master):
		self.required_addons += [addon_id]
		self.build_dependency_list(addon_id, url, full_name, master)
		self.required_addons = list(set(self.required_addons))
		self.unmet_addons = list(set(self.unmet_addons))
		sources = self.sources
		self.sources = {}
		for addon_id in sources:
			source = sources[addon_id]
			if source['type'] == SOURCES.DEFAULT:
				self.install_addon(addon_id, source['url'], self._full_name, False)
			elif source['type'] == SOURCES.NATIVE:
				kodi.xbmc.executebuiltin("XBMC.InstallAddon(%s)" % addon_id)
				i=0
				while kodi.get_condition_visiblity('System.HasAddon(%s)' % addon_id) == 0:
					if i == 30:
						kodi.raise_error("", "Unmet Dependencies:", "Install Timed Out", addon_id)
						break
						
					kodi.sleep(1000)
					i+=1
			elif source['type'] == SOURCES.ZIP:
				downloader.download(source['url'], addon_id + ".zip", self._destination, True)
			elif source['type'] == SOURCES.REPO:
				src = kodi.vfs.join("special://home/addons", addon_id +"-master") 
				dest = kodi.vfs.join("special://home/addons", addon_id)
				if kodi.vfs.exists(dest):
					if kodi.dialog_confirm("Confirm overwrite", dest):
						shutil.rmtree(dest)
					else: return
				downloader.download(source['url'], addon_id + ".zip", self._destination, True)

				shutil.move(src, dest)
			self.save_sources(sources)
			self.completed.append(addon_id)
	
	def save_sources(self, sources):
		save_file = kodi.vfs.join(kodi.get_profile(), "install.log")
		if vfs.exists(save_file):
			temp = kodi.load_data(save_file, format='json', compress=True)
		else:
			temp = {}
		for s in sources:
			temp[s] = sources[s]
		kodi.save_data(save_file, temp, format='json', compress=True)

	def enable_addon(self, addon_id):
		try:
			kodi.xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
			kodi.sleep(500)
			kodi.kodi_json_request("Addons.SetAddonEnabled", {"addonid": addon_id, "enabled": True})
		except: pass
