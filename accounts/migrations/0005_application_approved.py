# Generated by Django 3.2.9 on 2021-11-23 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20211123_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]