from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.dispatch import receiver
import os
from os.path import join
import shutil
import glob
import pandas as pd
import pdfkit
import threading
import subprocess
# from .managers import CustomUserManager

"""Function create folder"""

def path_folder(path_abs):
    index = 0
    for i,el in enumerate(path_abs):
        if el == '/':
            index = i
    if index > 0:
        return path_abs[0:index]
    else:
        return ''

"""Function delete file"""

def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)
   path_f = path_folder(path)
   lst = glob.glob(join(path_f,'*.jpg'))
   if (len(lst) == 0):
       lst = glob.glob(join(path_f,'*.png'))
   if len(lst) == 0 and os.path.exists(path_f):
       shutil.rmtree(path_f)

"""Path uploading object imgs"""

def upload_path_object(self, filename):
    return '/'.join(['imageObject', str(self.object.code), str(self.object.shortname), filename])

"""Path uploading main imgs"""

def upload_path_main(self, filename):
    return '/'.join(['imageMainTask', str(self.task.full_link).replace(" ", "").replace("|", "/"), str(self.task.task_name), filename])

"""Path uploading sub imgs"""

def upload_path_sub(self, filename):
    return '/'.join(['imageSubTask', str(self.subtask.full_link).replace(" ", "").replace("|", "/"), str(self.subtask.task_name), filename])

"""Path uploading main comment"""

def upload_path_main_comment(self, filename):
    last_index = len(self.comment_maintask.comment)
    if (last_index > 10):
        last_index = 10
    return '/'.join(['imageMainTask', str(self.comment_maintask.task.full_link).replace(" ", "").replace("|", "/"), str(self.comment_maintask.task.task_name), 'Комментарий #' + str(self.comment_maintask.id) + '(' + self.comment_maintask.comment[0:last_index] + ')', filename])

"""Path uploading sub comment"""

def upload_path_sub_comment(self, filename):
    last_index = len(self.comment_subtask.comment)
    if (last_index > 10):
        last_index = 10
    return '/'.join(['imageSubTask', str(self.comment_subtask.subtask.full_link).replace(" ", "").replace("|", "/"), str(self.comment_subtask.subtask.task_name), 'Комментарий #' + str(self.comment_subtask.id) + '(' + self.comment_subtask.comment[0:last_index] + ')', filename])

"""Path uploading object files"""

def upload_path_files_to_object(self, filename):
    return '/'.join(['filesObject', str(self.object.code), str(self.object.shortname), filename])

"""Path uploading files maintask"""

def upload_path_files_maintask(self, filename):
    return '/'.join(['filesMainTask', str(self.task.full_link).replace(" ", "").replace("|", "/"), str(self.task.task_name), filename])

"""Path uploading files subtask"""

def upload_path_files_subtask(self, filename):
    return '/'.join(['filesSubTask', str(self.subtask.full_link).replace(" ", "").replace("|", "/"), str(self.subtask.task_name), filename])

"""Path uploading main comment"""

def upload_path_files_maintask_comment(self, filename):
    last_index = len(self.comment_maintask.comment)
    if (last_index > 10):
        last_index = 10
    return '/'.join(['filesMainTask', str(self.comment_maintask.task.full_link).replace(" ", "").replace("|", "/"), str(self.comment_maintask.task.task_name), 'Комментарий #' + str(self.comment_maintask.id) + '(' + self.comment_maintask.comment[0:last_index] + ')', filename])

"""Path uploading main comment"""

def upload_path_files_subtask_comment(self, filename):
    last_index = len(self.comment_subtask.comment)
    if (last_index > 10):
        last_index = 10
    return '/'.join(['filesSubTask', str(self.comment_subtask.subtask.full_link).replace(" ", "").replace("|", "/"), str(self.comment_subtask.subtask.task_name), 'Комментарий #' + str(self.comment_subtask.id) + '(' + self.comment_subtask.comment[0:last_index] + ')', filename])

"""Function convert xls file"""

def convert_file_xls(path):
    try:
        cur_path = path
        index = cur_path.index(".", len(cur_path) - 5)
        cur_path = cur_path[0:index]
        df = pd.read_excel(path)
        df.to_html(cur_path + ".html")
        pdfkit.from_file(cur_path + ".html", cur_path + ".pdf")
        os.remove(cur_path + ".html")
    except Exception as ex:
        print(ex)

"""Function convert doc file"""

def convert_file_doc(path):
    try:
        print(path)
        cur_path = path
        index = cur_path.index(".", len(cur_path) - 5)
        cur_path = cur_path[0:index]
        lst = cur_path.split("/")
        cur_path = cur_path.replace("/" + lst[len(lst)-1], "")
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", path, "--outdir", cur_path])
    except Exception as ex:
        print(ex)


"""User model Limba"""

class User(AbstractUser):
    """Class User"""

    def __str__(self):
        return f"{self.username}"

"""User add info model Limba"""

class UserAdditionalInfo(models.Model):
    """Class UserAdditionalInfo"""

    positions = (
        ("0", 'Администратор'),
        ("1", 'Руководитель проектов'),
        ("2", 'Начальник отдела'),
        ("3", 'Начальник участка'),
        ("4", 'Прораб'),
        ("5", 'Монтажник'),
        ("6", 'Инженер'),
    )

    class Meta:
        db_table = 'user_info'

    user = models.ForeignKey(User, related_name='user_info', on_delete=models.CASCADE, null=True)
    abbreviation = models.CharField(_('Аббревиатура ФИО'), max_length=3, blank=False, default="")
    position_worker = models.CharField(_('Должность работника'), max_length=1, choices=positions, default=6)
    type_user = models.DecimalField(_('Тип пользователя'), max_digits=1 ,decimal_places=0 ,default=2)
    type_system = models.DecimalField(_('Тип системы'), max_digits=1 ,decimal_places=0 ,default=0)
    code_fcm = models.CharField(_('Токен пользователя'), max_length=300, default="")
    index_color = models.DecimalField(_('Цвет иконки пользователя'), max_digits=1 ,decimal_places=0 ,default=0)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"{_('Пользователь: ')}{self.user.username}."

"""Object model Limba"""

class Object(models.Model):
    """Class Object"""
    
    class Meta:
        db_table = 'objects'

    user = models.ForeignKey(User, related_name='user_limba', on_delete=models.DO_NOTHING, null=True)
    code = models.DecimalField(_('Код объекта'), max_digits=3, decimal_places=0, unique=True, null=True) 
    shortname = models.CharField(_('Сокращённое имя объекта'), max_length=8, default='', unique=True) 
    fullname = models.CharField(_('Полное имя объекта'), max_length=25, default='')
    supervisor = models.CharField(_('Руководитель проекта'), max_length=30, default='')
    chief = models.CharField(_('Начальник участка'), max_length=30, default='')
    group_number = models.DecimalField(_('Номер проектной группы'), max_digits=5, decimal_places=0, unique=True, null=True) 
    date_finished = models.DateField(_('Дата сдачи объекта'), null=True, blank=True)
    date_start_document = models.DateField(_('Дата создания ТУ Электоснабжение'), null=True, blank=True)
    date_finished_document = models.DateField(_('Дата окончания ТУ Электоснабжение'), null=True, blank=True)
    connected_workers = models.ManyToManyField(User, related_name='workers_object', blank=True)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"{_('Имя объекта: ')}{self.shortname}, {_('код: ')}{self.code}."

"""Image object model Limba"""

class ImageObject(models.Model):
    """Class ImageObject"""
  
    class Meta:
        db_table = 'objectimage'

    object = models.ForeignKey(Object, related_name='object_img', on_delete=models.CASCADE, null=True)
    image = models.ImageField(_('Фотография'), upload_to = upload_path_object, blank=True)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"Id: {self.id}, ObjectImage: {self.image}"

"""Departments model Limba"""

class Department(models.Model):
    """Class BlogCategory"""
    
    creator = models.ForeignKey(User, related_name='creator_department', on_delete=models.DO_NOTHING, null=True)
    user_assign = models.ForeignKey(User, related_name='user_assign', on_delete=models.DO_NOTHING, null=True)
    object_name = models.ForeignKey(Object, related_name='object', on_delete = models.CASCADE, null=True)
    fullname = models.CharField(_('Полное имя отдела'), max_length=30, default='')
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    class Meta:
        db_table = 'departments'
        unique_together = ("object_name", "fullname")

    def __str__(self):
        return f"{_('Имя отдела: ')}{self.fullname}, {_('Ответственный: ')}{self.user_assign}."

"""SubDepartments model Limba"""

class SubDepartmentObject(models.Model):
    """Class BlogCategory"""

    creator = models.ForeignKey(User, related_name='creator_subdepartment', on_delete=models.DO_NOTHING, null=True)    
    department = models.ForeignKey(Department, related_name='department', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, related_name='user_executor', on_delete=models.DO_NOTHING, null=True)
    fullname = models.CharField(_('Полное имя подобъекта'), max_length=30, default='')
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    class Meta:
        db_table = 'subdepartment_objects'
        unique_together = ("department", "fullname")

    def __str__(self):
        return f"{_('Название подотдела: ')}{self.fullname}, {_('Ответственный: ')}{self.user}."

"""Maintasks model Limba"""

class MainTask(models.Model):
    """Class MainTask"""

    class Meta:
        db_table = 'maintasks'

    subdepartment_object = models.ForeignKey(SubDepartmentObject, related_name='department_object', on_delete=models.CASCADE, null=True)
    creator_task = models.ForeignKey(User, related_name='creator_task', on_delete=models.DO_NOTHING, null=True)
    cols_subtasks = models.IntegerField(_('Колличество подзадач'), null=True, default=0)
    connected_workers = models.ManyToManyField(User, related_name='workers_main', blank=True)
    task_name = models.CharField(_('Заголовок'), max_length=30)
    full_link = models.CharField(_('Путь до задачи'), max_length=150)
    date_finished = models.DateField(_('Дата окончания задачи'), null=True, blank=True)
    executor_task = models.ForeignKey(User, related_name='executor_task', on_delete=models.DO_NOTHING, null=True)
    about = models.TextField(_('Подробности'), max_length=200, default="", blank=True)
    object = models.DecimalField(_('Объект'), max_digits=6, decimal_places=0, default=999999)
    location = models.CharField(_('Местоположение'), max_length=100, default="", blank=True)
    is_active = models.BooleanField(default=True)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"Задача: {self.task_name}, Исполнитель: {self.executor_task}"

"""Subtasks model Limba"""

class SubTask(models.Model):
    """Class SubTask"""

    class Meta:
        db_table = 'subtasks'

    maintask = models.ForeignKey(MainTask, related_name='maintask', on_delete=models.CASCADE, null=True)
    connected_workers = models.ManyToManyField(User, related_name='workers_sub', blank=True)
    task_name = models.CharField(_('Заголовок'), max_length=30)
    full_link = models.CharField(_('Путь до задачи'), max_length=150)
    date_finished = models.DateField(_('Дата окончания задачи'), null=True, blank=True)
    executor_task = models.ForeignKey(User, related_name='executor', on_delete=models.DO_NOTHING, null=True)
    about = models.TextField(_('Подробности'), max_length=200, default="", blank=True)
    location = models.CharField(_('Местоположение'), max_length=100, default="", blank=True)
    is_active = models.BooleanField(default=True)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"Подзадача: {self.task_name}, Исполнитель: {self.executor_task}"

"""MainImage model Limba"""

class ImageMain(models.Model):
    """Class Image"""
  
    class Meta:
        db_table = 'imagemain'
    
    task = models.ForeignKey(MainTask, related_name='maintask_img', on_delete=models.CASCADE, null=True)
    image = models.ImageField(_('Фотография'), upload_to = upload_path_main, blank=True)
    datetime = models.DateTimeField(auto_now_add=timezone.now)
    
    def __str__(self):
        return f"Id: {self.id}, Image: {self.image}"
    
"""SubImage model Limba"""

class ImageSubTask(models.Model):
    """Class SubImage"""
  
    class Meta:
        db_table = 'subimage'

    subtask = models.ForeignKey(SubTask, related_name='subtask_img', on_delete=models.CASCADE, null=True)
    image = models.ImageField(_('Фотография'), upload_to = upload_path_sub, blank=True)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"Id: {self.id}, SubImage: {self.image}"

"""MainTaskComments model Limba"""

class MainTaskComment(models.Model):
    """Class MainTaskComment"""

    class Meta:
        db_table = 'maintask_comment'
    
    task = models.ForeignKey(MainTask, related_name='maintask_comment', on_delete=models.CASCADE, null=True)
    creator_comment = models.ForeignKey(User, related_name='creator_maincomment', on_delete=models.DO_NOTHING, null=True)
    comment = models.TextField(_('Комментарий'), max_length=100, default="")
    datetime = models.DateTimeField(auto_now_add=timezone.now)
    
    def __str__(self):
        return f"Задача: {self.task}, Дата создания: {self.datetime}."

"""MainTaskImageComments model Limba"""

class ImageMainTaskComment(models.Model):
    """Class MainImageComment"""
  
    class Meta:
        db_table = 'mainimage_comment'

    comment_maintask = models.ForeignKey(MainTaskComment, related_name='mainimage_comment', on_delete=models.CASCADE, null=True)
    image = models.ImageField(_('Фотография'), upload_to = upload_path_main_comment, blank=True)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"Id: {self.id}, MainImageComment: {self.image}"

"""MainTaskFileComment model Limba"""

class FileMainTaskComment(models.Model):
    """Class FileMainTaskComment"""
  
    class Meta:
        db_table = 'files_maintask_comment'

    name_file = models.CharField(max_length = 50)
    size = models.IntegerField(default=0)
    comment_maintask = models.ForeignKey(MainTaskComment, related_name='files_maintask_comment', on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to = upload_path_files_maintask_comment)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"Id: {self.id}, File MainComment: {self.file}"

"""SubTaskComments model Limba"""

class SubTaskComment(models.Model):
    """Class SubTaskComment"""

    class Meta:
        db_table = 'subtask_comment'
    
    subtask = models.ForeignKey(SubTask, related_name='subtask_comment', on_delete=models.CASCADE, null=True)
    creator_comment = models.ForeignKey(User, related_name='creator_subcomment', on_delete=models.DO_NOTHING, null=True)
    comment = models.TextField(_('Комментарий'), max_length=100, default="")
    datetime = models.DateTimeField(auto_now_add=timezone.now)
    
    def __str__(self):
        return f"Подзадача: {self.subtask}, Дата создания: {self.datetime}."

"""SubTaskImageComments model Limba"""

class ImageSubTaskComment(models.Model):
    """Class SubImageComment"""
  
    class Meta:
        db_table = 'subimage_comment'

    comment_subtask = models.ForeignKey(SubTaskComment, related_name='subimage_comment', on_delete=models.CASCADE, null=True)
    image = models.ImageField(_('Фотография'), upload_to = upload_path_sub_comment, blank=True)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"Id: {self.id}, SubImageComment: {self.image}"

"""SubTaskFileComment model Limba"""

class FileSubTaskComment(models.Model):
    """Class FileSubTaskComment"""
  
    class Meta:
        db_table = 'files_subtask_comment'

    name_file = models.CharField(max_length = 50)
    size = models.IntegerField(default=0)
    comment_subtask = models.ForeignKey(SubTaskComment, related_name='files_subtask_comment', on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to = upload_path_files_subtask_comment)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"Id: {self.id}, File SubtaskComment: {self.file}"

"""PushNotifications model Limba"""

class PushNotification(models.Model):
    """Class PushNotification"""
  
    class Meta:
        db_table = 'push_notifications'

    title = models.CharField(_('Заголовок'), max_length=200, default="")
    body = models.CharField(_('Сообщение'), max_length=400, default="")
    data = models.CharField(_('Данные'), max_length=600, default="")
    type = models.DecimalField(_('Тип сообщения'), max_digits=1, decimal_places=0, default=0)
    is_active = models.BooleanField(default=True)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"Id: {self.id}, Title: {self.title}"

"""Files model file maintask"""

class UploadFileMainTask(models.Model):
    """Class UploadFileMainTask"""

    class Meta:
        db_table = 'maintask_files'

    task = models.ForeignKey(MainTask, related_name='maintask_file', on_delete=models.CASCADE, null=True)
    name_file = models.CharField(max_length = 50)
    size = models.IntegerField(default=0)
    file = models.FileField(upload_to = upload_path_files_maintask)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"Id: {self.id}, Name file: {self.name_file}"

"""Files model file subtask"""

class UploadFileSubTask(models.Model):
    """Class UploadFileSubTask"""

    class Meta:
        db_table = 'subtask_files'

    subtask = models.ForeignKey(SubTask, related_name='subtask_file', on_delete=models.CASCADE, null=True)
    name_file = models.CharField(max_length = 50)
    size = models.IntegerField(default=0)
    file = models.FileField(upload_to = upload_path_files_subtask)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"Id: {self.id}, Name file: {self.name_file}"

"""Files model file object"""

class UploadFileObject(models.Model):
    """Class UploadFileObject"""

    class Meta:
        db_table = 'object_files'

    object = models.ForeignKey(Object, related_name='object_file', on_delete=models.CASCADE, null=True)
    name_file = models.CharField(max_length = 50)
    size = models.IntegerField(default=0)
    file = models.FileField(upload_to = upload_path_files_to_object)
    datetime = models.DateTimeField(auto_now_add=timezone.now)
    
    def save(self, *args, **kwargs):
        super(UploadFileObject, self).save(*args, **kwargs)
        cur_path = self.file.path;
        if ("xls" in cur_path):
            thr = threading.Thread(target=convert_file_xls, args=(cur_path, ))
            thr.start()
        if ("doc" in cur_path):
            convert_file_doc(cur_path)

    def __str__(self):
        return f"Id: {self.id}, Name file: {self.name_file}"

@receiver(models.signals.post_delete, sender=ImageObject)
def post_delete_image_object(sender, instance, *args, **kwargs):
    if instance.image:
        _delete_file(instance.image.path)

@receiver(models.signals.post_delete, sender=ImageMain)
def post_delete_image_main(sender, instance, *args, **kwargs):
    if instance.image:
        _delete_file(instance.image.path)

@receiver(models.signals.post_delete, sender=ImageSubTask)
def post_delete_image_sub(sender, instance, *args, **kwargs):
    if instance.image:
        _delete_file(instance.image.path)

@receiver(models.signals.post_delete, sender=ImageMainTaskComment)
def post_delete_image_comment_maintask(sender, instance, *args, **kwargs):
    if instance.image:
        _delete_file(instance.image.path)

@receiver(models.signals.post_delete, sender=ImageSubTaskComment)
def post_delete_image_comment_subtask(sender, instance, *args, **kwargs):
    if instance.image:
        _delete_file(instance.image.path)

@receiver(models.signals.post_delete, sender=UploadFileObject)
def post_delete_file_object(sender, instance, *args, **kwargs):
    if instance.file:
        _delete_file(instance.file.path)

@receiver(models.signals.post_delete, sender=UploadFileMainTask)
def post_delete_file_maintask(sender, instance, *args, **kwargs):
    if instance.file:
        _delete_file(instance.file.path)

@receiver(models.signals.post_delete, sender=UploadFileSubTask)
def post_delete_file_subtask(sender, instance, *args, **kwargs):
    if instance.file:
        _delete_file(instance.file.path)

@receiver(models.signals.post_delete, sender=FileMainTaskComment)
def post_delete_file_maintask_comment(sender, instance, *args, **kwargs):
    if instance.file:
        _delete_file(instance.file.path)

@receiver(models.signals.post_delete, sender=FileSubTaskComment)
def post_delete_file_subtask_comment(sender, instance, *args, **kwargs):
    if instance.file:
        _delete_file(instance.file.path)
