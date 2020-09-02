from django.db import models
import short_url

# Create your models here.
class Urls(models.Model):
    short_id = models.SlugField(max_length=6, primary_key=True)
    httpurl = models.URLField(max_length=500)
    pub_date = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', default=True)

    def __str__(self):
        return self.httpurl


class ShortUrl(models.Model):
    url = models.URLField()
    short_url = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.url
