#!/usr/bin/env python

import os
import pynotify
import hipchat.config
from configobj import ConfigObj
from hipchat.room import Room
from datetime import datetime
from time import sleep, mktime

def init_cfg():
	global cfg_file
	hipchat.config.init_cfg(cfg_file)
	cfg = ConfigObj(cfg_file)
	hipchat.config.room_id = cfg.get('room_id', 0)
	hipchat.config.since = cfg.get('since', datetime.today())
	if isinstance(hipchat.config.since, str):
		hipchat.config.since = datetime.fromtimestamp(float(hipchat.config.since))
	
def write_cfg():
	global cfg_file
	cfg = ConfigObj(cfg_file)
	cfg['since'] = mktime(datetime.now().timetuple())
	cfg.write()

def is_since(m, since):
	dt = datetime.strptime(m.date[:-5], "%Y-%m-%dT%H:%M:%S")
	return dt >= since 

def notify(n, m):
	n.update(m.__getattribute__('from')['name'], m.message)
	n.show()
	sleep(3)

cfg_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'hipchat.cfg')

init_cfg()

if not pynotify.init("hipchat"):
	sys.exit(1)

n = pynotify.Notification("hipchat", "firing up")

x={"room_id": hipchat.config.room_id, "date": hipchat.config.since.strftime("%Y-%m-%d"), "timezone": "Europe/London", "format": "json"}

history=filter((lambda msg: is_since(msg, hipchat.config.since)), Room.history(**x))

map((lambda m: notify(n,m)), history)

write_cfg()
