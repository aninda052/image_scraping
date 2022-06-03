from django.db import models
from scraping.mixin import ResizeImageMixin


# Defining multiple image size
SMALL_IMAGE_WIDTH = 256
MEDIUM_IMAGE_WIDTH = 1024
LARGE_IMAGE_WIDTH = 2048



class ScrapedImage(models.Model, ResizeImageMixin):

    # defining image storing path
    def image_path(self, filename):
        """
            every image will store in a subdirectory of the static/image directory
            subdirectory will create with domain name of that image
        """
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
        """
            Declaring scraped_url and domain filed as index filed
            As they are text filed and user can use them for filtering
            Making them as index filed will improve query performance
        """
        indexes = [
            models.Index(fields=['scraped_url']),
            models.Index(fields=['domain']),
        ]

    def __str__(self):
        return self.image_source

    def save(self, *args, **kwargs):
        """
            This custom save method will store multiple image
            with multiple size of original image
            before saving the object
        """

        if self.image_original:

            # downscaling image to smale size if original image is bigger than small size image
            if self.image_original.width > SMALL_IMAGE_WIDTH:
                self.image_small = self.resize_image(self.image_original, (SMALL_IMAGE_WIDTH, SMALL_IMAGE_WIDTH), "small")

            # downscaling image to medium size if original image is bigger than medium size image
            if self.image_original.width > MEDIUM_IMAGE_WIDTH:
                self.image_medium = self.resize_image(self.image_original, (MEDIUM_IMAGE_WIDTH, MEDIUM_IMAGE_WIDTH), "medium")

            # downscaling image to large size if original image is bigger than large size image
            if self.image_original.width > LARGE_IMAGE_WIDTH:
                self.image_large = self.resize_image(self.image_original, (LARGE_IMAGE_WIDTH, LARGE_IMAGE_WIDTH), "large")

            # assigning original_image_dimension value
            self.original_image_dimension = f'{self.image_original.width}*{self.image_original.height}'

        super(ScrapedImage, self).save(*args, **kwargs)





