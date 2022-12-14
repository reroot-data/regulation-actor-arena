# Generated by Django 4.1 on 2022-08-25 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("initiatives", "0003_alter_legalbasis_article"),
        ("publication_documents", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attachment",
            name="work_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="initiatives.type",
            ),
        ),
    ]
