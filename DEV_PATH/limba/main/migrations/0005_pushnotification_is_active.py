# Generated by Django 3.1.5 on 2021-11-18 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20211116_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='pushnotification',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
