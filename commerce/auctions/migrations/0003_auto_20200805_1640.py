# Generated by Django 3.0.8 on 2020-08-05 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200804_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listings',
            name='category',
            field=models.CharField(default='no category', max_length=64),
        ),
    ]
