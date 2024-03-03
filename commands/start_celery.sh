#!/bin/bash

celery -A app worker -l info -c $CELERY_NUM_WORKERS
