# Generated by Django 4.2.9 on 2024-02-06 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0006_alter_shopclient_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopclient',
            name='has_gift',
            field=models.BooleanField(default=False),
        ),
    ]
