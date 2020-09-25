from django.db import models

class ImageRepo(models.Model):
    image_file = models.ImageField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_file = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.image_file.name
