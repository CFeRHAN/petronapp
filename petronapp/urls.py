from django.contrib import admin
from django.urls import path, include ,re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


schema_view = get_schema_view(
   openapi.Info(
      title="Petronapp API",
      default_version='v1',
      description="Petronapp API Test",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="mabnaic@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include(('rest_framework.urls'))),
    # path('login/', LoginView.as_view(template_name='rest_framework/login.html'), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout')
    
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),

    path('flow_manager/', include(('flow_manager.urls', 'flow_manager'), namespace='flow_manager')),

    path('trader/', include(('trader.urls', 'trader'), namespace='trader')),    
    path('freight/', include(('freight.urls', 'frieght'), namespace='freight')),
    path('producer/', include(('producer.urls', 'producer'), namespace='producer')),

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

