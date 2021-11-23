from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    MainTaskCommentView, 
    SubTaskCommentView, 
    UserView, 
    ObjectView,
    ImageObjectView, 
    DepartmentView, 
    SubDepartmentObjectView, 
    MainTaskView, 
    SubTaskView,
    ImageMainView,
    ImageSubTaskView,
    UserInfoView,
    ImageMainTaskCommentView,
    ImageSubTaskCommentView,
    MyTokenObtainPairView,
    PushNotificationView,
    ChangePasswordView,
    home,
    code,
)

router = routers.DefaultRouter()
router.register('users', UserView)
router.register('users-info', UserInfoView)
router.register('objects', ObjectView)
router.register('object-images', ImageObjectView)
router.register('departments', DepartmentView)
router.register('subdepartments', SubDepartmentObjectView)
router.register('maintasks', MainTaskView)
router.register('subtasks', SubTaskView)
router.register('maintask-comments', MainTaskCommentView)
router.register('subtask-comments', SubTaskCommentView)
router.register('maintask-images', ImageMainView)
router.register('subtask-images', ImageSubTaskView)
router.register('maintask-comment-images', ImageMainTaskCommentView)
router.register('subtask-comment-images', ImageSubTaskCommentView)
router.register('push-notifications', PushNotificationView)

urlpatterns = [
    path('tokens/', MyTokenObtainPairView.as_view()),
    path('token-refresh/', TokenRefreshView.as_view()),
    path('reset-password/', ChangePasswordView.as_view()),
    # path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('home/', home, name="home"),
    path('code/', code, name="code"), 
    path('', include(router.urls))
]
