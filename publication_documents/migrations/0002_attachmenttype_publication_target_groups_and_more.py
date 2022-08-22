# Generated by Django 4.1 on 2022-08-22 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("committees", "0002_targetgroup"),
        ("initiatives", "0004_alter_initiative_receiving_feedback_status"),
        ("publication_documents", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttachmentType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="publication",
            name="target_groups",
            field=models.ManyToManyField(to="committees.targetgroup"),
        ),
        migrations.AlterField(
            model_name="publication",
            name="front_end_stage",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="publication_front_end",
                to="initiatives.stage",
            ),
        ),
        migrations.AlterField(
            model_name="attachment",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="publication_documents.attachmenttype",
            ),
        ),
    ]