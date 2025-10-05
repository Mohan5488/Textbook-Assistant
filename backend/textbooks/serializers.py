from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()
        
        
        if not user:
            raise serializers.ValidationError({'username': 'Invalid username'})

        if not check_password(password, user.password):
            raise serializers.ValidationError({'password': 'Invalid password'})
        print(user.username)
        print(check_password(password,user.password))

        return {'user': user}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
