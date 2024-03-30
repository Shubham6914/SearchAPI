from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import MyUserSerializer,ParagraphSerializer,UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import MyUser, Paragraph
import re # for performing pattern matching and search operations within strings.


# Generate Token manually 
def get_tokens_for_user(user):
   refresh = RefreshToken.for_user(user)
   return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
   }



# created view for registering user 
class UserRegistration(APIView):
   def post(self,request,format=None):
      serializer = MyUserSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
         user = serializer.save()
         token = get_tokens_for_user(user)
         return Response({
            "token":token,
            "Message":"Registration Succesfull",},
            status=status.HTTP_201_CREATED)
      else:
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
      



# created view for logging user 
class UserLogin(APIView):
   def post(self,request,format=None):
      # Extract username and password from the request
      email = request.data.get('email')
      password = request.data.get('password')
      
      # authenticate user 
      user  = authenticate(email=email,password=password)
      if user is not None:
         token = get_tokens_for_user(user)
         return Response({
            "Token" : token,
            "Message":"Login Succesfully"},
            status=status.HTTP_200_OK)
      else:
         if not email:
            return Response(data={"email":"This Field is Required"})
         elif not password:
            return Response(data={"password":"This Field is Required"})
      return Response(data={"errors":{"non_field_errors":['Invalid Login Credentials']}},status=status.HTTP_401_UNAUTHORIZED)
      



# created UserProfile view to see current  user information
class UserProfile(APIView):
   permission_classes = [IsAuthenticated]
   def get(self, request, format=None):
        # Retrieve the current user's profile details
        user_profile_serializer = UserProfileSerializer(request.user)

        # Retrieve the paragraphs written by the current user
        paragraphs = Paragraph.objects.filter(user=request.user)
        paragraph_serializer = ParagraphSerializer(paragraphs, many=True)

        # Combine the user profile data and the paragraphs data
        response_data = {
            "user_profile": user_profile_serializer.data,
            "paragraphs": paragraph_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)



#  function to handle input given by user 
class Input_paragraph(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # Create a mutable copy of the request data
        mutable_data = request.data.copy()
        
        # Retrieve the user object based on the provided email address
        email = mutable_data.get('user')
        user = MyUser.objects.filter(email=email).first()
        
        if user:
            # Modify the request data to set the user's primary key as the value for the 'user' field
            mutable_data['user'] = user.id
            
            # Create the serializer instance with modified data
            serializer = ParagraphSerializer(data=mutable_data)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"Message": "Paragraph submitted successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User with the provided email address does not exist."}, status=status.HTTP_400_BAD_REQUEST)

class SearchParagraph(APIView):
    def post(self, request, format=None):
        # Get the email address and word to search for from the request data
        email = request.data.get('email', '')
        word_to_search = request.data.get('word', '')

        # Check if email and word are provided
        if not email:
            return Response({"error": "Please provide an email address."}, status=status.HTTP_400_BAD_REQUEST)

        if not word_to_search:
            return Response({"error": "Please provide a word to search for."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve all paragraphs associated with the provided email address
        paragraphs = Paragraph.objects.filter(user__email=email)

        if not paragraphs:
            return Response({"error": "No paragraphs found for the provided email address."}, status=status.HTTP_404_NOT_FOUND)

        # Search for the word in each paragraph
        indexed_paragraphs = {}
        for paragraph in paragraphs:
            paragraph_text = paragraph.text.split('\n\n')  # Split paragraphs based on '\n\n' delimiter
            for index, para_text in enumerate(paragraph_text, start=1):
                words = re.findall(r'\b\w+\b', para_text.lower())  # Use regex to match words
                if word_to_search.lower() in words:
                    indexed_paragraphs[(paragraph.id, index)] = para_text

        # Return the top 10 paragraphs where the word is present
        top_10_paragraphs = list(indexed_paragraphs.values())[:10]

        return Response({"top_paragraphs": top_10_paragraphs}, status=status.HTTP_200_OK)
