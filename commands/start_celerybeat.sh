#!/bin/bash

rm /tmp/celerybeat-schedule /tmp/celerybeat.pid
celery -A app beat -l info --schedule=/tmp/celerybeat-schedule --pidfile=/tmp/celerybeat.pid
#celery -A settings beat --loglevel=info --workdir=/srv/project/src --schedule=/srv/project/tmp/celerybeat-schedule --pidfile=/srv/project/tmp/celerybeat.pid
