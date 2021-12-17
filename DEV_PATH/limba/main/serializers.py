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
from .models import (
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

class DepartmentSerializer(serializers.ModelSerializer):
    """Class Department Serializer"""

    user_assign = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    creator = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())

    class Meta:
        model = Department
        fields = '__all__'

class SubDepartmentObjectSerializer(serializers.ModelSerializer):
    """Class SubDepartmentObject Serializer"""

    user = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    creator = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())

    class Meta:
        model = SubDepartmentObject
        fields = '__all__'

class MainTaskSerializer(serializers.ModelSerializer):
    """Class MainTask Serializer"""

    creator_task = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    executor_task = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    connected_workers = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all(), many=True)
    maintask_img = ImageMainSerializer(many = True, read_only=True)
    # datetime = serializers.DateTimeField(format='%H:%M:%S %d.%m.%Y')

    class Meta:
        model = MainTask
        fields = '__all__'

class SubTaskSerializer(serializers.ModelSerializer):
    """Class SubTask Serializer"""

    executor_task = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    connected_workers = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all(), many=True)
    subtask_img = ImageSubTaskSerializer(many = True, read_only=True)
    # datetime = serializers.DateTimeField(format='%H:%M:%S %d.%m.%Y')

    class Meta:
        model = SubTask
        fields = '__all__'

class MainTaskCommentSerializer(serializers.ModelSerializer):
    """Class MainTaskComment Serializer"""

    creator_comment = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    mainimage_comment = ImageMainTaskCommentSerializer(many = True, read_only=True)

    class Meta:
        model = MainTaskComment
        fields = '__all__'

class SubTaskCommentSerializer(serializers.ModelSerializer):
    """Class SubTaskComment Serializer"""

    creator_comment = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    subimage_comment = ImageSubTaskCommentSerializer(many = True, read_only=True)

    class Meta:
        model = SubTaskComment
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['id'] = user.id
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
        return data

class PushNotificationSerializer(serializers.ModelSerializer):
    """Class PushNotification Serializer"""

    class Meta:
        model = PushNotification
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