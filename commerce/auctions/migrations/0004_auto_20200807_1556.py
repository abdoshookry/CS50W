# Generated by Django 3.0.8 on 2020-08-07 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200805_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listings',
            name='image',
            field=models.URLField(max_length=400000),
        ),
    ]
