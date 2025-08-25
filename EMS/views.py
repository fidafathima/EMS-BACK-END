
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


from EMS.models import User, Form, FormField, FormSubmissionData, FormSubmission
from EMS.serializer import (RegisterSerializer, LoginSerializer,
                             ProfileSerializer, FormSerializer, FormSubmissionDataSerializer, FormSubmissionSerializer,
                             FormFieldSerializer)
from .filters import FormFilter


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)



class Registration(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RegistrationUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        form = self.get_object()
        serializer = self.get_serializer(form, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    
class ProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        try:
            return User.objects.get(id=self.request.user.id)
        except User.DoesNotExist:
            raise NotFound()

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class FormCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormSerializer
    queryset = Form.objects.all()

    def post(self, request):
        data=request.data
        data['created_by'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FormListAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormSerializer

    def get_object(self):
        try:
            return Form.objects.get(id=self.kwargs['pk'])
        except Form.DoesNotExist:
            raise NotFound("Form not found")


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not old_password or not new_password or not confirm_password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "New passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"success": "Password changed successfully"}, status=status.HTTP_200_OK)


class FormSubmissionAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormSubmissionSerializer
    queryset = FormSubmission.objects.all()

    def post(self, request):
        data=request.data
        data['submitted_by'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class FormSubmissionListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormSubmissionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = FormFilter
    search_fields = ['form_name',]
    
    def get_queryset(self):
        return FormSubmission.objects.filter(form=self.kwargs['pk'])
    
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FormSubmissionUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormSubmissionSerializer
    
    
    def get_object(self):
        try:
            return FormSubmission.objects.get(id=self.kwargs['pk'])
        except FormSubmission.DoesNotExist:
            raise NotFound()

    def get(self, request, *args, **kwargs):
        form = self.get_object()
        serializer = self.get_serializer(form)
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        form = self.get_object()
        serializer = self.get_serializer(form, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    
    def delete(self, request, *args, **kwargs):
        form = self.get_object()
        FormSubmissionData.objects.filter(submission=form).delete
        form.delete()
        return Response("Deleted Successfully")
    