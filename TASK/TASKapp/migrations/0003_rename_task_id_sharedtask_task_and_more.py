# Generated by Django 5.1.1 on 2024-10-02 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("TASKapp", "0002_sharedtask_task_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="sharedtask",
            old_name="task_id",
            new_name="task",
        ),
        migrations.RenameField(
            model_name="sharedtask",
            old_name="user_id",
            new_name="user",
        ),
    ]
