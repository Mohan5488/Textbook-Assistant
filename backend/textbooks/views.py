from rest_framework.views import APIView, Response
from .serializers import  LoginSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils.timezone import now
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from textbooks.nodes.document_ingest import document_ingest_node

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            user.last_login = now()  
            user.save(update_fields=['last_login'])
            return Response({
                'message': 'Login successful',
                'username': user.username,
                'token': token.key,
                "user_id" : user.id
            }, status=200)
        return Response({'message': serializer.errors}, status=400)
    
    def get(self, request):
        objs = User.objects.all()
        serializer = UserSerializer(objs, many=True)
        return Response(serializer.data, status=200)

class DocumentParser(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file_obj = request.data.get('file')
        user_id = request.data.get("user_id")
        title = file_obj.name

        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not user_id:
            return Response({"error": "No user_id provided"}, status=status.HTTP_400_BAD_REQUEST)

        file_name = default_storage.save(file_obj.name, ContentFile(file_obj.read()))
        file_path = default_storage.path(file_name)

        print(f"Saved file at: {file_path}")
        print(file_name)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Invalid user_id"}, status=status.HTTP_400_BAD_REQUEST)

        state = {
            "file_path": file_path,
            "uploader_id": user.id,
            "title": title
        }
        import os
        try:
            result = document_ingest_node(state)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

        return Response({
            "doc_id": result.get("doc_id"),
            "topics": result.get("topics"),
            "status": result.get("status", "parsed")
        }, status=status.HTTP_201_CREATED)




