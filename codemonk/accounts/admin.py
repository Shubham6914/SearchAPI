from django.contrib import admin
from .models import MyUser,Paragraph


@admin.register(MyUser)

class MyUserAdmin(admin.ModelAdmin):
   list_display = ['id','name','email','date_of_birth','created_at',
                   'modified_at','is_active','is_staff']

   
   
@admin.register(Paragraph)

class ParagraphAdmin(admin.ModelAdmin):
   list_display = ['id','user','text','created_at','modified_at']
   
   
