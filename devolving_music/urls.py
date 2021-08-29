from django.contrib import admin
from django.urls import path, re_path, include

from .views import react_index, auto_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(auto_views())),
    re_path(r'^.*$', react_index, name="react_index")
]
