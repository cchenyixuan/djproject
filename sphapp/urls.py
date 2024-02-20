from django.urls import path
from .views import apphome, voxels_1, get_cursor_position

urlpatterns = [
    path('SPHhome/', apphome, name='apphome'),
    path('voxels_1/', voxels_1, name='voxels_1'),

]
