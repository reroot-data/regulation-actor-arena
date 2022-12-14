# Generated by Django 4.1 on 2022-08-25 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("countries", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeedbackAttachment",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("size", models.BigIntegerField()),
                ("documentId", models.CharField(max_length=1000)),
                ("ers_file_name", models.CharField(max_length=1000)),
                ("pages", models.IntegerField(blank=True, null=True)),
                ("pdf_size", models.BigIntegerField()),
                ("is_rendered", models.BooleanField()),
                ("is_externalized_in_hrs", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="Feedback",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("language", models.CharField(max_length=10)),
                (
                    "organization",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("surname", models.CharField(blank=True, max_length=500, null=True)),
                ("feedback", models.CharField(blank=True, max_length=10000, null=True)),
                ("feedback_en", models.TextField(blank=True, null=True)),
                ("first_name", models.CharField(blank=True, max_length=500, null=True)),
                ("date_feedback", models.DateTimeField()),
                ("publication", models.CharField(max_length=100)),
                (
                    "company_size",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("tr_number", models.CharField(blank=True, max_length=100, null=True)),
                ("is_my_feedback", models.BooleanField()),
                ("reference_initiative", models.CharField(max_length=200)),
                ("history_event_occurs", models.BooleanField()),
                ("publication_id", models.BigIntegerField()),
                ("publication_status", models.CharField(max_length=100)),
                (
                    "attachments",
                    models.ManyToManyField(
                        blank=True, to="feedbacks.feedbackattachment"
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="countries.country",
                    ),
                ),
            ],
        ),
    ]
