# Generated by Django 5.0.1 on 2024-01-23 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='each_nth_cup_free',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
