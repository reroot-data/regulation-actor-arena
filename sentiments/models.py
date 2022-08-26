from django.db import models


class Sentiment(models.Model):
    feedback = models.ForeignKey('feedbacks.Feedback', on_delete=models.CASCADE)
    positive = models.DecimalField(max_digits=4, decimal_places=3)
    neutral = models.DecimalField(max_digits=4, decimal_places=3)
    negative = models.DecimalField(max_digits=4, decimal_places=3)
    compound = models.DecimalField(max_digits=5, decimal_places=4)
