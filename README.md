chatty-hippy
============

hipchat notifier running off pynotify &amp; libnotify

e.g. Running on cron
---------------------

### Using virtualenv

	*/1 * * * * export XAUTHORITY=/home/enru/.Xauthority && export DISPLAY=:0 && . /home/enru/chatty-hippy/bin/activate && /home/enru/chatty-hippy/hip.py > /dev/null

### Without virtualenv

	*/1 * * * * export XAUTHORITY=/home/enru/.Xauthority && export DISPLAY=:0 && /home/enru/chatty-hippy/hip.py > /dev/null

