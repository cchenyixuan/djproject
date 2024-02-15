from django.shortcuts import render


def apphome(request):
    return render(request, 'SPHapp.html')


def voxels_1(request):
    return render(request, 'voxels_1.html')


def cursor_movement_callback(request):
    if request.method == 'POST':
        data = request.POST.get('data')
