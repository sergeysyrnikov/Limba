from django.db.models import fields
from django_filters import rest_framework as rest_filters, NumberFilter, CharFilter
from .models import (
    Object,
    ImageObject, 
    Department, 
    SubDepartmentObject, 
    MainTask, 
    SubTask, 
    MainTaskComment, 
    SubTaskComment, 
    ImageMain, 
    ImageSubTask,
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

class UserFilter(rest_filters.FilterSet):
    """Class UserFilter"""

    id = NumberFilter(field_name="id")
    user = NumberFilter(field_name="user")

    class Meta:
        model = UserAdditionalInfo
        fields = ["id", "user"]

class ObjectFilter(rest_filters.FilterSet):
    """Class ObjectFilter"""

    id = NumberFilter(field_name="id")
    code = NumberFilter(field_name="code")
    user = NumberFilter(field_name="user")
    connected_workers = NumberFilter(field_name="connected_workers")

    class Meta:
        model = Object
        fields = ['id', 'code', 'user', "connected_workers"]

class ObjectImageFilter(rest_filters.FilterSet):
    """Class ObjectImageFilter"""

    id = NumberFilter(field_name="id")
    object_id = NumberFilter(field_name="object_id")
    image = CharFilter(lookup_expr='iexact')


    class Meta:
        model = ImageObject
        fields = ['id', 'object_id']

class ObjectFileFilter(rest_filters.FilterSet):
    """Class ObjectFileFilter"""

    id = NumberFilter(field_name="id")
    object_id = NumberFilter(field_name="object_id")
    file = CharFilter(lookup_expr='iexact')


    class Meta:
        model = UploadFileObject
        fields = ['id', 'object_id']

class DepartmentFilter(rest_filters.FilterSet):
    """Class DepartmentFilter"""

    id = NumberFilter(field_name="id")
    object_name = NumberFilter(field_name="object_name")
    user_assign = NumberFilter(field_name="user_assign")
    creator = NumberFilter(field_name="creator")

    class Meta:
        model = Department
        fields = ['id', 'object_name', 'user_assign', 'creator']

class SubDepartmentFilter(rest_filters.FilterSet):
    """Class SubDepartmentFilter"""

    id = NumberFilter(field_name="id")
    department_id = NumberFilter(field_name="department_id")
    creator = NumberFilter(field_name="creator")

    class Meta:
        model = SubDepartmentObject
        fields = ['id', 'department_id', 'creator']

class TaskFilter(rest_filters.FilterSet):
    """Class TaskFilter"""

    id = NumberFilter(field_name="id")
    subdepartment_id = NumberFilter(field_name="subdepartment_object_id")
    connected_workers = NumberFilter(field_name="connected_workers")

    class Meta:
        model = MainTask
        fields = ['id', 'subdepartment_object_id', 'connected_workers']

class SubTaskFilter(rest_filters.FilterSet):
    """Class SubTaskFilter"""

    id = NumberFilter(field_name="id")
    maintask_id = NumberFilter(field_name="maintask_id")
    connected_workers = NumberFilter(field_name="connected_workers")

    class Meta:
        model = SubTask
        fields = ['id', 'maintask_id', "connected_workers"]

class MainTaskImageFilter(rest_filters.FilterSet):
    """Class MainTaskImageFilter"""

    id = NumberFilter(field_name="id")
    task_id = NumberFilter(field_name="task_id")
    image = CharFilter(lookup_expr='iexact')

    class Meta:
        model = ImageMain
        fields = ['id', 'task_id']

class MainTaskFileFilter(rest_filters.FilterSet):
    """Class MainTaskFileFilter"""

    id = NumberFilter(field_name="id")
    task_id = NumberFilter(field_name="task_id")
    file = CharFilter(lookup_expr='iexact')

    class Meta:
        model = UploadFileMainTask
        fields = ['id', 'task_id']

class SubTaskImageFilter(rest_filters.FilterSet):
    """Class SubTaskImageFilter"""

    id = NumberFilter(field_name="id")
    subtask_id = NumberFilter(field_name="subtask_id")
    image = CharFilter(lookup_expr='iexact')

    class Meta:
        model = ImageSubTask
        fields = ['id', 'subtask_id']

class SubTaskFileFilter(rest_filters.FilterSet):
    """Class SubTaskFileFilter"""

    id = NumberFilter(field_name="id")
    subtask_id = NumberFilter(field_name="subtask_id")
    file = CharFilter(lookup_expr='iexact')

    class Meta:
        model = UploadFileSubTask
        fields = ['id', 'subtask_id']

class MainTaskCommentFilter(rest_filters.FilterSet):
    """Class MainTaskCommentFilter"""

    id = NumberFilter(field_name="id")
    task_id = NumberFilter(field_name="task_id")

    class Meta:
        model = MainTaskComment
        fields = ['id', 'task_id']

class SubTaskCommentFilter(rest_filters.FilterSet):
    """Class SubTaskCommentFilter"""

    id = NumberFilter(field_name="id")
    subtask_id = NumberFilter(field_name="subtask_id")

    class Meta:
        model = SubTaskComment
        fields = ['id', 'subtask_id']

class MainTaskCommentImageFilter(rest_filters.FilterSet):
    """Class MainTaskCommentImageFilter"""

    id = NumberFilter(field_name="id")
    comment_maintask_id = NumberFilter(field_name="comment_maintask_id")
    image = CharFilter(lookup_expr='iexact')

    class Meta:
        model = ImageMainTaskComment
        fields = ['id', 'comment_maintask_id']

class MainTaskCommentFileFilter(rest_filters.FilterSet):
    """Class MainTaskCommentFileFilter"""

    id = NumberFilter(field_name="id")
    comment_maintask_id = NumberFilter(field_name="comment_maintask_id")
    file = CharFilter(lookup_expr='iexact')

    class Meta:
        model = FileMainTaskComment
        fields = ['id', 'comment_maintask_id']

class SubTaskCommentImageFilter(rest_filters.FilterSet):
    """Class SubTaskCommentImageFilter"""

    id = NumberFilter(field_name="id")
    comment_subtask_id = NumberFilter(field_name="comment_subtask_id")
    image = CharFilter(lookup_expr='iexact')

    class Meta:
        model = ImageSubTaskComment
        fields = ['id', 'comment_subtask_id']

class SubTaskCommentFileFilter(rest_filters.FilterSet):
    """Class SubTaskCommentFileFilter"""

    id = NumberFilter(field_name="id")
    comment_subtask_id = NumberFilter(field_name="comment_subtask_id")
    file = CharFilter(lookup_expr='iexact')

    class Meta:
        model = FileSubTaskComment
        fields = ['id', 'comment_subtask_id']

class PushNotificationFilter(rest_filters.FilterSet):
    """Class PushNotificationFilter"""

    id = NumberFilter(field_name="id")
    type = NumberFilter(field_name="type")

    class Meta:
        model = PushNotification
        fields = ['id', 'type']