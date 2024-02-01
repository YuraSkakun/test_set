from django.db import models

# Create your models here.

import datetime
from django.contrib.auth.models import AbstractUser
from django.db.models import Max, Sum, Case, When, Count, IntegerField

from testsuite.models import TestResultDetail


"""
-- Create model User
--
CREATE TABLE "user_account_user" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "password" varchar(128) NOT NULL,
    "last_login" datetime NULL, "is_superuser" bool NOT NULL,
    "username" varchar(150) NOT NULL UNIQUE,
    "first_name" varchar(150) NOT NULL,
    "last_name" varchar(150) NOT NULL,
    "email" varchar(254) NOT NULL,
    "is_staff" bool NOT NULL,
    "is_active" bool NOT NULL,
    "date_joined" datetime NOT NULL,
    "image" varchar(100) NOT NULL,
    "avr_score" decimal NOT NULL,
    "number_tests_passed" integer unsigned NULL CHECK ("number_tests_passed" >= 0),
    "percent_success" decimal NULL,
    "location" varchar(30) NOT NULL,
    "birth_date" date NULL,
    "correct_answers_count" integer unsigned NULL CHECK ("correct_answers_count" >= 0),
    "total_questions" integer unsigned NULL CHECK ("total_questions" >= 0)
);
"""


class User(AbstractUser):
    image = models.ImageField(default='default.jpg', upload_to='pics')
    avr_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=True)
    number_tests_passed = models.PositiveIntegerField(null=True, blank=True, default=0)
    percent_success = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, null=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True, default=datetime.date.today)
    correct_answers_count = models.PositiveIntegerField(null=True, blank=True, default=0)
    total_questions = models.PositiveIntegerField(null=True, blank=True, default=0)

    def update_score(self):
        results = TestResultDetail.objects\
            .filter(
                test_result__user=self,
                test_result__is_completed=True)\
            .values(
                'test_result',
                'question')\
            .annotate(
                answers=Sum(
                    Case(
                        When(is_correct=1, then=1),
                        output_field=IntegerField()
                    )
                ),
                # answers=Sum('is_correct'),
                questions=Count('question')
            )

        """
            SELECT "testsuite_testresultdetail"."test_result_id", "testsuite_testresultdetail"."question_id",
            SUM(CASE WHEN "testsuite_testresultdetail"."is_correct" = 1 THEN 1 ELSE NULL END) AS "answers",
            COUNT("testsuite_testresultdetail"."question_id") AS "questions"
            FROM "testsuite_testresultdetail"
            INNER JOIN "testsuite_testresult"
            ON ("testsuite_testresultdetail"."test_result_id" = "testsuite_testresult"."id")
            WHERE ("testsuite_testresult"."is_completed" AND "testsuite_testresult"."user_id" = 1)
            GROUP BY "testsuite_testresultdetail"."test_result_id", "testsuite_testresultdetail"."question_id";
        """

        """
            results
            <QuerySet [
            {'test_result': 1, 'question': 1, 'answers': 4, 'questions': 4},
            {'test_result': 1, 'question': 2, 'answers': 4, 'questions': 4},
            {'test_result': 1, 'question': 3, 'answers': 3, 'questions': 3},
            {'test_result': 1, 'question': 4, 'answers': 4, 'questions': 4},
            {'test_result': 2, 'question': 1, 'answers': 3, 'questions': 4},
            {'test_result': 2, 'question': 2, 'answers': 4, 'questions': 4},
            {'test_result': 2, 'question': 3, 'answers': 3, 'questions': 3},
            {'test_result': 2, 'question': 4, 'answers': 4, 'questions': 4}
            ]>
        """

        self.correct_answers_count = sum(result['answers'] == result['questions'] for result in results)
        self.total_questions = len(results)
        if self.total_questions:
            # self.avr_score = self.correct_answers_count / self.total_questions * 100
            self.avr_score = round((self.correct_answers_count / self.total_questions) * 100, 2)

    def count_passed_tests(self):
        return self.test_results.filter(is_completed=True).count()

    def total_score(self):
        return self.avr_score

    def last_run(self):
        if self.test_results.count() != 0:
            return self.test_results.last().datetime_run
        else:
            return "_____"

    # def update_score(self):
    #     points = self.test_results.aggregate(total=Sum('avr_score')).get('total', 0.0)
    #     self.avr_score = points / self.test_results.count()
    #
    # def count_passed_tests(self):
    #     return self.test_results.filter(is_completed=True).count()
    #
    # def total_score(self):
    #     return self.avr_score

    def percent_success_passed(self):
        percent_success_passed = sum([tr.percent_correct_answers() for tr in
                                      self.test_results.filter(is_completed=True)])
        return round(percent_success_passed, 2)

    def test_last_run(self):
        last_run = self.test_results.last()  # order_by('-id').first()
        # return last_run.datetime_run
        if last_run:
            return last_run.datetime_run
        return ''
