# Generated by Django 4.1 on 2023-03-30 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="create_date",
            new_name="created_date",
        ),
    ]
