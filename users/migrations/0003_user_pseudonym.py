# Generated by Django 4.2.6 on 2023-10-19 09:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_user_last_login_at_user_last_request_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="pseudonym",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
