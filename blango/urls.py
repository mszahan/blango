import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
import blog.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", blog.views.index),
    path("post/<slug>/", blog.views.post_detail, name="blog-post-detail"),
    #url for ip address
    path("ip/", blog.views.get_ip),



]


# we want this to work only if the debug is true, mainly in development
#this will work only if the debug is true
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]


# from django.conf import settings
# print(f"Time zone: {settings.TIME_ZONE}")
