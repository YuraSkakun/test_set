import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic.base import View
from django.views.generic import ListView

from testsuite.models import Test, TestResult, Question, Variant, TestResultDetail
from user_account.models import User

# from testsuite.tasks import run_slow


# class TestListView(LoginRequiredMixin, ListView):
class TestListView(ListView):
    model = Test
    template_name = 'testsuit/test_list.html'
    context_object_name = 'test_list'
    # login_url = reverse_lazy('account:login')

    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-id')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Test Suites'
        return context


class UserLeaderBoardListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'testsuite/result_list.html'
    context_object_name = 'user_list'
    login_url = reverse_lazy('account:login')

    paginate_by = 5

    # context_object_name = 'result_list'
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     qs = qs.select_related('user')
    #     qs = qs.order_by('-avr_score')
    #     return qs

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-avr_score')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Leader Board'
        return context


class StartTestView(LoginRequiredMixin, View):

    login_url = reverse_lazy('account:login')

    def get(self, request, pk):
        test = Test.objects.get(pk=pk)

        test_result_id = request.session.get('testresult')  # id or None

        if test_result_id:
            test_result = TestResult.objects.get(id=test_result_id)
        else:
            test_result = TestResult.objects.create(
                user=request.user,
                test=test
            )

        request.session['testresult'] = test_result.id

        best_result = User.objects.aggregate(Max('avr_score')).get('avr_score__max')
        best_result_users = User.objects.filter(avr_score=best_result)

        return render(
            request=request,
            template_name='testsuite/testrun_start.html',
            context={
                'test': test,
                'test_result': test_result,
                'best_result': round(best_result, 2),
                'best_result_users': best_result_users,
            },
        )


class TestRunView(LoginRequiredMixin, View):

    login_url = reverse_lazy('account:login')

    PREFIX = 'answer_'

    def get(self, request, pk):

        if 'testresult' not in request.session:
            return HttpResponse('ERROR!')

        # if 'testresult_step' not in request.session:
        #     testresult_step =1
        # else:
        #     testresult_step = request.session['testresult_step']
        # # == analog stroki nizhe ==
        testresult_step = request.session.get('testresult_step', 1)
        request.session['testresult_step'] = testresult_step

        # question = Question.objects.filter(test__id=pk, number=testresult_step).first()
        question = Question.objects.get(test__id=pk, number=testresult_step)

        variants = [
            variant.text
            for variant in question.variants.all()
        ]

        return render(
            request=request,
            template_name='testsuite/testrun.html',
            context={
                'question': question,
                'variants': variants,
                'prefix': self.PREFIX
            }
        )

    def post(self, request, pk):

        if 'testresult_step' not in request.session:
            return HttpResponse('ERROR!')

        testresult_step = request.session['testresult_step']

        test = Test.objects.get(pk=pk)
        # question = Question.objects.filter(test__id=pk, number=testresult_step).first()
        question = Question.objects.get(test__id=pk, number=testresult_step)

        variants = Variant.objects.filter(
            question=question
        ).all()

        # data = request.POST

        choices = {
            k.replace(self.PREFIX, ''): True
            for k in request.POST if k.startswith(self.PREFIX)
        }

        if not choices:
            messages.error(self.request, extra_tags='danger', message="ERROR: You should select at least 1 answer!")
            return redirect(reverse('testsuite:next', kwargs={'pk': pk}))

        if len(choices) == len(variants):
            messages.error(self.request, extra_tags='danger', message="ERROR: You can't select ALL answers!")
            return redirect(reverse('testsuite:next', kwargs={'pk': pk}))

        # current_test_result = TestResult.objects.filter(
        #     test=test,
        #     user=request.user,
        #     is_completed=False).last()
        current_test_result = TestResult.objects.get(
            id=request.session['testresult']
        )

        for idx, variant in enumerate(variants, 1):
            value = choices.get(str(idx), False)
            TestResultDetail.objects.create(
                test_result=current_test_result,
                question=question,
                variant=variant,
                is_correct=(value == variant.is_correct)
            )

        if question.number < test.questions_count():
            current_test_result.is_new = False
            current_test_result.save()
            request.session['testresult_step'] = testresult_step + 1
            return redirect(reverse('testsuite:next', kwargs={'pk': pk}))
        else:
            del request.session['testresult']
            del request.session['testresult_step']
            # current_test_result.avr_score = ...
            # current_test_result.update_score()  # make up this method
            # current_test_result.is_complete = True
            current_test_result.finish()
            current_test_result.save()

            current_user = User.objects.get(pk=request.user.pk)
            # current_user = request.user
            current_user.update_score()
            current_user.save()

            score_info = current_test_result.score_info()
            score_result = current_test_result.avr_score

            return render(
                request=request,
                template_name='testsuite/testrun_end.html',
                context={
                    'test': test,
                    'score_info': score_info,
                    'score_result': round(score_result, 2),
                    'test_result': current_test_result,
                    'time_spent': datetime.datetime.utcnow() - current_test_result.datetime_run.replace(tzinfo=None),
                    # 'is_correct': is_correct,
                    # 'questions_count': test.questions_count(),
                    # 'test': test
                }
            )


# class TestRunView(View):
#
#     def get(self, request, pk, seq_nr):
#         question = Question.objects.filter(test__id=pk, number=seq_nr).first()
#
#         variants = [
#             variant.text
#             for variant in question.variants.all()
#         ]
#
#         return render(
#             request=request,
#             template_name='testsuite/testrun.html',
#             context={
#                 'question': question,
#                 'variants': variants
#             }
#         )
#
#     def post(self, request, pk, seq_nr):
#
#         return HttpResponse('OK')


# class TestRunView(View):
#     PREFIX = 'answer_'
#     variants_count = []
#
#     def get(self, request, pk, seq_nr):
#         print(self.variants_count)
#
#         if 'testresult' not in request.session:
#             return HttpResponse('ERROR!')
#
#         question = Question.objects.filter(test__id=pk, number=seq_nr).first()
#
#         variants = [
#             variant.text
#             for variant in question.variants.all()
#         ]
#
#         return render(
#             request=request,
#             template_name='testsuite/testrun.html',
#             context={
#                 'question': question,
#                 'variants': variants,
#                 'prefix': self.PREFIX
#             }
#         )
#
#     def post(self, request, pk, seq_nr):
#         test = Test.objects.get(pk=pk)
#         question = Question.objects.filter(test__id=pk, number=seq_nr).first()
#
#         variants = Variant.objects.filter(
#             question=question
#         ).all()
#
#         # data = request.POST
#
#         choices = {
#             k.replace(self.PREFIX, ''): True
#             for k in request.POST if k.startswith(self.PREFIX)
#         }
#
#         self.variants_count.append(variants.count())
#
#         if not choices:
#             messages.error(self.request, extra_tags='danger', message="ERROR: You should select at least 1 answer!")
#             return redirect(reverse('testsuite:testrun_step', kwargs={'pk': pk, 'seq_nr': seq_nr}))
#
#         if len(choices) == len(variants):
#             messages.error(self.request, extra_tags='danger', message="ERROR: You can't select ALL answers!")
#             return redirect(reverse('testsuite:testrun_step', kwargs={'pk': pk, 'seq_nr': seq_nr}))
#
#         # current_test_result = TestResult.objects.filter(
#         #     test=test,
#         #     user=request.user,
#         #     is_completed=False).last()
#         current_test_result = TestResult.objects.get(
#             id=request.session['testresult']
#         )
#
#         for idx, variant in enumerate(variants, 1):
#             value = choices.get(str(idx), False)
#             TestResultDetail.objects.create(
#                 test_result=current_test_result,
#                 question=question,
#                 variant=variant,
#                 is_correct=(value == variant.is_correct)
#             )
#
#         if question.number < test.questions_count():
#             return redirect(reverse('testsuite:testrun_step', kwargs={'pk': pk, 'seq_nr': seq_nr + 1}))
#         else:
#             qs = current_test_result.test_result_details.values('question').filter(is_correct=True).\
#                 annotate(Count('is_correct'))
#
#             is_correct = 0
#             for qs_item in zip(qs, self.variants_count):
#                 if qs_item[0].get('is_correct__count') == qs_item[1]:
#                     is_correct += 1
#
#             self.variants_count.clear()
#
#             # current_test_result.avr_score = ...
#             # current_test_result.update_score()  # make up this method
#             # current_test_result.is_complete = True
#             current_test_result.finish()
#             current_test_result.save()
#
#             current_user = User.objects.get(pk=request.user.pk)
#             current_user.update_score()
#             current_user.save()
#
#             return render(
#                 request=request,
#                 template_name='testsuite/testrun_end.html',
#                 context={
#                     'test_result': current_test_result,
#                     'time_spent': datetime.datetime.utcnow() - current_test_result.datetime_run.replace(tzinfo=None),
#                     'is_correct': is_correct,
#                     'questions_count': test.questions_count(),
#                     'test': test
#                 }
#             )


# def run_slow():
#     import time
#     time.sleep(10)
#
# def slow_func(request):
#     run_slow()
#     return HttpResponse('DONE!')


def slow_func(request):
    # run_slow()
    run_slow.delay(10)
    return HttpResponse('DONE!')
