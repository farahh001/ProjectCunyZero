# Generated by Django 3.2.9 on 2021-11-30 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_shoppingcart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='thumbnail',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='thumbnails/'),
        ),
    ]