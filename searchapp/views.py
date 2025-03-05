from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import SearchQuery
from .serializers import SearchQuerySerializer
from .gemini import process_query
from .scraper import google_search
from .youtube_api import search_youtube
# from .linkedin_api import search_linkedin
from .news_api import get_news

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({'error': 'Please provide all required fields'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def get(self, request):
        return Response({"message": "This is the login API. Use POST to log in."}, status=status.HTTP_200_OK)
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# class LogoutView(APIView):
#     def post(self, request):
#         try:
#             refresh_token = request.data.get("refresh")
#             if not refresh_token:
#                 return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class SearchView(APIView):
    def post(self, request):
        serializer = SearchQuerySerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.save()
            
            # AI Response using LangChain
            ai_response = process_query(query.query_text)
            
            # Web Scraping and API Integrations
            google_results = google_search(query.query_text)
            youtube_results = search_youtube(query.query_text)
            # linkedin_results = search_linkedin(query.query_text)
            news_results = get_news(query.query_text) 

            return Response({
                "query": query.query_text,
                "ai_response": ai_response,
                "google_results": google_results,
                "youtube_results": youtube_results,
                # "linkedin_results": linkedin_results
                "news_results": news_results
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)