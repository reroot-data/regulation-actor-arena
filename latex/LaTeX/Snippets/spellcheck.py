import re

from django.db.models.signals import pre_save
from django.dispatch import receiver
from feedbacks.models import Feedback
from spellchecker import SpellChecker


@receiver(pre_save, sender=Feedback)
def feedback_spell_check(sender, instance, *args, **kwargs):
    spell = SpellChecker()
    list_words = re.findall("[a-zA-Z]}", instance.feedback_en)
    misspelled = spell.unknown(list_words)
    for word in misspelled:
        instance.feedback_en.replace(word, spell.correction(word))
