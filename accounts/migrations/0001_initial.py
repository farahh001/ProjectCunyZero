# Generated by Django 3.2.7 on 2021-12-06 05:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('role', models.CharField(choices=[('ins', 'Instructor'), ('std', 'Student')], max_length=50)),
                ('document', models.FileField(upload_to='applications/')),
                ('approved', models.BooleanField(default=False)),
                ('rejected', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('ins', 'Instructor'), ('std', 'Student')], max_length=50)),
                ('image', models.ImageField(upload_to='profile_pics/')),
                ('suspended', models.BooleanField(default=False)),
                ('GPA', models.FloatField(default=0.0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GPA', models.FloatField(default=0.0)),
                ('by_instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='given_grades', to='accounts.profile')),
            ],
        ),
    ]