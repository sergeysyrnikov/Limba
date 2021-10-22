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
    User,
    UserAdditionalInfo
)

UserModel = get_user_model()

class ImageMainSerializer(serializers.ModelSerializer):
    """Class ImageMain Serializer"""

    class Meta:
        model = ImageMain
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'image': self.context['request'].build_absolute_uri(instance.image.url),
            'image_url': unquote(instance.image.url),
            'task': instance.task.id,
            'datetime': instance.datetime
        }

class ImageSubTaskSerializer(serializers.ModelSerializer):
    """Class ImageSubTask Serializer"""

    class Meta:
        model = ImageSubTask
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'image': self.context['request'].build_absolute_uri(instance.image.url),
            'image_url': unquote(instance.image.url),
            'subtask': instance.task.id,
            'datetime': instance.datetime
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

class ObjectSerializer(serializers.ModelSerializer):
    """Class Object Serializer"""

    user = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    connected_workers = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all(), many=True)
    
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

    class Meta:
        model = MainTask
        fields = '__all__'

class SubTaskSerializer(serializers.ModelSerializer):
    """Class SubTask Serializer"""

    executor_task = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())
    connected_workers = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all(), many=True)
    subtask_img = ImageSubTaskSerializer(many = True, read_only=True)

    class Meta:
        model = SubTask
        fields = '__all__'

class MainTaskCommentSerializer(serializers.ModelSerializer):
    """Class MainTaskComment Serializer"""

    creator_comment = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())

    class Meta:
        model = MainTaskComment
        fields = '__all__'

class SubTaskCommentSerializer(serializers.ModelSerializer):
    """Class SubTaskComment Serializer"""

    creator_comment = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset = User.objects.all())

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

# class ObjectDetailSerializer(serializers.ModelSerializer):
    
#     posts = serializers.SerializerMethodField()

#     class Meta:
#         model = Object
#         fields = '__all__'

#     @staticmethod
#     def get_posts(obj):
#         return ContentPostSerializer(ContentPost.objects.filter(blog_category=obj), many=True).data

# class ContentPostSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = ContentPost
#         fields = '__all__'

# class ContentPostListRetrieveSerializer(serializers.ModelSerializer):
    
#     blog_category = ObjectSerializer()

#     class Meta:
#         model = ContentPost
#         fields = '__all__'
