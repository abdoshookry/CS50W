# Generated by Django 3.0.8 on 2020-08-31 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0018_auto_20200831_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='followers',
        ),
    ]
