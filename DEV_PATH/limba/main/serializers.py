from django.db.models import fields
from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from django.contrib.auth import get_user_model
import datetime as dt
import json
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from urllib.parse import unquote
from django.utils import timezone
from .models import (
    Log,
    SubTaskComment, 
    SubTask, 
    Department, 
    ImageMain, 
    ImageSubTask, 
    MainTask, 
    MainTaskComment, 
    SubDepartmentObject, 
    Object,
    ImageObject, 
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

UserModel = get_user_model()

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    id = serializers.IntegerField()
    password = serializers.CharField(required=True)

class ImageObjectSerializer(serializers.ModelSerializer):
    """Class ImageObject Serializer"""

    class Meta:
        model = ImageObject
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'image_url': unquote(instance.image.url),
            'object': instance.object.id,
            'datetime': instance.datetime.strftime("%H:%M:%S %d.%m.%Y")
        }

class ImageMainSerializer(serializers.ModelSerializer):
    """Class ImageMain Serializer"""

    class Meta:
        model = ImageMain
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'image_url': unquote(instance.image.url),
            'task': instance.task.id,
            'datetime': instance.datetime.strftime("%H:%M:%S %d.%m.%Y")
        }

class ImageSubTaskSerializer(serializers.ModelSerializer):
    """Class ImageSubTask Serializer"""

    class Meta:
        model = ImageSubTask
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'image_url': unquote(instance.image.url),
            'subtask': instance.subtask.id,
            'datetime': instance.datetime.strftime("%H:%M:%S %d.%m.%Y")
        }

class ImageMainTaskCommentSerializer(serializers.ModelSerializer):
    """Class ImageMainTaskComment Serializer"""

    class Meta:
        model = ImageMainTaskComment
        fields = "__all__"
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'image_url': unquote(instance.image.url),
            'comment_maintask': instance.comment_maintask.id,
            'datetime': instance.datetime.strftime("%H:%M:%S %d.%m.%Y")
        }

class ImageSubTaskCommentSerializer(serializers.ModelSerializer):
    """Class ImageSubTaskComment Serializer"""

    class Meta:
        model = ImageSubTaskComment
        fields = "__all__"
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'image_url': unquote(instance.image.url),
            'comment_subtask': instance.comment_subtask.id,
            'datetime': instance.datetime.strftime("%H:%M:%S %d.%m.%Y")
        }

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)

    def create(self, validate_data):
        user = UserModel.objects.create_user(
            username = validate_data['username'],
            password = validate_data['password'],
            first_name = validate_data['first_name'],
            last_name = validate_data['last_name'],
            email = validate_data['email'],
            is_admin_company = validate_data['is_admin_company'],
            company = validate_data['company']
            # is_staff = validate_data['is_staff'],
            # is_superuser = validate_data['is_superuser'],
        )

        return user

    class Meta:
        model = UserModel
        fields = [
            'id', 
            'username', 
            'password', 
            'first_name', 
            'last_name', 
            'email',
            'company',
            'is_admin_company',
            # 'is_staff', 
            # 'is_superuser', 
        ]

        # write_only_fields = ('password',)

class UserInfoSerialiser(serializers.ModelSerializer):
    """Class UserInfo Serializer"""

    # position_worker = serializers.CharField(source='get_position_worker_display')

    class Meta:
        model = UserAdditionalInfo
        fields = '__all__'

class UploadFileObjectSerializer(serializers.ModelSerializer):
    """Class UploadFileObject Serializer"""

    # datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UploadFileObject
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name_file': instance.name_file,
            'file_url': unquote(instance.file.url),
            'object': instance.object.id,
            'datetime': instance.datetime.strftime("%H:%M:%S %d.%m.%Y")
        }

class ObjectSerializer(serializers.ModelSerializer):
    """Class Object Serializer"""

    user = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    connected_workers = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all(), many=True)
    object_img = ImageObjectSerializer(many = True, read_only=True)
    object_file = UploadFileObjectSerializer(many = True, read_only=True)

    class Meta:
        model = Object
        fields = '__all__'


class SubDepartmentObjectSerializer(serializers.ModelSerializer):
    """Class SubDepartmentObject Serializer"""

    user = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    creator = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    
    class Meta:
        model = SubDepartmentObject
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    """Class Department Serializer"""

    user_assign = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    creator = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    department = SubDepartmentObjectSerializer(many = True, read_only=True)
    user_assign_id = serializers.SerializerMethodField('user_assign_met')

    def user_assign_met(self, obj):
        try:
            return int(obj.user_assign.id)
        except Exception as ex:
            print(ex)
        return 999999
        


    class Meta:
        model = Department
        fields = ['id', 'user_assign', 'creator', 'department', 'fullname',
            'datetime', 'object_name', 'user_assign_id']

class SubTaskCustomSerializer(serializers.ModelSerializer):
    """Class SubTask Serializer"""

    executor_task = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    # creator_task = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    # connected_workers = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all(), many=True)
    # subtask_img = ImageSubTaskSerializer(many = True, read_only=True)
    datetime = serializers.DateTimeField(format='%H:%M:%S %d.%m.%Y')
    col_imgs = serializers.SerializerMethodField('number_imgs')
    col_comments = serializers.SerializerMethodField('number_comments')
    # datetime = serializers.DateTimeField(format='%H:%M:%S %d.%m.%Y')

    def number_imgs(self, obj):
        number = 0
        objs = ImageSubTask.objects.filter(subtask=obj.id)
        number += len(objs)
        objs_comments = SubTaskComment.objects.filter(subtask=obj.id)
        for obj_msg in objs_comments:
            number += len(ImageSubTaskComment.objects.filter(comment_subtask=obj_msg.id)) 
        return number
    
    def number_comments(self, obj):
        objs = SubTaskComment.objects.filter(subtask=obj.id)
        return len(objs)

    class Meta:
        model = SubTask
        fields = ['id', 'datetime', 'task_name', 'col_imgs', 'col_comments', 'is_show_executor',
        'executor_task', 'is_active']

class SubTaskCommentSerializer(serializers.ModelSerializer):
    """Class SubTaskComment Serializer"""

    creator_comment = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    subimage_comment = ImageSubTaskCommentSerializer(many = True, read_only=True)

    class Meta:
        model = SubTaskComment
        fields = '__all__'

class SubTaskSerializer(serializers.ModelSerializer):
    """Class SubTask Serializer"""

    executor_task = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    connected_workers = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all(), many=True)
    subtask_img = ImageSubTaskSerializer(many = True, read_only=True)
    subtask_comment = SubTaskCommentSerializer(many = True, read_only=True)
    # datetime = serializers.DateTimeField(format='%H:%M:%S %d.%m.%Y')
    creator_id = serializers.SerializerMethodField(method_name='id_creator')
    creator_name = serializers.SerializerMethodField(method_name='name_creator')
    executor_id = serializers.SerializerMethodField(method_name='id_executor')


    def id_executor(self, obj):
        try:
            return int(obj.executor_task.id)
        except Exception as ex:
            print(ex)
        return 999999
    
    def id_creator(self, obj):
        try:
            return int(obj.maintask.creator_task.id)
        except Exception as ex:
            print(ex)
        return 999999
    
    def name_creator(self, obj):
        try:
            return str(obj.maintask.creator_task.username)
        except Exception as ex:
            print(ex)
        return ''

    class Meta:
        model = SubTask
        fields = '__all__'

class MainTaskCustomSerializer(serializers.ModelSerializer):
    """Class MainTask Serializer"""

    creator_task = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    executor_task = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    connected_workers = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all(), many=True)
    # maintask_img = ImageMainSerializer(many = True, read_only=True)
    maintask = SubTaskCustomSerializer(many = True, read_only=True)
    col_imgs = serializers.SerializerMethodField('number_imgs')
    col_comments = serializers.SerializerMethodField('number_comments')
    datetime = serializers.DateTimeField(format='%H:%M:%S %d.%m.%Y')
    creator_id = serializers.SerializerMethodField(method_name='id_creator')

    def id_creator(self, obj):
        try:
            return int(obj.creator_task.id)
        except Exception as ex:
            print(ex)
        return 999999

    def number_imgs(self, obj):
        number = 0
        objs = ImageMain.objects.filter(task=obj.id)
        number += len(objs)
        objs_comments = MainTaskComment.objects.filter(task=obj.id)
        for obj_msg in objs_comments:
            number += len(ImageMainTaskComment.objects.filter(comment_maintask=obj_msg.id)) 
        return number
    
    def number_comments(self, obj):
        objs = MainTaskComment.objects.filter(task=obj.id)
        return len(objs)
    


    class Meta:
        model = MainTask
        fields = ['id', 'subdepartment_object', 'maintask', 'connected_workers', 'executor_task', 'creator_task',
        'task_name', 'col_imgs', 'col_comments', 'datetime', 'is_active', 'is_show_executor', 'creator_id']

class MainTaskCommentSerializer(serializers.ModelSerializer):
    """Class MainTaskComment Serializer"""

    creator_comment = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    mainimage_comment = ImageMainTaskCommentSerializer(many = True, read_only=True)

    class Meta:
        model = MainTaskComment
        fields = '__all__'

class MainTaskSerializer(serializers.ModelSerializer):
    """Class MainTask Serializer"""

    creator_task = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    executor_task = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    connected_workers = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all(), many=True)
    maintask_img = ImageMainSerializer(many = True, read_only=True)
    maintask_comment = MainTaskCommentSerializer(many = True, read_only=True)
    creator_id = serializers.SerializerMethodField(method_name='id_creator')
    executor_id = serializers.SerializerMethodField(method_name='id_executor')
    # maintask = SubTaskCustomSerializer(many = True, read_only=True)
    # datetime = serializers.DateTimeField(format='%H:%M:%S %d.%m.%Y')

    def id_creator(self, obj):
        try:
            return int(obj.creator_task.id)
        except Exception as ex:
            print(ex)
        return 999999

    def id_executor(self, obj):
        try:
            return int(obj.executor_task.id)
        except Exception as ex:
            print(ex)
        return 999999

    class Meta:
        model = MainTask
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['id'] = user.id
        token['company'] = user.company
        token['is_admin_company'] = user.is_admin_company
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['groups'] = self.user.groups.values_list('name', flat=True)
        data['id'] = self.user.id
        data['company'] = self.user.company
        data['is_admin_company'] = self.user.is_admin_company
        return data

class PushNotificationSerializer(serializers.ModelSerializer):
    """Class PushNotification Serializer"""

    class Meta:
        model = PushNotification
        fields = '__all__'

class PushNotificationUserSerializer(serializers.ModelSerializer):
    """Class PushNotificationUser Serializer"""

    datetime_custom = serializers.SerializerMethodField('date_custom')
    # datetime_custom = serializers.DateTimeField(format='%d %m %H:%M')

    def date_custom(self, obj):
        return str(timezone.localtime(obj.datetime).strftime(format='%d %m %H:%M'))
        

    class Meta:
        model = PushNotificationUser
        fields = '__all__'

class UploadFileMainTaskSerializer(serializers.ModelSerializer):
    """Class UploadFileMainTask Serializer"""

    class Meta:
        model = UploadFileMainTask
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name_file': instance.name_file,
            'file_url': unquote(instance.file.url),
            'task': instance.task.id,
            'datetime': instance.datetime.strftime("%H:%M:%S %d.%m.%Y")
        }

class UploadFileSubTaskSerializer(serializers.ModelSerializer):
    """Class UploadFileSubTask Serializer"""

    class Meta:
        model = UploadFileSubTask
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name_file': instance.name_file,
            'file_url': unquote(instance.file.url),
            'subtask': instance.subtask.id,
            'datetime': instance.datetime.strftime("%H:%M:%S %d.%m.%Y")
        }

class FileMainTaskCommentSerializer(serializers.ModelSerializer):
    """Class FileMainTaskComment Serializer"""

    class Meta:
        model = FileMainTaskComment
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name_file': instance.name_file,
            'file_url': unquote(instance.file.url),
            'comment_maintask': instance.comment_maintask.id,
            'datetime': instance.datetime.strftime("%H:%M:%S %d.%m.%Y")
        }

class FileSubTaskCommentSerializer(serializers.ModelSerializer):
    """Class FileSubTaskComment Serializer"""

    class Meta:
        model = FileSubTaskComment
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name_file': instance.name_file,
            'file_url': unquote(instance.file.url),
            'comment_subtask': instance.comment_subtask.id,
            'datetime': instance.datetime.strftime("%H:%M:%S %d.%m.%Y")
        }

class LogSerializer(serializers.ModelSerializer):
    """Class Log Serializer"""

    class Meta:
        model = Log
        fields = '__all__'