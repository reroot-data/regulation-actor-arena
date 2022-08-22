# Generated by Django 4.1 on 2022-08-21 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("initiatives", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="initiative",
            name="initiative_status",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="initiatives.status",
            ),
        ),
    ]
