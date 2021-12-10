# Generated by Django 3.2.9 on 2021-11-27 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_class_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='warning',
            name='reason',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warning',
            name='semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='warnings_issued', to='course.semester'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='class',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='course.semester'),
        ),
    ]