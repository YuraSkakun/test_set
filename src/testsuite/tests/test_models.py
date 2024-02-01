import datetime

from django.core.management import call_command
from django.test import TestCase

from testsuite.models import Test, Question

'''
class TestModelTest(TestCase):

    def test_questions_count(self):
        test = Test.objects.create(title='Test title')
        question = Question.objects.create(
            test=test,
            number=1,
            text='Question text'
        )

        self.assertEqual(test.questions_count(), 1)

    def test_last_run(self):
        call_command('loaddata', 'tests/fixtures/accounts.json', verbosity=0)
        call_command('loaddata', 'tests/fixtures/tests.json', verbosity=0)

        test = Test.objects.first()
        self.assertEqual(test.questions_count(), 4)

        dt = datetime.datetime.strptime('2020-11-22T18:31:12.809Z', "%Y-%m-%dT%H:%M:%S.%f%z")
        self.assertEqual(test.last_run(), dt)

        # dt = datetime.datetime.strptime('2020-11-22T18:31:12.809Z', "%Y-%m-%dT%H:%M:%S.%fz")
        # self.assertEqual(test.last_run().replace(tzinfo=None), dt)
'''


class TestModelTest(TestCase):

    def setUp(self):
        call_command('loaddata', 'tests/fixtures/accounts.json', verbosity=0)
        call_command('loaddata', 'tests/fixtures/tests.json', verbosity=0)

    def tearDown(self):
        pass

    def test_questions_count_1(self):
        test = Test.objects.first()
        count = test.questions_count()

        # test = Test.objects.create(title='Test title')
        question = Question.objects.create(
            test=test,
            number=1,
            text='Question text'
        )
        print(question)
        self.assertEqual(test.questions_count(), count + 1)

    def test_questions_count(self):
        test = Test.objects.first()
        self.assertEqual(test.questions_count(), 4)

    def test_last_run(self):
        test = Test.objects.first()
        self.assertEqual(test.questions_count(), 4)

        # print(test.last_run())

        dt = datetime.datetime.strptime('2020-11-22T18:31:12.809Z', "%Y-%m-%dT%H:%M:%S.%f%z")
        self.assertEqual(test.last_run(), dt)

        # dt = datetime.datetime.strptime('2020-11-22T18:31:12.809Z', "%Y-%m-%dT%H:%M:%S.%fz")
        # self.assertEqual(test.last_run().replace(tzinfo=None), dt)
