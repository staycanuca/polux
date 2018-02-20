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

import kodi
import time
import xbmcgui
import zipfile
try:
	from libs import requests
except:
	path = kodi.vfs.join(kodi.get_path(), "libs")
	sys.path.append(path)
	import requests

class downloaderException(Exception):
	pass

def format_speed(speed):
	if speed > 2000:
		speed = float(speed) / 1000
		speed = "Speed %.2f MB/s" % speed
	else:
		speed = "Speed %.0f KB/s" % speed
	return speed	

def download(url, filename, destination, unzip=False):
	r = requests.get(url, stream=True)
	kodi.log("Download: %s" % url)
	if r.status_code == requests.codes.ok:
		temp_file = kodi.vfs.join(kodi.get_profile(), "downloads")
		if not kodi.vfs.exists(temp_file): kodi.vfs.mkdir(temp_file, recursive=True)
		temp_file = kodi.vfs.join(temp_file, filename)
		try:
			total_bytes = int(r.headers["Content-Length"])
		except:
			total_bytes = 0
		block_size = 1000
		cached_bytes = 0
		pb = xbmcgui.DialogProgress()
		pb.create("Downloading",filename,' ', ' ')
		kodi.sleep(150)
		start = time.time()
		with open(temp_file, 'wb') as f:
			for block in r.iter_content(chunk_size=block_size):
				if not block: break
				if pb.iscanceled():
					return False
				cached_bytes += len(block)
				f.write(block)
				if total_bytes > 0:
					delta = int(time.time() - start)
					if delta:
						kbs = int(cached_bytes / (delta * 1000))
					else: kbs = 0
					percent = int(cached_bytes * 100 / total_bytes)
					pb.update(percent, "Downloading",filename, format_speed(kbs))
		pb.close()
		if unzip:
			zip_ref = zipfile.ZipFile(temp_file, 'r')
			zip_ref.extractall(destination)
			zip_ref.close()
			kodi.vfs.rm(temp_file, quiet=True)
		else:
			kodi.vfs.mv(temp_file, kodi.vfs.join(destination, filename))
	else:
		kodi.close_busy_dialog()
		raise downloaderException(r.status_code)
	return True	
	
