from django.contrib import admin
from django.urls import path, include
from interactions.views import get_drug_interactions


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('api/get_drug_interactions/', get_drug_interactions, name='get_drug_interactions'),
    
]
