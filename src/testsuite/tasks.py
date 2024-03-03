import datetime

import time
from celery import shared_task
from django.conf import settings

from testsuite.models import TestResult, Test


@shared_task
def run_slow(n):
    time.sleep(n)
    print('REALLY DONE!')


@shared_task
def run_slow_1(id):
    test = Test.objects.get(id=id)
    print(test.title)
    print('REALLY TEST_TITLE DONE!')


@shared_task
def cleanup_outdated_testruns():
    outdated_tests = TestResult.objects.filter(
        is_completed=False,
        datetime_run__lte=datetime.datetime.now() - datetime.timedelta(seconds=settings.SESSION_COOKIE_AGE)
    )
    outdated_tests.delete()

    print('Outdated testresults deleted!')
