# Generated by Django 3.0.8 on 2020-08-26 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0015_auto_20200826_1517'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='x',
            new_name='likes',
        ),
    ]