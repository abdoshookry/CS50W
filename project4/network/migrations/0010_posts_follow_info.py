# Generated by Django 3.0.8 on 2020-08-22 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_auto_20200821_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='follow_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follow_info', to='network.follow'),
        ),
    ]