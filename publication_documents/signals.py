import io

import pandas as pd
import plotly.express as px
from django.core.files.base import ContentFile, File
from django.core.files.images import ImageFile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from sentiments.models import Sentiment

from .models import Publication


@receiver(pre_save, sender=Publication)
def Publication_create_plot(sender, instance, *args, **kwargs):
    sentiments = Sentiment.objects.filter(feedback__publication_object=instance)

    if not sentiments.exists():
        return

    values_list = [
        "feedback__organization",
        "positive",
        "negative",
        "feedback__user_type",
    ]
    sentiments_data = sentiments.values_list(*values_list)
    df = pd.DataFrame.from_records(sentiments_data, columns=values_list)
    fig = px.scatter(
        df,
        x="positive",
        y="negative",
        text="feedback__organization",
        color="feedback__user_type",
        width=1500,
        height=1500,
    )
    fig.update_traces(textposition="top center")
    fig_bytes = fig.to_image(format="png")
    fig_html = fig.to_html()

    instance.sentiment_map_png = ImageFile(
        io.BytesIO(fig_bytes), name=f"{instance.reference}_({instance.id}).png"
    )
    instance.sentiment_map_html = File(
        io.StringIO(fig_html), name=f"{instance.reference}_({instance.id}).html"
    )
