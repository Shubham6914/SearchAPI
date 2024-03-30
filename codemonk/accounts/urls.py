from django.urls import path
from .views import UserRegistration,UserLogin,UserProfile,Input_paragraph,SearchParagraph
urlpatterns = [
   path('UserRegister/',UserRegistration.as_view(),name='UserRegister'),
   path('login/', UserLogin.as_view(),name ='login'),
   path('profile/', UserProfile.as_view(),name ='Profile'),
   path('InputPara/', Input_paragraph.as_view(),name ='InputPara'),
   path('search/', SearchParagraph.as_view(),name ='search'),
]
