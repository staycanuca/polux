# -*- coding: utf-8 -*-
import xbmc

from resources.lib.misc import *
from resources.lib.db import DB


class Monitor(xbmc.Monitor):
    pass


if __name__ == '__main__':
    db = DB(os.path.join(addonprofile, 'database.db'))
    monitor = Monitor()
    try:
        monitor.waitForAbort()
    except AttributeError:
        # Below for Gotham support
        while not xbmc.abortRequested:
            xbmc.sleep(500)
    xbmc.log("Watchlist Service done!", level=xbmc.LOGNOTICE)
