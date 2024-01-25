"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from my_store_app.views import CategoryView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user-auth/', include("user_app.urls")),
    path('catalog/', include("catalog.urls")),
    path('cart/', include("cart.urls")),
    path('details/', include("product_details.urls")),
    path('private-office/', include("private_office.urls")),
    path('order/', include("ordering.urls")),
    path('', CategoryView.as_view(), name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)