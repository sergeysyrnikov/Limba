from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

class Object(models.Model):
    """Class BlogCategory"""
    
    class Meta:
        db_table = 'object'

    user = models.ForeignKey(User, related_name='user', on_delete=models.DO_NOTHING)
    code = models.DecimalField(_('Код объекта'), max_digits=3, decimal_places=0, unique=True, null=True) 
    shortname = models.CharField(_('Сокращённое имя объекта'), max_length=8, default='', unique=True) 
    fullname = models.CharField(_('Полное имя объекта'), max_length=30, default='')
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"{_('Имя объекта ')}{self.shortname}, {_('код ')}{self.code}."

class Departments(models.Model):
    """Class BlogCategory"""
    
    class Meta:
        db_table = 'departments'
    
    user_assign = models.ForeignKey(User, related_name='user', on_delete=models.NOTHING, null=True)
	object_name = models.ForeignKey(Object, related_name='object', on_delete=models.CASCADE)
    fullname = models.CharField(_('Полное имя отдела'), max_length=30, default='')
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"{_('Имя подобъекта ')}{self.shortname}, {_('код ')}{self.code}."

class SubDepartmentObjects(models.Model):
    """Class BlogCategory"""
    
    class Meta:
        db_table = 'subdepartment_objects'
        
	department = models.ForeignKey(Departments, related_name='department', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.NOTHING, null=True)
    fullname = models.CharField(_('Полное имя подобъекта'), max_length=30, default='')
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"{_('Имя подобъекта ')}{self.shortname}, {_('код ')}{self.code}."
  
class MainTask(models.Model):
    """Class Task"""

    class Meta:
        db_table = 'maintasks'

    subdepartment_object = models.ForeignKey(SubDepartmentObjects, related_name='department_object', on_delete=models.CASCADE)
    creator_task = models.ForeignKey(User, related_name='creator', on_delete=models.NOTHING, null=True)
    cols_subtasks = models.IntegerField(_('Колличество подзадач'), null=True, default=0)
    connected_workers = models.ManyToMany(User, related_name='workers')
    task_name = models.CharField(_('Заголовок'), max_length=30)
    date_finished = models.DateField(_('Дата окончания задачи'), default=datetime.now)
    executor_task = models.ForeignKey(User, related_name='creator', on_delete=models.NOTHING, null=True)
    about = models.TextField(_('Подробности'), max_length=200)
    location = models.CharField(_('Местоположение'), max_length=100)
    is_active = models.BooleanField(default=True)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"{self.title} из шифра \"{self.blog_category.name}\""

class SubTask(models.Model):
    """Class SubTask"""

    class Meta:
        db_table = 'subtasks'

    maintask = models.ForeignKey(MainTask, related_name='maintask', on_delete=models.CASCADE)
    connected_workers = models.ManyToMany(User, related_name='workers')
    task_name = models.CharField(_('Заголовок'), max_length=30)
    date_finished = models.DateField(_('Дата окончания задачи'), default=datetime.now)
    executor_task = models.ForeignKey(User, related_name='creator', on_delete=models.NOTHING, null=True)
    about = models.TextField(_('Подробности'), max_length=200)
    location = models.CharField(_('Местоположение'), max_length=100)
    is_active = models.BooleanField(default=True)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"{self.title} из шифра \"{self.blog_category.name}\""

class ImageMain(models.Model):
  """Class Image"""
  
  class Meta:
    db_table = 'image'
  
  task = models.ForeignKey(MainTask, related_name='maintask', on_delete=models.CASCADE)
  image = models.ImageField(_('Фотография'), upload_to='images/', null=True)
  datetime = models.DateTimeField(auto_now_add=timezone.now)
  
  def __str__(self):
    return self.image

class ImageSubTask(models.Model):
    """Class Image"""
  
    class Meta:
        db_table = 'image'

    task = models.ForeignKey(MainTask, related_name='task', on_delete=models.CASCADE)
    image = models.ImageField(_('Фотография'), upload_to='images/', null=True)
    datetime = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.image


    
#   проверить файл сеттингс в серегиной ветке