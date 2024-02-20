from django.http import JsonResponse
from django.shortcuts import render
from utils import camera
import pyrr
import numpy as np

cam = camera.Camera()

def apphome(request):
    return render(request, 'SPHapp.html')


def voxels_1(request):
    global cam

    if request.method == 'POST':
        return get_cursor_position(request)
    cam = camera.Camera()
    return render(request, 'voxels_1.html')


def get_cursor_position(request):
    global cam
    if request.method == 'POST':
        x = request.POST.get('pos_x')
        y = request.POST.get('pos_y')
        flag = request.POST.get('flag')
        # Process x and y as needed
        # print(x, y, flag)
        cam(pyrr.Vector3((x, y, 0.0), dtype=np.float32), flag)
        # print(cam(pyrr.Vector3((x, y, 0.0), dtype=np.float32), flag))
        return JsonResponse({'view': [*cam.view.reshape((-1, ))]})
    # return render(request, 'voxels_1.html')

