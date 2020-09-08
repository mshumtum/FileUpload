from rest_framework import serializers
from ImageUpload.models import ImageRepo


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageRepo
        fields = "__all__"
