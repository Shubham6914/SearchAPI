from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from.models import Paragraph,MyUser



# created serialzer for MyUser Model 
class MyUserSerializer(ModelSerializer):
   # we are writing this because we need to confirm password field in our registartion request
   password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
   class Meta:
      model = MyUser
      fields = ['id','name','email','date_of_birth','created_at','modified_at','password','password2']
      extra_kwargs  = {
         'password':{'write_only':True}
      }
      
   def validate(self, data):
      password1 = data.get('password')
      password2 = data.get('password2')
      if password1 != password2:
         raise serializers.ValidationError("password and confirm password does not match")
      return data
   
   def create(self,validated_data):
      # Remove password2 from validated_data
      validated_data.pop('password2',None)
      
      # create the user 
      user = MyUser.objects.create_user(**validated_data)
      return user
   
   
   
# created user UserProfileSerializer for fetching user details 
class UserProfileSerializer(ModelSerializer):
   class Meta:
      model = MyUser
      fields = ['id', 'name', 'email', 'date_of_birth', 'created_at', 'modified_at']
      
      
# created serailzer for Paragraph Model 
class ParagraphSerializer(ModelSerializer):
   class Meta:
      model = Paragraph
      fields = ['user','text']