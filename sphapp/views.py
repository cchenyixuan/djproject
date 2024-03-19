from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from utils import camera
import pyrr
import numpy as np

cam = camera.Camera()


def apphome(request):
    return render(request, 'SPHapp.html')


def convex_hull(request):
    global cam
    if request.method == 'POST':
        return get_cursor_position(request)
    cam = camera.Camera()
    return render(request, 'convex_hull.html')


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
        # print([*cam.view.reshape((-1, ))])
        return JsonResponse({'view': [*cam.view.reshape((-1,))]})
    # return render(request, 'voxels_1.html')


def get_vertex_src(request):
    buffer = """"""
    with open("templates/shaders/vertex.vert", "r") as f:
        for row in f:
            buffer += row
        f.close()
    return JsonResponse({'data': buffer})


def get_fragment_src(request):
    buffer = """"""
    with open("templates/shaders/fragment.frag", "r") as f:
        for row in f:
            buffer += row
        f.close()
    return JsonResponse({'data': buffer})


def load_obj(request, filename):
    def search_data(data_values, data_type):
        import re
        compiled_re = {"v": re.compile(r"v ([0-9.-]*) ([0-9.-]*) ([0-9.-]*)", re.S),
                       "vt": re.compile(r"vt ([0-9.-]*) ([0-9.-]*)", re.S),
                       "vn": re.compile(r"vn ([0-9.-]*) ([0-9.-]*) ([0-9.-]*)", re.S),
                       "f": re.compile(r" ([0-9]*)/([0-9]*)/([0-9]*)", re.S)}
        find_number = compiled_re[data_type]
        data = re.findall(find_number, data_values)
        if data_type == "f":
            data = [int(item) - 1 for sub_data in data for item in sub_data]
        else:
            data = [float(item) for item in data[0]]
        return data

    indices = []
    vertices = []
    texture_uvs = []
    normals = []
    with open("utils/" + filename, "r", encoding="utf8") as f:
        for row in f.readlines():
            if row[:2] == "v ":
                vertices.append(search_data(row, "v"))
            if row[:2] == "vt":
                texture_uvs.append(search_data(row, "vt"))
            if row[:2] == "vn":
                normals.append(search_data(row, "vn"))
            if row[:2] == "f ":
                index = search_data(row, "f")
                indices.append([index[0], index[3], index[6]])

                for i in range(3):
                    vertices[index[i * 3]].extend(texture_uvs[index[i * 3 + 1]])
                    vertices[index[i * 3]].extend(normals[index[i * 3 + 2]])
        f.close()
    averaged_vertex = []
    for vertex in vertices:
        pos = vertex[:3]
        uv_normal = np.array([0, 0, 0, 0, 0], dtype=np.float32)
        uvnnn = [np.array(vertex[3 + 5 * j:8 + 5 * j]) for j in range((len(vertex) - 3) // 5)]
        for partial in uvnnn:
            uv_normal += partial / len(uvnnn)
        averaged_vertex.append([*pos, *uv_normal])

    vertices = averaged_vertex

    vertices = np.array(vertices)

    indices = [item for _ in indices for item in _]
    # print(vertices)

    return JsonResponse({'vertices': [*vertices.reshape((-1,))], 'indices': indices})


def load_output(request, filename):
    def search_data(data_values, data_type):
        import re
        compiled_re = {"v": re.compile(r"v ([0-9.-]*) ([0-9.-]*) ([0-9.-]*)", re.S),
                       "vt": re.compile(r"vt ([0-9.-]*) ([0-9.-]*)", re.S),
                       "vn": re.compile(r"vn ([0-9.-]*) ([0-9.-]*) ([0-9.-]*)", re.S),
                       "f": re.compile(r" ([0-9]*)/([0-9]*)/([0-9]*)", re.S)}
        find_number = compiled_re[data_type]
        data = re.findall(find_number, data_values)
        if data_type == "f":
            data = [int(item) - 1 for sub_data in data for item in sub_data]
        else:
            data = [float(item) for item in data[0]]
        return data

    indices = []
    vertices = []
    texture_uvs = []
    normals = []
    with open("utils/output/" + filename, "r", encoding="utf8") as f:
        for row in f.readlines():
            if row[:2] == "v ":
                vertices.append(search_data(row, "v"))
            if row[:2] == "vt":
                texture_uvs.append(search_data(row, "vt"))
            if row[:2] == "vn":
                normals.append(search_data(row, "vn"))
            if row[:2] == "f ":
                index = search_data(row, "f")
                indices.append([index[0], index[3], index[6]])

                for i in range(3):
                    vertices[index[i * 3]].extend(texture_uvs[index[i * 3 + 1]])
                    vertices[index[i * 3]].extend(normals[index[i * 3 + 2]])
        f.close()
    averaged_vertex = []
    for vertex in vertices:
        pos = vertex[:3]
        uv_normal = np.array([0, 0, 0, 0, 0], dtype=np.float32)
        uvnnn = [np.array(vertex[3 + 5 * j:8 + 5 * j]) for j in range((len(vertex) - 3) // 5)]
        for partial in uvnnn:
            uv_normal += partial / len(uvnnn)
        averaged_vertex.append([*pos, *uv_normal])

    vertices = averaged_vertex

    vertices = np.array(vertices)

    indices = [item for _ in indices for item in _]
    # print(vertices)

    return JsonResponse({'vertices': [*vertices.reshape((-1,))], 'indices': indices})


def upload(request):
    if request.method == 'POST':
        file = request.FILES['fileInput']
        if file:
            # print(file)
            # Process the uploaded file as needed
            with open(f"templates/cache/{file.name}", 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
                f.close()
            return JsonResponse({'success': True, 'name': file.name})
    return JsonResponse({'success': False, 'error': 'No file uploaded'})


def compute_convexhull(request):
    with open(r"C:\Users\cchen\PycharmProjects\djproject\utils\compute_flag.txt", 'w') as flag:
        flag.write("run")
        flag.close()
    if request.method == 'POST':
        fileName = request.POST['name'][1:-1]
        output_dir = os.path.join(os.getcwd(), "utils", "output")  # Use absolute path
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        import utils.quick_convex_hull as quick_hull
        import utils.half_edge_mesh as half_edge_mesh
        if fileName[-3:] == "stl":
            vertices, facets = half_edge_mesh.HalfEdgeMesh.load_stl(f"templates/cache/{fileName}")
        elif fileName[-3:] == "obj":
            vertices, facets = half_edge_mesh.HalfEdgeMesh.load_obj(f"templates/cache/{fileName}")

        quick_hull.QuickConvexHull(vertices)
        return JsonResponse({'success': True, 'count': len(os.listdir(output_dir))})

    return JsonResponse({'success': False, 'error': 'Cannot compute'})


def download(request):
    if request.method == 'POST':
        fileName = request.POST['final'][1:-1]
        outputName = request.POST['name'][1:-1]
        output_dir = os.path.join(os.getcwd(), "utils", "output", fileName)
        if os.path.exists(output_dir):
            with open(output_dir, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{outputName}"'
                return response
        else:
            return JsonResponse({'success': False, 'error': 'File not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


def stop_calculations(request):
    with open(r"C:\Users\cchen\PycharmProjects\djproject\utils\compute_flag.txt", 'w') as flag:
        flag.write("stop")
        flag.close()
    return JsonResponse({"success": True})


def volume_cal(request):
    if request.method == 'POST':
        input_file = request.POST['input'][1:-1]
        output_file = request.POST['output'][1:-1]
        in_dir = os.path.join(os.getcwd(), "templates", "cache", input_file)
        out_dir = os.path.join(os.getcwd(), "utils", "output", output_file)

        import utils.volume_calculation as v_cal
        if input_file[-3:] == "stl":
            vertices, faces = v_cal.read_stl_file(in_dir)
            in_volume = v_cal.calculate_volume_stl(vertices, faces)
        else:
            vertices, faces = v_cal.read_obj_file(in_dir)
            in_volume = v_cal.calculate_volume_obj(vertices, faces)

        vertices, faces = v_cal.read_obj_file(out_dir)
        out_volume = v_cal.calculate_volume_obj(vertices, faces)

        volume_change = out_volume / in_volume - 1

        return JsonResponse({'success': True, 'volume_change': volume_change})
    else:
        return JsonResponse({'success': False, 'error': 'Volume cannot be estimated'}, status=405)
