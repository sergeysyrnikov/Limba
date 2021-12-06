# Generated by Django 3.2.4 on 2021-12-06 13:22

from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_rename_title_uploadfilemaintask_name_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFileSubTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_file', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to=main.models.upload_path_files_subtask)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('subtask', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subtask_file', to='main.subtask')),
            ],
            options={
                'db_table': 'subtask_files',
            },
        ),
        migrations.CreateModel(
            name='UploadFileObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_file', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to=main.models.upload_path_files_to_object)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('object', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='object_file', to='main.object')),
            ],
            options={
                'db_table': 'object_files',
            },
        ),
        migrations.CreateModel(
            name='FileSubTaskComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_file', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to=main.models.upload_path_files_subtask_comment)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('comment_subtask', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files_subtask_comment', to='main.subtaskcomment')),
            ],
            options={
                'db_table': 'files_subtask_comment',
            },
        ),
        migrations.CreateModel(
            name='FileMainTaskComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_file', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to=main.models.upload_path_files_maintask_comment)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('comment_maintask', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files_maintask_comment', to='main.maintaskcomment')),
            ],
            options={
                'db_table': 'files_maintask_comment',
            },
        ),
    ]