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

from libs import kodi

@kodi.register('main')
def main():
	show_about()
	kodi.add_menu_item({'mode': 'search_menu', 'type': "username", 'title': "Search by GitHub Username"}, {'title': "Search by GitHub Username"}, icon='username.png')
	kodi.add_menu_item({'mode': 'search_menu', 'type': "repository", 'title': "Search by GitHub Repository Title"}, {'title': "Search by GitHub Repository Title"}, icon='repository.png')
	kodi.add_menu_item({'mode': 'search_menu', 'type': "addonid",'title': "Search by Addon ID"}, {'title': "Search by Addon ID"}, icon='addonid.png')
	kodi.add_menu_item({'mode': 'update_addons'}, {'title': "Check for Updates"}, icon='update.png', visible=kodi.get_setting('enable_updates') == 'true')
	kodi.add_menu_item({'mode': 'addonuri'}, {'title': "GitHub Addons List"}, icon='about.png')
	kodi.add_menu_item({'mode': 'users'}, {'title': "GitHub Username List"}, icon='about.png')
	kodi.add_menu_item({'mode': 'about'}, {'title': "About GitHub Installer"}, icon='about.png')
	kodi.add_menu_item({'mode': 'addon_settings'}, {'title': "Tools and Settings"}, icon='settings.png')
	kodi.eod()
		
	
@kodi.register('search_menu')
def search_menu():
	from libs.database import DB
	kodi.add_menu_item({'mode': 'void'}, {'title': "[COLOR darkorange]%s[/COLOR]" % kodi.arg('title')}, icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': kodi.arg('type')}, {'title': "*** New Search ***"}, icon='null')
	results = DB.query_assoc("SELECT search_id, query FROM search_history WHERE search_type=? ORDER BY ts DESC LIMIT 10", [kodi.arg('type')], silent=True)
	if results is not None:
		for result in results:
			menu = kodi.ContextMenu()
			menu.add('Delete from search history', {"mode": "history_delete", "id": result['search_id']})
			kodi.add_menu_item({'mode': 'search', 'type': kodi.arg('type'), 'query': result['query']}, {'title': result['query']}, menu=menu, icon='null')
	kodi.eod()

@kodi.register('addonuri')
def addonuri():
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'covenantkodi'}, {'title': '[COLOR darkorange]Covenant[/COLOR] - by covenantkodi'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'Iceballs'}, {'title': '[COLOR darkorange]IceFilms[/COLOR] - by Iceballs'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'kodibae'}, {'title': '[COLOR darkorange]Exodus[/COLOR] - by kodibae'},  icon='null')	
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'OpenELEQ'}, {'title': '[COLOR darkorange]Elysium[/COLOR] - by OpenELEQ'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'teverz'}, {'title': '[COLOR darkorange]Placenta & Neptune[/COLOR] - by teverz'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'gaiaorigin'}, {'title': '[COLOR darkorange]Gaia[/COLOR] - by gaiaorigin'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'nixgates'}, {'title': '[COLOR darkorange]Incursion[/COLOR] - by nixgates'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'biglad'}, {'title': '[COLOR darkorange]SportsDevil[/COLOR] - by biglad'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'midraal'}, {'title': '[COLOR darkorange]Bob[/COLOR] - by midraal'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'trailerpark'}, {'title': '[COLOR darkorange]Bubbles[/COLOR] - by trailerpark'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'CypherMediaGIT'}, {'title': '[COLOR darkorange]Rebirth[/COLOR] - by CypherMediaGIT'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'xngsrs'}, {'title': '[COLOR darkorange]Sarsaila Repo[/COLOR] (RO)'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'addonid', 'query': 'plugin.video.streams'}, {'title': '[COLOR darkorange]Streams[/COLOR] - by moromete (RO)'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'addonid', 'query': 'plugin.video.digi-online'}, {'title': '[COLOR darkorange]Digi Online[/COLOR] - by dexterke (RO)'},  icon='null')
	kodi.eod()
	
@kodi.register('users')
def users():
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'iwannabelikemike'}, {'title': 'iwannabelikemike'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'teverz'}, {'title': 'teverz'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'biglad'}, {'title': 'biglad'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'mullafabz'}, {'title': 'mullafabz'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'alkiber'}, {'title': 'alkiber'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'spinztv'}, {'title': 'spinztv'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'mhancoc7'}, {'title': 'mhancoc7'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'kodibae'}, {'title': 'kodibae'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'tvaddonsco'}, {'title': 'tvaddonsco'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'redhood36'}, {'title': 'redhood36'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'nemesis668'}, {'title': 'nemesis668'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'jsergio123'}, {'title': 'jsergio123'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'Andorth'}, {'title': 'Andorth'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'Dev-kong'}, {'title': 'Dev-kong'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'midraal'}, {'title': 'midraal'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'TheKnifeRepo'}, {'title': 'TheKnifeRepo'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'rvermaat'}, {'title': 'rvermaat'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'blackstar3000'}, {'title': 'blackstar3000'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'crazyxbmc'}, {'title': 'crazyxbmc'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'nixgates'}, {'title': 'nixgates'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'goliath-evolve'}, {'title': 'goliath-evolve'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'MrBlamo420'}, {'title': 'MrBlamo420'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'kayaaron13'}, {'title': 'kayaaron13'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'Shepo6'}, {'title': 'Shepo6'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'LReylist'}, {'title': 'LReylist'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'tkey3'}, {'title': 'tkey3'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'tony5856'}, {'title': 'tony5856'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'familyrep'}, {'title': 'familyrep'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'ttmediav1'}, {'title': 'ttmediav1'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'BludhavenGrayson'}, {'title': 'BludhavenGrayson'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'intrcomp'}, {'title': 'intrcomp'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'TheBeautifulMonkey'}, {'title': 'TheBeautifulMonkey'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'teamrepomonster'}, {'title': 'teamrepomonster'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'kodil'}, {'title': 'kodil'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'GandelfsRepo'}, {'title': 'GandelfsRepo'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'fluxustv'}, {'title': 'fluxustv'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'illuminatitemple'}, {'title': 'illuminatitemple'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'elgatito'}, {'title': 'elgatito'},  icon='null')
	kodi.add_menu_item({'mode': 'search', 'type': 'username', 'query': 'koying'}, {'title': 'koying'},  icon='null')
	kodi.eod()
	
@kodi.register('search')
def search():
	from libs.database import DB
	from libs import github_api
	from libs.github_api import re_repository
	q = kodi.arg('query') if kodi.arg('query') else kodi.dialog_input('Search GitHub')
	if q in [None, False, '']: return False
	DB.execute('INSERT INTO search_history(search_type, query) VALUES(?,?)', [kodi.arg('type'), q])
	DB.commit()
	if kodi.arg('type') == 'username':
		rtype = 'api'
		response = github_api.find_zips(q)
		if response is None: return
		for r in github_api.sort_results(response['items']):
			url = github_api.content_url % (r['repository']['full_name'], r['path'])
			menu = kodi.ContextMenu()
			if re_repository.search(r['name']):
				menu.add('Browse Repository Contents', {"mode": "browse_repository", "url": url, "file": r['name'], "full_name": "%s/%s" % (q, r['repository']['name'])})
			kodi.add_menu_item({'mode': 'github_install', "url": url, "user": q, "file": r['name'], "full_name": "%s/%s" % (q, r['repository']['name'])}, {'title': r['name']}, menu=menu, icon='null')
		kodi.eod()
	elif  kodi.arg('type') == 'repository':
		rtype = 'api'
		results = github_api.search(q, 'title')
		if results is None: return
		for i in results['items']:
			user = i['owner']['login']
			response = github_api.find_zips(user)
			if response is None: continue
			for r in github_api.sort_results(response['items']):
				url = github_api.content_url % (r['repository']['full_name'], r['path'])
				menu = kodi.ContextMenu()
				if re_repository.search(r['name']):
					menu.add('Browse Repository Contents', {"mode": "browse_repository", "url": url, "file": r['name'], "full_name": "%s/%s" % (q, r['repository']['name'])})
				kodi.add_menu_item({'mode': 'github_install', "url": url, "user": q, "file": r['name'], "full_name": "%s/%s" % (q, r['repository']['name'])}, {'title': r['name']}, menu=menu, icon='null')
		kodi.eod()
	elif  kodi.arg('type') == 'addonid':
		rtype = 'web'
		results = github_api.web_search(q)
		if results is None: return
		for r in results['items']:
			kodi.add_menu_item({'mode': 'github_install', "user": r['owner']['login'], "repo": r['name'], "rtype": rtype}, {'title': "%s/%s" % (r['owner']['login'], r['name'])}, icon='null')
		kodi.eod()
	
@kodi.register('github_install')
def github_install():
	if kodi.arg('rtype') == 'web':
		from libs import github_installer
		from libs.github_api import master_url
		full_name = "%s/%s" % (kodi.arg('user'), kodi.arg('repo'))
		c = kodi.dialog_confirm("Confirm Install", full_name, yes="Install", no="Cancel")
		if not c: return
		url = master_url % (kodi.arg('user'), kodi.arg('repo'))
		github_installer.GitHub_Installer(kodi.arg('repo'), url, full_name, kodi.vfs.join("special://home", "addons"), True)
		r = kodi.dialog_confirm(kodi.get_name(), 'Click Continue to install more addons or', 'Restart button to finalize addon installation', yes='Restart', no='Continue')
		if r:
			import sys
			import xbmc
			if sys.platform in ['linux', 'linux2', 'win32']:
				xbmc.executebuiltin('RestartApp')
			else:
				xbmc.executebuiltin('ShutDown')
	else:
		import re
		from libs import github_installer
		from libs import github_api
		c = kodi.dialog_confirm("Confirm Install", kodi.arg('file'), yes="Install", no="Cancel")
		if not c: return
		addon_id = re.sub("-[\d\.]+zip$", "", kodi.arg('file'))
		github_installer.GitHub_Installer(addon_id, kodi.arg('url'), kodi.arg('full_name'), kodi.vfs.join("special://home", "addons"))
		r = kodi.dialog_confirm(kodi.get_name(), 'Click Continue to install more addons or', 'Restart button to finalize addon installation', yes='Restart', no='Continue')
		if r:
			import sys
			import xbmc
			if sys.platform in ['linux', 'linux2', 'win32']:
				xbmc.executebuiltin('RestartApp')
			else:
				xbmc.executebuiltin('ShutDown')

@kodi.register('about')
def about():
	try:
		import xbmc
		KODI_LANGUAGE = xbmc.getLanguage()
	except:
		KODI_LANGUAGE = 'English'
	path = kodi.vfs.join(kodi.get_path(), 'resources/language/%s/github_help.txt', KODI_LANGUAGE)
	if not kodi.vfs.exists(path):
		path = kodi.vfs.join(kodi.get_path(), 'resources/language/English/github_help.txt')
	text = kodi.vfs.read_file(path)
	kodi.dialog_textbox('GitHub Browser Instructions', text)

def show_about():
	interval = int(kodi.get_setting('last_about'))
	if interval == 0:
		interval = 5
		try:
			import xbmc
			KODI_LANGUAGE = xbmc.getLanguage()
		except:
			KODI_LANGUAGE = 'English'
		path = kodi.vfs.join(kodi.get_path(), 'resources/language/%s/github_help.txt', KODI_LANGUAGE)
		if not kodi.vfs.exists(path):
			path = kodi.vfs.join(kodi.get_path(), 'resources/language/English/github_help.txt')
		text = kodi.vfs.read_file(path)
		kodi.dialog_textbox('GitHub Browser Instructions', text)
	else:
		interval -= 1	
	kodi.set_setting('last_about', interval)
			

@kodi.register('browse_repository')
def browse_repository():
	from libs import github_api
	xml = github_api.browse_repository(kodi.arg('url'))
	
	heading = "%s/%s" % (kodi.arg('full_name'), kodi.arg('file'))
	options = []
	if xml:
		for addon in xml.findAll('addon'):
			options.append("%s (%s)" % (addon['name'], addon['version']))
			
		kodi.dialog_select(heading, sorted(options))


@kodi.register('history_delete')
def history_delete():
	if not kodi.arg('id'): return
	from libs.database import DB
	DB.execute("DELETE FROM search_history WHERE search_id=?", [kodi.arg('id')])
	DB.commit()	
	kodi.refresh()

@kodi.register('update_addons')
def update_addons():
	from libs import github_installer
	quiet = True if kodi.arg('quiet') == 'quiet' else False
	if not quiet:
		c = kodi.dialog_confirm("Confirm Update", "Check for updates", yes="Update", no="Cancel")
		if not c: return
	github_installer.update_addons(quiet)
	
if __name__ == '__main__': kodi.run()
