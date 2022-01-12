from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    MainTaskCommentView,
    MainTaskView, 
    SubTaskCommentView,
    SubTaskCustomView, 
    UserView, 
    ObjectView,
    ImageObjectView, 
    DepartmentView, 
    SubDepartmentObjectView, 
    MainTaskCustomView, 
    SubTaskView,
    ImageMainView,
    ImageSubTaskView,
    UserInfoView,
    ImageMainTaskCommentView,
    ImageSubTaskCommentView,
    MyTokenObtainPairView,
    PushNotificationView,
    PushNotificationUserView,
    ChangePasswordView,
    # UploadFileMaintaskCommentView,
    UploadFileObjectView,
    # UploadFileSubTaskView,
    # UploadFileSubtaskCommentView,
    # UploadFileMainTaskView, 
    home,
    code,
    number_task_new,
    push,
    tokens,
    users,
)

router = routers.DefaultRouter()
router.register('users', UserView)
router.register('users-info', UserInfoView)
router.register('objects', ObjectView)
router.register('object-images', ImageObjectView)
router.register('departments', DepartmentView)
router.register('subdepartments', SubDepartmentObjectView)
router.register('maintasks-custom', MainTaskCustomView)
router.register('maintasks', MainTaskView)
router.register('subtasks', SubTaskView)
router.register('subtasks-custom', SubTaskCustomView)
router.register('maintask-comments', MainTaskCommentView)
router.register('subtask-comments', SubTaskCommentView)
router.register('maintask-images', ImageMainView)
router.register('subtask-images', ImageSubTaskView)
router.register('maintask-comment-images', ImageMainTaskCommentView)
router.register('subtask-comment-images', ImageSubTaskCommentView)
router.register('push-notifications', PushNotificationView)
router.register('push-notifications-user', PushNotificationUserView)
# router.register('maintask-files', UploadFileMainTaskView)
# router.register('subtask-files', UploadFileSubTaskView)
router.register('object-files', UploadFileObjectView)
# router.register('maintask-comment-files', UploadFileMaintaskCommentView)
# router.register('subtask-comment-files', UploadFileSubtaskCommentView)

urlpatterns = [
    path('tokens/', MyTokenObtainPairView.as_view()),
    path('token-refresh/', TokenRefreshView.as_view()),
    path('reset-password/', ChangePasswordView.as_view()),
    # path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('home/', home, name="home"),
    path('code/', code, name="code"), 
    path('users-code/', users, name="users"), 
    path('push-create/', push, name="push"), 
    path('number-tasks/', number_task_new, name="number_task_new"), 
    path('tokens-fcm/', tokens, name="tokens"), 
    path('', include(router.urls))
]
