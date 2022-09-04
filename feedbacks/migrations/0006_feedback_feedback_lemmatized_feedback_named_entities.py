# Generated by Django 4.1 on 2022-09-04 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("named_entities", "0001_initial"),
        ("feedbacks", "0005_alter_feedback_publication_object"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedback",
            name="feedback_lemmatized",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="feedback",
            name="named_entities",
            field=models.ManyToManyField(
                blank=True, null=True, to="named_entities.namedentity"
            ),
        ),
    ]