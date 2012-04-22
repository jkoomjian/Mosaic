from django.db import models
from django.contrib.auth.models import User

    
class Mosaic(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=256)
    photoset = models.ForeignKey('Photoset')  #quote class name b/c it hasn't been created yet
    tile_width = models.IntegerField()
    tile_height = models.IntegerField()

class Photoset(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=256)
    num_photos_to_get = models.IntegerField()
    search_query = models.CharField(max_length=256)
    latitude = models.CharField(max_length=256)
    longitude = models.CharField(max_length=256)
    #Many-to-Many relationship with images - only set this on one model
    images = models.ManyToManyField('Image')
    
    def __unicode__(self):
        return self.name
    
    def get_cover_img_id(self):
        if (len(self.images.all()) > 0):
            return self.images.all()[0].flickr_id
        else:
            return ''
    
class Image(models.Model):
    flickr_id = models.CharField(max_length=256)
    flickr_title = models.CharField(max_length=256)
    flickr_author = models.CharField(max_length=256)
    flickr_html_url = models.CharField(max_length=256)
#    photo_sets = models.ManyToManyField(Photoset, through=Photoset)