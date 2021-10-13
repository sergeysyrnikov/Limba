from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
# from .managers import CustomUserManager

"""Path uploading main imgs"""

def upload_path_main(self, filename):
    return '/'.join(['imageMainTask',str(self.task.task_name), filename])

"""Path uploading sub imgs"""

def upload_path_sub(self, filename):
    return '/'.join(['imageSubTask',str(self.subtask.task_name), filename])

"""Object model Limba"""

class User(AbstractUser):
    """Class User"""

    def __str__(self):
        return f"{self.username}"

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
    code_fcm = models.CharField(_('Токен пользователя'), max_length=300, default="")
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"{_('Пользователь: ')}{self.user.username}."

class Object(models.Model):
    """Class Object"""
    
    class Meta:
        db_table = 'objects'

    user = models.ForeignKey(User, related_name='user_limba', on_delete=models.DO_NOTHING, null=True)
    code = models.DecimalField(_('Код объекта'), max_digits=3, decimal_places=0, unique=True, null=True) 
    shortname = models.CharField(_('Сокращённое имя объекта'), max_length=8, default='', unique=True) 
    fullname = models.CharField(_('Полное имя объекта'), max_length=15, default='')
    supervisor = models.CharField(_('Руководитель проекта'), max_length=30, default='')
    chief = models.CharField(_('Начальник участка'), max_length=30, default='')
    group_number = models.DecimalField(_('Номер проектной группы'), max_digits=5, decimal_places=0, unique=True, null=True) 
    date_finished = models.DateField(_('Дата сдачи объекта'), null=True, blank=True)
    date_start_document = models.DateField(_('Дата создания ТУ Электоснабжение'), null=True, blank=True)
    date_finished_document = models.DateField(_('Дата окончания ТУ Электоснабжение'), null=True, blank=True)
    connected_workers = models.ManyToManyField(User, related_name='workers_object')
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"{_('Имя объекта: ')}{self.shortname}, {_('код: ')}{self.code}."

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
    connected_workers = models.ManyToManyField(User, related_name='workers_main')
    task_name = models.CharField(_('Заголовок'), max_length=30)
    full_link = models.CharField(_('Путь до задачи'), max_length=150)
    date_finished = models.DateField(_('Дата окончания задачи'), null=True, blank=True)
    executor_task = models.ForeignKey(User, related_name='executor_task', on_delete=models.DO_NOTHING, null=True)
    about = models.TextField(_('Подробности'), max_length=200, default="")
    location = models.CharField(_('Местоположение'), max_length=100, default="")
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
    connected_workers = models.ManyToManyField(User, related_name='workers_sub')
    task_name = models.CharField(_('Заголовок'), max_length=30)
    full_link = models.CharField(_('Путь до задачи'), max_length=150)
    date_finished = models.DateField(_('Дата окончания задачи'), null=True, blank=True)
    executor_task = models.ForeignKey(User, related_name='executor', on_delete=models.DO_NOTHING, null=True)
    about = models.TextField(_('Подробности'), max_length=200, default="")
    location = models.CharField(_('Местоположение'), max_length=100, default="")
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
    image = models.ImageField(_('Фотография'), upload_to = upload_path_main, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=timezone.now)
    
    def __str__(self):
        return f"Задача: {self.task}, Дата создания {self.datetime}, Путь файлов: {self.image}"

"""SubTaskComments model Limba"""

class SubTaskComment(models.Model):
    """Class SubTaskComment"""

    class Meta:
        db_table = 'subtask_comment'
    
    subtask = models.ForeignKey(SubTask, related_name='subtask_comment', on_delete=models.CASCADE, null=True)
    creator_comment = models.ForeignKey(User, related_name='creator_subcomment', on_delete=models.DO_NOTHING, null=True)
    comment = models.TextField(_('Комментарий'), max_length=100, default="")
    image = models.ImageField(_('Фотография'), upload_to = upload_path_sub, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=timezone.now)
    
    def __str__(self):
        return f"Подзадача: {self.subtask}, Дата создания {self.datetime}, Путь файлов: {self.image}"


