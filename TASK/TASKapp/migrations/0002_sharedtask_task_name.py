# Generated by Django 5.1.1 on 2024-10-02 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TASKapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sharedtask",
            name="task_name",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
