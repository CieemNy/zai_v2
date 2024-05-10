from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("graphql",  csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('api-token-auth/', views.obtain_auth_token),
    path('admin/', admin.site.urls),
    path('filmy/', include('filmy.urls')),
]
