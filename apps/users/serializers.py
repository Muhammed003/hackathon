from rest_framework import serializers

from apps.users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    email = serializers.CharField(
        write_only=True
    )
    password = serializers.CharField(
        write_only=True
    )
    token = serializers.CharField(
        read_only=True
    )
    class Meta:
        model = CustomUser
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=8, write_only=True)
    username = serializers.CharField(write_only=True, max_length=250)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password_confirm')

    def validate(self, attrs):

        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")

        if len(password) < 8 or len(password_confirm) < 8:
            raise serializers.ValidationError("Password is invalid")

        if sum(c.isalpha() for c in password) < 1:
            raise serializers.ValidationError("The password must contain at least 1 letter")

        if sum(c.isdigit() for c in password) < 1:
            raise serializers.ValidationError("The password must contain at least 1 number")


        if password != password_confirm:
            raise serializers.ValidationError("Password do not match")

        return attrs

    def create(self, validate_data):
        return CustomUser.objects.create_user(**validate_data)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs:dict):
        email = attrs.get("email")
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Account with this email have not found")
        return attrs


class ResetPasswordSerializer(serializers.ModelSerializer):
    activate_code = serializers.CharField(required=True)
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('activate_code', 'password', 'password_confirm')

    def validate(self, attrs):

        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")

        if len(password) < 8 or len(password_confirm) < 8:
            raise serializers.ValidationError("Password is invalid")

        if sum(c.isalpha() for c in password) < 1:
            raise serializers.ValidationError("The password must contain at least 1 letter")

        if sum(c.isdigit() for c in password) < 1:
            raise serializers.ValidationError("The password must contain at least 1 number")


        if password != password_confirm:
            raise serializers.ValidationError("Password do not match")

        return attrs