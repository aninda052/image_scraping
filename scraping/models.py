from django.db import models

# Create your models here.


class ScrapedImage(models.Model):
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
    image_dimension = models.CharField(max_length=10)

    def __str__(self):
        return self.image_source





