# Generated by Django 3.0.8 on 2020-08-31 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0017_auto_20200826_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='no_followers',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='no_following',
        ),
    ]
