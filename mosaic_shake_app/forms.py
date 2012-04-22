from django import forms
from mosaic_shake_app.models import Photoset

#using widget_tweaks
class PhotosetForm(forms.Form):
    name = forms.CharField()
    num_photos_to_get = forms.IntegerField(min_value=2, max_value=100)
    search_query = forms.CharField()
    latitude = forms.CharField()
    longitude = forms.CharField()

class MosaicForm(forms.Form):
    #for now mosaic sizes are hard coded
    TILE_WIDTH_CHOICES = (
        (512, 512),
        (256, 256),
        (128, 128),
        (64, 64),
        (32, 32)
#        (16,16), #will kill the server
#        (8, 8)
#        (4, 4),
#        (2, 2),
    )
    TILE_HEIGHT_CHOICES = (
       (341, 341),
       (62, 62),
       (31, 31),
       (22, 22)
#       (11, 11),
#       (2, 2),
    )
    name = forms.CharField()
    photoset = forms.ModelChoiceField(queryset=Photoset.objects.all(), empty_label=None)
    tile_width = forms.ChoiceField(choices=TILE_WIDTH_CHOICES)
    tile_height = forms.ChoiceField(choices=TILE_HEIGHT_CHOICES)