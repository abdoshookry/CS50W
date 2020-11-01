# Generated by Django 3.0.8 on 2020-08-20 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20200820_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='follow_info', to=settings.AUTH_USER_MODEL),
        ),
    ]