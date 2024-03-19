import numpy as np


def calculate_volume_obj(vertices, faces):
    volume = 0
    for face in faces:
        p1 = vertices[face[0] - 1]
        p2 = vertices[face[1] - 1]
        p3 = vertices[face[2] - 1]
        volume += np.dot(p1, np.cross(p2, p3))
    volume /= 6.0
    return abs(volume)


def calculate_volume_stl(vertices, faces):
    volume = 0
    for face in faces:
        p1 = vertices[face[0]]
        p2 = vertices[face[1]]
        p3 = vertices[face[2]]
        volume += np.dot(p1, np.cross(p2, p3))
    volume /= 6.0
    return abs(volume)


def read_obj_file(filename):
    vertices = []
    faces = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = list(map(float, line.split()[1:]))
                vertices.append(vertex)
            elif line.startswith('f '):
                face = [int(x.split('/')[0]) for x in line.split()[1:]]
                faces.append(face)
    return np.array(vertices), np.array(faces)


def read_stl_file(filename):
    vertices = []
    faces = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) > 0 and parts[0] == 'vertex':
                vertex = list(map(float, parts[1:]))
                vertices.append(vertex)
            elif len(parts) > 0 and parts[0] == 'endfacet':
                if len(vertices) >= 3:
                    faces.append([len(vertices)-3, len(vertices)-2, len(vertices)-1])
    return np.array(vertices), np.array(faces)


if __name__ == "__main__":
    file1 = r"../test_cube.obj"
    vertices, faces = read_obj_file(file1)
    volume = calculate_volume_obj(vertices, faces)
    print(volume)
    file2 = r"../test_cube2.obj"
    vertices, faces = read_obj_file(file2)
    volume = calculate_volume_obj(vertices, faces)
    print(volume)
    file3 = r"../test_cube3.obj"
    vertices, faces = read_obj_file(file3)
    volume = calculate_volume_obj(vertices, faces)
    print(volume)
