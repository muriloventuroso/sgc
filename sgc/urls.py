"""sgc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.views import logout_then_login
from django.conf import settings
import sgc.views


urlpatterns = i18n_patterns(
    path('login/', sgc.views.login, {}, 'login'),
    path('logout/', logout_then_login, {'login_url': '/login/'}, 'logout'),
    path('congregations/', include('congregations.urls')),
    path('meetings/', include('meetings.urls')),
    path('', sgc.views.home, {}, 'home')
)
if settings.ADMIN_ENABLED:
    urlpatterns += i18n_patterns(
        path('admin/', admin.site.urls)
    )

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += i18n_patterns(
        path('rosetta/', include('rosetta.urls'))
    )
