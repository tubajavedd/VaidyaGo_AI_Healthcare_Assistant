from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserDocument
from .serializers import UserDocumentSerializer
from .utils import generate_file_hash


class UploadDocumentAPIView(APIView):
    def post(self, request):
        uploaded_file = request.FILES.get("file")
        title = request.data.get("title")

        if not uploaded_file:
            return Response(
                {"error": "No file uploaded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        file_hash = generate_file_hash(uploaded_file)

        # check duplicate
        existing = UserDocument.objects.filter(file_hash=file_hash).first()
        if existing:
            return Response(
                {"message": "This file is already uploaded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        document = UserDocument.objects.create(
            user=request.user,
            title=title or uploaded_file.name,
            file=uploaded_file,
            file_hash=file_hash
        )

        serializer = UserDocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_201_CREATED)