"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from arosaje import views
from arosaje.views import (PlantsViewSet, PostsViewSet, KeepingViewSet, SpeciesViewSet, 
                           CurrentUserView, ConsentmentsViewSet) 

apiRouter = routers.DefaultRouter()
apiRouter.register(r'users', views.UserViewSet)
apiRouter.register(r'groups', views.GroupViewSet)
apiRouter.register(r'plants', PlantsViewSet)
apiRouter.register(r'posts', PostsViewSet)
apiRouter.register(r'keeping', KeepingViewSet)
apiRouter.register(r'species', SpeciesViewSet)
apiRouter.register(r'consentments', ConsentmentsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(apiRouter.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/me/', CurrentUserView.as_view(), name='me'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
