import re

from django.db.models.signals import pre_save
from django.dispatch import receiver
from feedbacks.models import Feedback
from nltk.stem import WordNetLemmatizer


@receiver(pre_save, sender=Feedback)
def feedback_lemmatization(sender, instance, *args, **kwargs):
    lemmatizer = WordNetLemmatizer()
    text_list = re.findall("[a-zA-Z]}", instance.feedback_en)
    lemmatized = [lemmatizer.lemmatize(word) for word in text_list]
    instance.feedback_lemmatized = " ".join(lemmatized)
