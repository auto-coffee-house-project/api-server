# Generated by Django 4.2.9 on 2024-02-04 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0003_shopclient_shop_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopgroup',
            name='gift_name',
            field=models.CharField(default='Бесплатная чашка кофе', max_length=64),
        ),
        migrations.AddField(
            model_name='shopgroup',
            name='gift_photo_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
