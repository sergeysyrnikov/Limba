from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, render
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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
    ImageSubTaskComment
)
from .filtrers import (
    MainTaskCommentImageFilter,
    SubTaskCommentImageFilter,
    ObjectFilter,
    ObjectImageFilter, 
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
    ImageObjectSerializer,
    DepartmentSerializer,
    SubDepartmentObjectSerializer,
    MainTaskSerializer,
    SubTaskSerializer,
    MainTaskCommentSerializer,
    SubTaskCommentSerializer,
    ImageMainSerializer,
    ImageSubTaskSerializer,
    UserInfoSerialiser,
    MyTokenObtainPairSerializer,
    ImageMainTaskCommentSerializer,
    ImageSubTaskCommentSerializer
)

class UserView(ModelViewSet):
    """Class UserView"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # pagination_class = PaginationUsers

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        instance = response.data
        user = User.objects.get(id=instance['id'])
        user.is_active = False
        user.save()
        email = user.email
        mail_subject = 'Активируйте свой аккаунт в Limba.'
        code = 0
        try:
            code = request.data["code"]
        except Exception as ex:
            print(ex)
        message = render_to_string('main/home_limba.html',
        {
            'user': user,
            'code': code
        })
        email = EmailMessage(
            mail_subject, message, to=[email]
        )
        email.send()
        print(instance)
        return Response({'status': 'success', 'pk': instance['id']})
    
    # @action(detail=True, methods=['post'])
    # def set_active(self, request, pk=None):
    #     user = self.get_object()
    #     print("Lsdfldsfdsf")
    #     print(user)

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

class ImageObjectView(ModelViewSet):
    """Class ImageObjectView"""

    queryset = ImageObject.objects.all()
    serializer_class = ImageObjectSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = ObjectImageFilter
    # pagination_class = PaginationSubTaskComments

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

class ImageMainTaskCommentView(ModelViewSet):
    """Class ImageMainTaskCommentView"""

    queryset = ImageMainTaskComment.objects.all()
    serializer_class = ImageMainTaskCommentSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = MainTaskCommentImageFilter
    # pagination_class = PaginationSubTaskComments

class ImageSubTaskCommentView(ModelViewSet):
    """Class ImageSubTaskCommentView"""

    queryset = ImageSubTaskComment.objects.all()
    serializer_class = ImageSubTaskCommentSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = SubTaskCommentImageFilter
    # pagination_class = PaginationSubTaskComments

# def activate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User._default_manager.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return HttpResponse('Спасибо за подтверждение вашей почты. Вы можете войти в свой аккаунт!')
#     else:
#         return HttpResponse('Активация аккаунта завершилась неудачей!')

def home(request):
    return render(request, 'main/home_limba.html', {})