#Tell the admin interface about our app

from mosaic_shake_app.models import Image, Photoset, Mosaic
from django.contrib import admin

admin.site.register(Image)
admin.site.register(Photoset)
admin.site.register(Mosaic)