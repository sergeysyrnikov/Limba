from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework_simplejwt import token_blacklist
from .models import (
    Object, 
    ImageMain, 
    ImageSubTask, 
    MainTask, 
    MainTaskComment, 
    SubDepartmentObject, 
    Department, 
    SubTask, 
    SubTaskComment, 
    User,
    UserAdditionalInfo,
    ImageMainTaskComment,
    ImageSubTaskComment,
    PushNotification,
    PushNotificationUser,
    UploadFileMainTask,
    UploadFileSubTask,
    UploadFileObject,
    FileMainTaskComment,
    FileSubTaskComment,
)

# """Class User admin"""    

# @admin.register(User)
# class User(admin.ModelAdmin):
#     """Class User"""

class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):
    
    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)

admin.site.register(User, UserAdmin)

@admin.register(UserAdditionalInfo)
class UserInfoAdmin(admin.ModelAdmin):
    """Class UserInfoAdmin"""

    list_display = [f.name for f in UserAdditionalInfo._meta.fields]
    list_filter = ["id", "abbreviation", "position_worker", "type_user", "datetime", "user"]

"""Class Object admin"""  

@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    """Class ObjectAdmin"""

    list_display = [f.name for f in Object._meta.fields]
    list_filter = [f.name for f in Object._meta.fields]

"""Class MainTask admin"""    

@admin.register(MainTask)
class MainTask(admin.ModelAdmin):
    """Class MainTask"""

    list_display = [f.name for f in MainTask._meta.fields]
    list_filter = [f.name for f in MainTask._meta.fields]

"""Class SubTask admin"""    

@admin.register(SubTask)
class SubTask(admin.ModelAdmin):
    """Class SubTask"""

    list_display = [f.name for f in SubTask._meta.fields]
    list_filter = [f.name for f in SubTask._meta.fields]

"""Class Department admin"""    

@admin.register(Department)
class Department(admin.ModelAdmin):
    """Class Department"""

    list_display = [f.name for f in Department._meta.fields]
    list_filter = [f.name for f in Department._meta.fields]

"""Class SubDepartmentObject admin"""    

@admin.register(SubDepartmentObject)
class SubDepartmentObject(admin.ModelAdmin):
    """Class SubDepartmentObject"""

    list_display = [f.name for f in SubDepartmentObject._meta.fields]
    list_filter = [f.name for f in SubDepartmentObject._meta.fields]

"""Class ImageMain admin"""    

@admin.register(ImageMain)
class ImageMain(admin.ModelAdmin):
    """Class ImageMain"""

    list_display = ['task', 'image', 'datetime']
    list_filter = ['task', 'datetime']

"""Class ImageSubTask admin"""    

@admin.register(ImageSubTask)
class ImageSubTask(admin.ModelAdmin):
    """Class ImageSubTask"""

    list_display = ['subtask', 'image', 'datetime']
    list_filter = ['subtask', 'datetime']

"""Class ImageMainTaskComment admin"""    

@admin.register(ImageMainTaskComment)
class ImageMainTaskComment(admin.ModelAdmin):
    """Class ImageMainTaskComment"""

    list_display = [f.name for f in ImageMainTaskComment._meta.fields]
    list_filter = ['datetime']

"""Class ImageSubTaskComment admin"""    

@admin.register(ImageSubTaskComment)
class ImageSubTaskComment(admin.ModelAdmin):
    """Class ImageSubTaskComment"""

    list_display = [f.name for f in ImageSubTaskComment._meta.fields]
    list_filter = ['datetime']

"""Class MainTaskComment admin"""    

@admin.register(MainTaskComment)
class MainTaskComment(admin.ModelAdmin):
    """Class MainTaskComment"""

    list_display = [f.name for f in MainTaskComment._meta.fields]
    list_filter = [f.name for f in MainTaskComment._meta.fields]

"""Class SubTaskComment admin"""    

@admin.register(SubTaskComment)
class SubTaskComment(admin.ModelAdmin):
    """Class SubTaskComment"""

    list_display = [f.name for f in SubTaskComment._meta.fields]
    list_filter = [f.name for f in SubTaskComment._meta.fields]

@admin.register(PushNotification)
class PushNotification(admin.ModelAdmin):
    """Class PushNotification"""

    list_display = [f.name for f in PushNotification._meta.fields]
    list_filter = ['type', 'is_active', 'type_system', 'datetime']

@admin.register(PushNotificationUser)
class PushNotificationUser(admin.ModelAdmin):
    """Class PushNotification"""

    list_display = [f.name for f in PushNotificationUser._meta.fields]
    list_filter = ['user', 'event', 'datetime']

# @admin.register(FileSubTaskComment)
# class FileSubTaskComment(admin.ModelAdmin):
#     """Class FileSubTaskComment"""

#     list_display = [f.name for f in FileSubTaskComment._meta.fields]
#     list_filter = [f.name for f in FileSubTaskComment._meta.fields]

# @admin.register(FileMainTaskComment)
# class FileMainTaskComment(admin.ModelAdmin):
#     """Class FileSubTaskComment"""

#     list_display = [f.name for f in FileMainTaskComment._meta.fields]
#     list_filter = [f.name for f in FileMainTaskComment._meta.fields]

# """Class FileMainTask admin"""    

# @admin.register(UploadFileMainTask)
# class UploadFileMainTask(admin.ModelAdmin):
#     """Class UploadFileMainTask"""

#     list_display = [f.name for f in UploadFileMainTask._meta.fields]
#     list_filter = [f.name for f in UploadFileMainTask._meta.fields]


# """Class FileSubTask admin"""    

# @admin.register(UploadFileSubTask)
# class UploadFileSubTask(admin.ModelAdmin):
#     """Class UploadFileSubTask"""

#     list_display = [f.name for f in UploadFileSubTask._meta.fields]
#     list_filter = [f.name for f in UploadFileSubTask._meta.fields]

"""Class FileObject admin"""    

@admin.register(UploadFileObject)
class UploadFileObject(admin.ModelAdmin):
    """Class UploadFileObject"""

    list_display = [f.name for f in UploadFileObject._meta.fields]
    list_filter = [f.name for f in UploadFileObject._meta.fields]