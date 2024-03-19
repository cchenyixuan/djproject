from django.contrib import admin
from django.urls import include, path
import sphapp.views as v
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("stop/", v.stop_calculations, name='stop'),
    path('', views.index, name=''),
    path('upload/', v.upload, name='upload_file'),
    path('compute/', v.compute_convexhull, name='compute_convexhull'),
    path('download/', v.download, name='download_file'),
    path('volume/', v.volume_cal, name='volume_calculation'),


    path('home/', v.apphome, name='apphome'),
    path('voxels_1/', v.voxels_1, name='voxels_1'),
    path('voxels_1/shaders/vertex.vert', v.get_vertex_src, name='vert'),
    path('voxels_1/shaders/fragment.frag', v.get_fragment_src, name='frag'),
    path('voxels_1/<str:filename>/', v.load_obj, name='loader'),

    path('convexhull/', v.convex_hull, name='convexhull'),
    path('convexhull/shaders/vertex.vert', v.get_vertex_src, name='vert'),
    path('convexhull/shaders/fragment.frag', v.get_fragment_src, name='frag'),
    path('convexhull/<str:filename>/', v.load_obj, name='loader'),
    path('convexhull/output/<str:filename>/', v.load_output, name="output_loader")




]
