import os
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import ImageSerializer
from .Utils.image_processor import generate_edges
from FileUpload.settings import MEDIA_ROOT
from django.http import HttpResponse
from ImageUpload.models import ImageRepo
from django.http import FileResponse


class ImageUploadView(generics.CreateAPIView):
    parser_class = (FileUploadParser,)
    serializer_class = ImageSerializer()

    def post(self, request, *args, **kwargs):
      file_serializer = ImageSerializer(data=request.data)

      if file_serializer.is_valid():
          file_serializer.save()
          data = file_serializer.data
          filename = data.get('image_file')
          r_data = request.data
          threshold_1 = r_data.get('t1')
          threshold_2 = r_data.get('t2')
          threshold1 = int(threshold_1) if threshold_1 else threshold_1
          threshold2 = int(threshold_2) if threshold_2 else threshold_2
          filename = filename.replace('/media/', '')
          if threshold_1 and threshold_2:
              processed_file = generate_edges(MEDIA_ROOT, filename, threshold1=threshold1, threshold2=threshold2)
          else:
              processed_file = generate_edges(MEDIA_ROOT, filename)
          ImageRepo.objects.filter(image_file=filename).update(processed_file=processed_file)
          saved_data = ImageRepo.objects.get(pk= data.get('id'))
          serialized_data = ImageSerializer(saved_data)
          return Response(serialized_data.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetImageView(generics.RetrieveAPIView):
    serializer_class = ImageSerializer()

    def get(self, request, *args, **kwargs):
      image_id = kwargs.get('pk', None)
      image_file = ImageRepo.objects.get(pk=image_id)
      img_path =  image_file.processed_file
      response = FileResponse(open(img_path.path, 'rb'), content_type="image/png")
      return response