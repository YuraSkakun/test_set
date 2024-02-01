from django.db.models.signals import post_save
from django.dispatch import receiver

from testsuite.models import TestResult


@receiver(post_save, sender=TestResult)
def save_result(sender, instance, **kwargs):
    if instance.is_completed:
        user = instance.user
        user.update_score()
        user.save()
