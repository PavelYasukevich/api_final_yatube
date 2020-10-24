# Generated by Django 3.1.2 on 2020-10-23 12:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api", "0004_auto_20201023_1144"),
    ]

    operations = [
        migrations.AlterField(
            model_name="follow",
            name="following",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="following",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]