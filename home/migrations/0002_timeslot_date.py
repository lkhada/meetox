# Generated by Django 4.1.1 on 2022-09-17 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="timeslot",
            name="date",
            field=models.DateField(null=True),
        ),
    ]
