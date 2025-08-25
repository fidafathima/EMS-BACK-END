from rest_framework import serializers

from EMS.models import User, FormField, Form, FormSubmissionData, FormSubmission
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("Account is disabled")

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return {
            "user": {"id": user.id,
                    "username": user.username,
            },
            "access": access_token,
            "refresh": refresh_token,
        }


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=('username', 'email', 'password', 'password2')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'



class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ["id", "label", "field_type", "required", "order"]


class FormSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True)
    class Meta:
        model = Form
        fields = ["id", "name", "description", "fields", 'created_by']
        
    def create(self, validated_data):
        fields_data = validated_data.pop('fields')
        form = Form.objects.create(**validated_data)
        for field_data in fields_data:
            FormField.objects.create(form=form, **field_data)
        return form


class FormSubmissionDataSerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source='field.label', read_only=True)
    form = serializers.CharField(source='field.form.name', read_only=True)
    class Meta:
        model = FormSubmissionData
        fields = ["field", "value", "field_name", "form"]



class FormSubmissionSerializer(serializers.ModelSerializer):
    data = FormSubmissionDataSerializer(many=True)
    submitted_by = serializers.CharField(source="submitted_by.username", read_only=True)
    
    
    class Meta:
        model = FormSubmission
        fields = ["id", "form", "submitted_by", "submitted_at", "data"]
        
    def validate(self, validated_data):
        data_items = validated_data.get('data')
        form = validated_data.get('form')
        form = Form.objects.get(id=form.id)
        fields = form.fields.all()
        exclude = []
        for data in data_items:
            field = data.get('field')
            exclude.append(field.id)
            fields = form.fields.get(id=field.id)
            if not data.get('value') and fields.required:
                raise serializers.ValidationError(f'{field.label} is required')
        required_fields = form.fields.exclude(id__in=exclude).filter(required=True)
        if required_fields:
            for required_field in required_fields:
                raise serializers.ValidationError(f'{required_field.label} is required')
        return super().validate(validated_data)
    
    def create(self, validated_data):
        data_items = validated_data.pop('data')
        submission = FormSubmission.objects.create(**validated_data)
        for item in data_items:
            FormSubmissionData.objects.create(submission=submission, **item)
        return submission
    
    def update(self, instance, validated_data):
        data_items = validated_data.pop('data')
        submission = super().update(instance, validated_data)
        FormSubmissionData.objects.filter(submission=submission).delete()
        for item in data_items:
            FormSubmissionData.objects.create(submission=submission, **item)
        return submission
    


        