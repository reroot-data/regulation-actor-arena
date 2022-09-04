import re

from django.db.models.signals import pre_save
from django.dispatch import receiver
from feedbacks.models import Feedback


@receiver(pre_save, sender=Feedback)
def feedback_trim_whitespaces(sender, instance, *args, **kwargs):
    instance.feedback_en = re.sub(" +", " ", instance.feedback_en)
