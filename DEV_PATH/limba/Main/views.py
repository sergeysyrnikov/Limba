from rest_framework.viewsets import ModelViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
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
from .filtrers import (
    ObjectFilter, 
    DepartmentFilter, 
    SubDepartmentFilter, 
    TaskFilter, 
    SubTaskFilter,
    MainTaskImageFilter,
    SubTaskImageFilter,
    MainTaskCommentFilter,
    SubTaskCommentFilter,
    UserFilter
)
from .service import (
    PaginationUsers,
    PaginationObjects, 
    PaginationDepartments, 
    PaginationSubDepartments, 
    PaginationMainTasks, 
    PaginationSubTasks, 
    PaginationMainTaskImgs,
    PaginationSubTaskImgs,
    PaginationMainTaskComments,
    PaginationSubTaskComments,
    PaginationUsersInfo    
)
from .serializers import (
    UserSerializer,
    ObjectSerializer,
    DepartmentSerializer,
    SubDepartmentObjectSerializer,
    MainTaskSerializer,
    SubTaskSerializer,
    MainTaskCommentSerializer,
    SubTaskCommentSerializer,
    ImageMainSerializer,
    ImageSubTaskSerializer,
    UserInfoSerialiser,
    MyTokenObtainPairSerializer
)

class UserView(ModelViewSet):
    """Class UserView"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # pagination_class = PaginationUsers

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserInfoView(ModelViewSet):
    """Class UserInfoView"""

    queryset = UserAdditionalInfo.objects.all()
    serializer_class = UserInfoSerialiser
    filter_backends = (DjangoFilterBackend, )
    filter_class = UserFilter
    # pagination_class = PaginationUsersInfo

class ObjectView(ModelViewSet):
    """Class ObjectView"""

    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = ObjectFilter
    # pagination_class = PaginationObjects

class DepartmentView(ModelViewSet):
    """Class DepartmentView"""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = DepartmentFilter
    # pagination_class = PaginationDepartments

class SubDepartmentObjectView(ModelViewSet):
    """Class SubDepartmentView"""

    queryset = SubDepartmentObject.objects.all()
    serializer_class = SubDepartmentObjectSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = SubDepartmentFilter
    # pagination_class = PaginationSubDepartments

class MainTaskView(ModelViewSet):
    """Class MainTaskView"""

    queryset = MainTask.objects.all()
    serializer_class = MainTaskSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = TaskFilter
    # pagination_class = PaginationMainTasks

class SubTaskView(ModelViewSet):
    """Class SubTaskView"""

    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = SubTaskFilter
    # pagination_class = PaginationSubTasks

class MainTaskCommentView(ModelViewSet):
    """Class MainTaskCommentView"""

    queryset = MainTaskComment.objects.all()
    serializer_class = MainTaskCommentSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = MainTaskCommentFilter
    # pagination_class = PaginationMainTaskComments

class SubTaskCommentView(ModelViewSet):
    """Class SubTaskCommentView"""

    queryset = SubTaskComment.objects.all()
    serializer_class = SubTaskCommentSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = SubTaskCommentFilter
    # pagination_class = PaginationSubTaskComments

class ImageMainView(ModelViewSet):
    """Class ImageMainView"""

    queryset = ImageMain.objects.all()
    serializer_class = ImageMainSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = MainTaskImageFilter
    # pagination_class = PaginationMainTaskImgs

class ImageSubTaskView(ModelViewSet):
    """Class ImageSubTaskView"""

    queryset = ImageSubTask.objects.all()
    serializer_class = ImageSubTaskSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = SubTaskImageFilter
    # pagination_class = PaginationSubTaskComments


    # action_to_serializer = {
    #    "retrieve": BlogCategoryDetailSerializer,
    # }

    # def get_serializer_class(self):
    #     return self.action_to_serializer.get(
    #         self.action,
    #         self.serializer_class
    #     )

# class ContentPostView(ModelViewSet):
#     queryset = ContentPost.objects.all()
#     serializer_class = ContentPostSerializer

#     action_to_serializer = {
#         "list": ContentPostListRetrieveSerializer,
#         "retrieve": ContentPostListRetrieveSerializer,
#     }

#     def get_serializer_class(self):
#         return self.action_to_serializer.get(
#             self.action,
#             self.serializer_class
#         )

