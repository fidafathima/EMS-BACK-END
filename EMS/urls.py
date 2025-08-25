

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from EMS import views
from rest_framework_simplejwt.views import (TokenRefreshView,)


urlpatterns = [
    path('Login/',views.LoginView.as_view(),name='Login'),
    path('register/',views.Registration.as_view(),name='Register'),
    path('profile/', views.ProfileView.as_view()),
    path('form/', views.FormCreateAPIView.as_view()),
    path('form/<int:pk>', views.FormListAPIView.as_view()),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('form-submission/', views.FormSubmissionAPIView.as_view()),
    path('form-submission/<int:pk>', views.FormSubmissionListAPIView.as_view()),
    path('form-submission-data/<int:pk>', views.FormSubmissionUpdateAPIView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    

]