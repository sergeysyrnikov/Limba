# Generated by Django 4.0 on 2021-12-30 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_object_chief_alter_object_fullname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='is_new_task',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='object',
            name='number_tasks',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Количество задач'),
        ),
    ]
