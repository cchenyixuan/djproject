from django.urls import path
from .views import apphome, voxels_1

urlpatterns = [
    path('SPHhome/', apphome, name='apphome'),
    path('voxels_1/', voxels_1, name='voxels_1')

]