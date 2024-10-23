from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model

class CustomRegisterSerializer(RegisterSerializer):
    user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, required=True)
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['user_type'] = self.validated_data.get('user_type')
        return data
    
    def save(self, request):
        user = super().save(request)
        user.user_type = self.validated_data.get('user_type')
        user.save()  # Değişiklikleri kaydet
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  # CustomUser kullanıyorsanız bu User modelinizi getirir
        fields = ['id', 'username']  # Sadece id ve username döndürecek