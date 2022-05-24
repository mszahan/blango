import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
import blog.views
import blango_auth.views
# from the django registration view
from django_registration.backends.activation.views import RegistrationView
from blango_auth.forms import BlangoRegistrationForm



urlpatterns = [
    path('admin/', admin.site.urls),
    path("", blog.views.index),
    path("post/<slug>/", blog.views.post_detail, name="blog-post-detail"),
    #url for ip address
    path("ip/", blog.views.get_ip),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", blango_auth.views.profile, name="profile"),
    path(
    "accounts/register/",
    RegistrationView.as_view(form_class=BlangoRegistrationForm),
    name="django_registration_register",),
    # this is for the activation url
    path("accounts/", include("django_registration.backends.activation.urls")),







]


# we want this to work only if the debug is true, mainly in development
#this will work only if the debug is true
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]


# from django.conf import settings
# print(f"Time zone: {settings.TIME_ZONE}")
