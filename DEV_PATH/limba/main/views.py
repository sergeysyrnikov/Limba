from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
import json
from django.forms.models import model_to_dict
from django.core import serializers
from rest_framework.decorators import action

# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
# from rest_framework.decorators import action
from django.shortcuts import render
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import (
    PushNotificationUser,
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
    UploadFileObject,
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
    UserFilter,
    PushNotificationFilter,
    PushNotificationUserFilter,
    ObjectFileFilter,
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
    PushNotificationUserSerializer,
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
    ImageSubTaskCommentSerializer,
    PushNotificationSerializer,
    ChangePasswordSerializer,
    UploadFileMainTaskSerializer,
    UploadFileSubTaskSerializer,
    UploadFileObjectSerializer,
    FileMainTaskCommentSerializer,
    FileSubTaskCommentSerializer,
)

class UserView(ModelViewSet):
    """Class UserView"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # filter_backends = (DjangoFilterBackend, )
    # filter_class = UserFilter
    permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationUsers

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        instance = response.data
        user = User.objects.get(id=instance['id'])
        user.is_active = True
        user.save()
        return Response({
            'status': 'success', 
            'id': instance['id'],
            'first_name': instance['first_name'],
            'last_name': instance['last_name']
        })
    
    # def get_permissions(self):
    #     if self.request.method in ['PUT', 'DELETE', 'POST']:
    #         return [permissions.IsAuthenticated()]
    #     return [permissions.]

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
    permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationUsersInfo

class ObjectView(ModelViewSet):
    """Class ObjectView"""

    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = ObjectFilter
    permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationObjects

class ImageObjectView(ModelViewSet):
    """Class ImageObjectView"""

    queryset = ImageObject.objects.all()
    serializer_class = ImageObjectSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = ObjectImageFilter
    permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationSubTaskComments

class DepartmentView(ModelViewSet):
    """Class DepartmentView"""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = DepartmentFilter
    permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationDepartments

class SubDepartmentObjectView(ModelViewSet):
    """Class SubDepartmentView"""

    queryset = SubDepartmentObject.objects.all()
    serializer_class = SubDepartmentObjectSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = SubDepartmentFilter
    permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationSubDepartments

class MainTaskView(ModelViewSet):
    """Class MainTaskView"""

    queryset = MainTask.objects.all()
    serializer_class = MainTaskSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = TaskFilter
    permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationMainTasks

class SubTaskView(ModelViewSet):
    """Class SubTaskView"""

    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = SubTaskFilter
    permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationSubTasks

class MainTaskCommentView(ModelViewSet):
    """Class MainTaskCommentView"""

    queryset = MainTaskComment.objects.all()
    serializer_class = MainTaskCommentSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = MainTaskCommentFilter
    permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationMainTaskComments

class SubTaskCommentView(ModelViewSet):
    """Class SubTaskCommentView"""

    queryset = SubTaskComment.objects.all()
    serializer_class = SubTaskCommentSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = SubTaskCommentFilter
    permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationSubTaskComments

class ImageMainView(ModelViewSet):
    """Class ImageMainView"""

    queryset = ImageMain.objects.all()
    serializer_class = ImageMainSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = MainTaskImageFilter
    permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationMainTaskImgs

class ImageSubTaskView(ModelViewSet):
    """Class ImageSubTaskView"""

    queryset = ImageSubTask.objects.all()
    serializer_class = ImageSubTaskSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = SubTaskImageFilter
    permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationSubTaskComments

class ImageMainTaskCommentView(ModelViewSet):
    """Class ImageMainTaskCommentView"""

    queryset = ImageMainTaskComment.objects.all()
    serializer_class = ImageMainTaskCommentSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = MainTaskCommentImageFilter
    permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationSubTaskComments

class ImageSubTaskCommentView(ModelViewSet):
    """Class ImageSubTaskCommentView"""

    queryset = ImageSubTaskComment.objects.all()
    serializer_class = ImageSubTaskCommentSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = SubTaskCommentImageFilter
    permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationSubTaskComments

class PushNotificationView(ModelViewSet):
    """Class PushNotificationView"""

    queryset = PushNotification.objects.all()
    serializer_class = PushNotificationSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = PushNotificationFilter
    permission_classes = (IsAuthenticated,)

    # @action(detail=True, methods=['post'])
    # def set_active(self, request, pk=None):
    #     user = self.get_object()
    #     print("Lsdfldsfdsf")
    #     print(user)
    

class PushNotificationUserView(ModelViewSet):
    """Class PushNotificationUserView"""

    queryset = PushNotificationUser.objects.all()
    serializer_class = PushNotificationUserSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = PushNotificationUserFilter
    permission_classes = (IsAuthenticated,)

class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsAuthenticated,)

        def update(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                # set_password also hashes the password that the user will get
                id = serializer.data.get("id")
                object = User.objects.get(pk=int(id))
                object.set_password(serializer.data.get("password"))
                object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UploadFileMainTaskView(ModelViewSet):
#     """Class UploadFileMainTaskView"""

#     queryset = UploadFileMainTask.objects.all()
#     serializer_class = UploadFileMainTaskSerializer
#     filter_backends = (DjangoFilterBackend, )
#     filter_class = MainTaskFileFilter
#     permission_classes = (IsAuthenticated,)

# class UploadFileSubTaskView(ModelViewSet):
#     """Class UploadFileSubTaskView"""

#     queryset = UploadFileSubTask.objects.all()
#     serializer_class = UploadFileSubTaskSerializer
#     filter_backends = (DjangoFilterBackend, )
#     filter_class = SubTaskFileFilter

class UploadFileObjectView(ModelViewSet):
    """Class UploadFileSubTaskView"""

    queryset = UploadFileObject.objects.all()
    serializer_class = UploadFileObjectSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = ObjectFileFilter
    permission_classes = (IsAuthenticated,)

# class UploadFileMaintaskCommentView(ModelViewSet):
#     """Class UploadFileMaintaskCommentView"""

#     queryset = FileMainTaskComment.objects.all()
#     serializer_class = FileMainTaskCommentSerializer
#     filter_backends = (DjangoFilterBackend, )
#     filter_class = MainTaskCommentFileFilter

# class UploadFileSubtaskCommentView(ModelViewSet):
#     """Class UploadFileSubtaskCommentView"""

#     queryset = FileSubTaskComment.objects.all()
#     serializer_class = FileSubTaskCommentSerializer
#     filter_backends = (DjangoFilterBackend, )
#     filter_class = SubTaskCommentFileFilter

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



@api_view(["POST"])
@csrf_exempt 
def code(request):
    try:
        if request.method == "POST":
            if request.data["code_check"] == "34ubitaV":
                code_reg = str(request.data["code"])
                email = request.data["email"]
                data = request.data["data"]
                message = render_to_string('main/home_limba.html',
                {
                    'email': email,
                    'code': code_reg,
                    'data': data
                })
                mail_subject = 'Активируйте свой аккаунт в Limba.'
                email = EmailMessage(
                    mail_subject, message, to=[email]
                )
                email.send() 
    except Exception as ex:
        print(ex)
    return HttpResponse("")

@api_view(["POST"])
@csrf_exempt 
def users(request):
    try:
        if request.method == "POST":
            code = request.data["code"]
            is_info = request.data["is_info"]
            print(code)
            if (code == "34ubitaV" and is_info):
                ser = [{ "email": el.username, "id": el.id, "first_name": el.first_name, "second_name": el.last_name } for el in User.objects.filter(email=request.data["email"])]
                return JsonResponse(ser, safe=False)
            else:
                if (code == "34ubitaV"):
                    ser = [{ "email": el.username, "id": el.id} for el in User.objects.all()]
                    return JsonResponse(ser, safe=False)
                else:
                    return HttpResponse("")
    except Exception as ex:
        print(ex)
    return HttpResponse("")

@api_view(["POST"])
@csrf_exempt 
def push(request):
    try:
        if request.method == "POST":
            code = request.data["code"]
            print(code)
            if (code == "34ubitaV"):
                PushNotification.objects.create(
                    title = request.data["title"],
                    body = request.data["body"],
                    data = request.data["data"],
                    type = request.data["type"],
                    token_fcm = request.data["token_fcm"],
                    type_system = request.data["type_system"]
                )
                print("Good!")
                return HttpResponse("")
            else:
                return HttpResponse("")
    except Exception as ex:
        print(ex)
    return HttpResponse("")

@api_view(["POST"])
@csrf_exempt 
def tokens(request):
    try:
        if request.method == "POST":
            code = request.data["code"]
            print(code)
            if (code == "34ubitaV"):
                ser = [{ "code_fcm": el.code_fcm, "type_system": el.type_system } for el in UserAdditionalInfo.objects.filter(user=request.data["id"])]
                return JsonResponse(ser, safe=False)
            else:
                return HttpResponse("")
    except Exception as ex:
        print(ex)
    return HttpResponse("")

@api_view(["POST"])
@csrf_exempt 
def number_task_new(request):
    try:
        if request.method == "POST":
            code = request.data["code"]
            # print(code)
            if (code == "34ubitaV"):
                user_id = request.data["user"],
                type_request = request.data["type"];
                if type_request == 0:
                    list = request.data["list_id"],
                    list = list[0]
                    objs = []
                    for el in list:
                        objs.append(Object.objects.get(id=el))
                    number_tasks = []
                    new_tasks = []
                    for obj in objs:
                        objs_task = MainTask.objects.filter(executor_task=user_id, is_active = True, object=obj.id)
                        objs_subtasks = SubTask.objects.filter(executor_task=user_id, is_active = True, object=obj.id)
                        objs_task_new = MainTask.objects.filter(executor_task=user_id, is_active = True, object=obj.id, is_show_executor=False)
                        if len(objs_task_new) > 0:
                            new_tasks.append(True)
                        else:
                            objs_subtask_new = SubTask.objects.filter(executor_task=user_id, is_active = True, object=obj.id, is_show_executor=False)
                            if len(objs_subtask_new) > 0:
                                new_tasks.append(True)
                            else:
                                new_tasks.append(False)
                        number_tasks.append(len(objs_task) + len(objs_subtasks))
                    ser = {"number_tasks": number_tasks, "new_tasks": new_tasks}
                    return JsonResponse(ser, safe=False)
                elif type_request == 1:
                    list = request.data["list_id"]
                    list_number_tasks = []
                    new_tasks = []
                    k = 0
                    for lst in list:
                        print("Checking!")
                        list_number_tasks.append([])
                        new_tasks.append([])
                        for el in lst:
                            print("Id " + str(el))
                            try:
                                subdep_obj = SubDepartmentObject.objects.get(id=el)
                                objs_task = MainTask.objects.filter(executor_task=user_id, is_active = True, subdepartment_object=subdep_obj)
                                objs_subtasks = SubTask.objects.filter(executor_task=user_id, is_active = True, subdepartment_object=subdep_obj)
                                objs_task_new = MainTask.objects.filter(executor_task=user_id, is_active = True, subdepartment_object=subdep_obj, is_show_executor=False)
                                if len(objs_task_new) > 0:
                                    new_tasks[k].append(True)
                                else:
                                    objs_subtask_new = SubTask.objects.filter(executor_task=user_id, is_active = True, subdepartment_object=subdep_obj, is_show_executor=False)
                                    if len(objs_subtask_new) > 0:
                                        new_tasks[k].append(True)
                                    else:
                                        new_tasks[k].append(False)
                                list_number_tasks[k].append(len(objs_task) + len(objs_subtasks))
                                
                            except:
                                list_number_tasks[k].append(0)
                                new_tasks[k].append(False)
                        k+=1
                    print(list_number_tasks)
                    print(new_tasks)
                    ser = {"number_tasks": list_number_tasks, "new_tasks": new_tasks}
                    return JsonResponse(ser, safe=False)
                else:
                    return HttpResponse("")
            else:
                return HttpResponse("")
    except Exception as ex:
        print(ex)
    return HttpResponse("")