from django.conf.urls import patterns, include, url

#all view paths start with mosaic_shake_app.views
urlpatterns = patterns('mosaic_shake_app.views',
     url(r'^gallery/(?P<user_id>\d+)/(?P<msc_id>\d+)', 'gallery'),
     url(r'^gallery/(?P<msc_id>\d+)', 'gallery'),
     url(r'^gallery/', 'gallery'),
     url(r'^gallery_next_json/(?P<user_id>\d+)/(?P<msc_id>\d+)', 'gallery_next_json'),
     url(r'^gallery_next_json/(?P<msc_id>\d+)', 'gallery_next_json'),
     url(r'^home/', 'home'),
     url(r'^new_photoset/', 'new_photoset'),
     url(r'^edit_photoset/(?P<ps_id>\d+)', 'edit_photoset'),
     url(r'^new_mosaic/', 'new_mosaic'),
)

