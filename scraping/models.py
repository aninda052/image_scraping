from django.db import models
from PIL import Image


SMALL_IMAGE_WIDTH = 256
MEDIUM_IMAGE_WIDTH = 1024
LARGE_IMAGE_WIDTH = 2048



class ResizeImageMixin:
    def resize(self, imageField: models.ImageField, size:tuple, size_title='large'):
        source_image = Image.open(imageField.path)  # Catch original
        source_image = source_image.convert('RGB')
        source_image.thumbnail(size)  # Resize to size

        # Resize to desire size
        source_image.thumbnail(size, resample=Image.ANTIALIAS)

        # extracting original file name
        original_file_name = imageField.path.split('/')[-1]

        # create new file name with concating original file name and  desire size
        tmp_original_file_name = original_file_name.split(".")

        # create new file name without file extension
        new_file_name = f'{tmp_original_file_name[0]}_{size_title}'

        # if extension exist in original file, add extension in new file
        if len(tmp_original_file_name)>1:
            new_file_name = f'{new_file_name}.{tmp_original_file_name[1]}'

        # making new image file path
        new_file_path = imageField.path.replace(original_file_name, new_file_name)

        # storing new image file
        source_image.save(new_file_path, quality=100)


        return new_file_path

class ScrapedImage(models.Model, ResizeImageMixin):
    def image_path(self, filename):
        return f"images/{self.domain}/{filename}"

    image_original = models.ImageField(null=False, upload_to=image_path)
    image_small = models.ImageField(null=True, upload_to=image_path)
    image_medium = models.ImageField(null=True, upload_to=image_path)
    image_large = models.ImageField(null=True, upload_to=image_path)
    image_source = models.URLField(unique=True, null=False)
    scraped_url = models.URLField(null=False)
    domain = models.CharField(max_length=25)
    download_date = models.DateField(auto_now_add=True)
    original_image_dimension = models.CharField(max_length=10)

    class Meta:
        indexes = [
            models.Index(fields=['scraped_url']),
            models.Index(fields=['domain']),
        ]

    def __str__(self):
        return self.image_source

    def save(self, *args, **kwargs):

        if self.image_original:

            if self.image_original.width > SMALL_IMAGE_WIDTH:
                self.image_small = self.resize(self.image_original, (SMALL_IMAGE_WIDTH, SMALL_IMAGE_WIDTH), "small")
            if self.image_original.width > MEDIUM_IMAGE_WIDTH:
                self.image_medium = self.resize(self.image_original, (MEDIUM_IMAGE_WIDTH, MEDIUM_IMAGE_WIDTH), "medium")
            if self.image_original.width > LARGE_IMAGE_WIDTH:
                self.image_large = self.resize(self.image_original, (LARGE_IMAGE_WIDTH, LARGE_IMAGE_WIDTH), "large")

            self.original_image_dimension = f'{self.image_original.width}*{self.image_original.height}'

        super(ScrapedImage, self).save(*args, **kwargs)





