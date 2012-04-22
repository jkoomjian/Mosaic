from django.conf.urls import patterns, include, url

#all view paths start with mosaic_shake_app.views
urlpatterns = patterns('auth.views',
     url(r'^login/', 'login_view'),
     url(r'^logout/', 'logout_view'),
)

