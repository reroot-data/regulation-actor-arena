# Generated by Django 4.1 on 2022-08-25 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("topics", "0001_initial"),
        ("committees", "0001_initial"),
        ("initiatives", "0001_initial"),
        ("publication_documents", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="initiative",
            name="publications",
            field=models.ManyToManyField(
                blank=True, to="publication_documents.publication"
            ),
        ),
        migrations.AddField(
            model_name="initiative",
            name="receiving_feedback_status",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="initiative_feedback_status",
                to="initiatives.status",
            ),
        ),
        migrations.AddField(
            model_name="initiative",
            name="stage",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="initiatives.stage"
            ),
        ),
        migrations.AddField(
            model_name="initiative",
            name="topics",
            field=models.ManyToManyField(to="topics.topic"),
        ),
        migrations.AddField(
            model_name="initiative",
            name="unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="committees.unit",
            ),
        ),
    ]
