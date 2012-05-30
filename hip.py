#!/usr/bin/env python

import pynotify
import hipchat.config
from configobj import ConfigObj
from hipchat.room import Room
from datetime import datetime
from time import sleep, mktime

def init_cfg(fname):
	hipchat.config.init_cfg(fname)
	cfg = ConfigObj(fname)
	hipchat.config.room_id = cfg.get('room_id', 0)
	hipchat.config.since = cfg.get('since', datetime.today())
	if isinstance(hipchat.config.since, str):
		hipchat.config.since = datetime.fromtimestamp(float(hipchat.config.since))
	
def write_cfg(fname):
	cfg = ConfigObj(fname)
	cfg['since'] = mktime(datetime.now().timetuple())
	cfg.write()

def is_since(m, since):
	dt = datetime.strptime(m.date[:-5], "%Y-%m-%dT%H:%M:%S")
	return dt >= since 

def notify(n, m):
	n.update("%s: %s" % (m.__getattribute__('from')['name'], m.message))
	n.show()
	sleep(3)

init_cfg('hipchat.cfg')

n = pynotify.Notification("hipchat", "firing up")

x={"room_id": hipchat.config.room_id, "date": hipchat.config.since.strftime("%Y-%m-%d"), "timezone": "Europe/London", "format": "json"}

history=filter((lambda msg: is_since(msg, hipchat.config.since)), Room.history(**x))

map((lambda m: notify(n,m)), history)

write_cfg('hipchat.cfg')
