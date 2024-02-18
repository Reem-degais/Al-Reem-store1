from django.db import models

# Create your models here.
class Catecory(models.Model):
    catecory_name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    catecory_img = models.ImageField(upload_to='photoes/catecgories', blank=True)

    class Meta:
       verbose_name = 'category'
       verbose_name_plural = 'catecgories'
    def __str__(self):
        return self.catecory_name