# Generated by Django 4.0 on 2022-01-02 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_remove_object_is_new_task_remove_object_number_tasks'),
    ]

    operations = [
        migrations.AddField(
            model_name='subdepartmentobject',
            name='object_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Объект'),
        ),
    ]
