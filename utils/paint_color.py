import numpy as np


def color_bar(num:float) -> np.ndarray:
    color = np.array([int(abs(np.cos(0.5 * np.pi * num)) * 255), int(abs(np.sin(1.0 * np.pi * num)) * 255),
                      int(abs(np.sin(0.5 * np.pi * num)) * 255), 1.0], dtype=np.float32)
    return color


def read_csv(file):
    pos = []
    color_ref = []
    with open(file, 'r') as f:
        next(f)
        for row in f:
            row = row[:-1].split(",")
            pos.append(row[:3])
            color_ref.append(row[6])
        f.close()
    return pos, color_ref


def load_obj(file):
    vertices = []
    faces = []
    try:
        with open(file, "r") as f:
            for row in f:
                if row[:2] == "v ":
                    vertices.append(row[2:-1].split(" "))
                elif row[:2] == "f ":
                    faces.append([item.split("/")[0] for item in row[2:-1].split(" ")])
            f.close()
    except FileNotFoundError:
        pass
    return np.array(vertices, dtype=np.float32), np.array(faces, dtype=np.int32) - np.array([1, 1, 1])


def nearest_search(vertices, pos, ref):
    ref = np.array(ref, dtype=np.float32)
    ref = (ref - np.min(ref)) / (np.max(ref) - np.min(ref))
    vert_color = np.zeros(vertices.shape, dtype=np.int32)
    pos = np.array(pos, dtype=np.float32)

    x_M, x_m = np.min(pos[:, 0]), np.max(pos[:, 0])
    y_M, y_m = np.min(pos[:, 1]), np.max(pos[:, 1])
    z_M, z_m = np.min(pos[:, 2]), np.max(pos[:, 2])

    grid = np.zeros((20*20*20, 100, 2), dtype=np.int32)
    for i, xyz in enumerate(pos):
        x = min(int((xyz[0] - x_m) / (x_M - x_m) * 20), 19)
        y = min(int((xyz[1] - y_m) / (y_M - y_m) * 20), 19)
        z = min(int((xyz[2] - z_m) / (z_M - z_m) * 20), 19)
        grid[x*400+y*20+z] = np.delete(np.insert(grid[x*400+y*20+z], 0, [i, 1], axis=0), -1, axis=0)

    for i, xyz in enumerate(vertices):
        x = max(min(int((xyz[0] - x_m) / (x_M - x_m) * 20), 19), 0)
        y = max(min(int((xyz[1] - y_m) / (y_M - y_m) * 20), 19), 0)
        z = max(min(int((xyz[2] - z_m) / (z_M - z_m) * 20), 19), 0)

        distance = 1e8
        index = -1
        for step, note in enumerate(grid[x*400+y*20+z]):
            point = pos[note[0]]
            if note[-1] != 1.0:  # find empty slot
                if step != 0:  # grid not empty
                    vert_color[i] = color_bar(ref[grid[x * 400 + y * 20 + z][index][0]])[:3]
                    break
                else:
                    vert_color[i] = [255, 255, 255]
                    break

            d = np.linalg.norm(xyz-point)
            if d < distance:
                distance = d
                index = step


    return vert_color


def export_ply(file, pos, color, facets):

    vertex_num = len(pos)
    face_num = len(facets)
    with open(file, 'w') as f:
        f.write(f"ply\nformat ascii 1.0\ncomment author Greg Turk\ncomment object another cube\nelement vertex {vertex_num}\nproperty float x\n"+
                f"property float y\nproperty float z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\nelement face {face_num}\n"+
                "property list uchar int vertex_index\nend_header")
        for vertex, col in zip(pos, color):
            f.write(f"{vertex[0]} {vertex[1]} {vertex[2]} {col[0]} {col[1]} {col[2]}\n")
        for facet in facets:
            f.write(f"3 {facet[0]} {facet[1]} {facet[2]}\n")
        f.close()



if __name__ == "__main__":
    file = r"C:\Users\ysugi\PycharmProjects\QtOpenGL\CM_Mie_case02_DICOM_0.csv"
    pos, ref = read_csv(file)
    file2 = r"C:\Users\ysugi\PycharmProjects\QtOpenGL\m02.obj"
    vertices, facets = load_obj(file2)
    color = nearest_search(vertices, pos, ref)
    exp_file = r"a.ply"
    export_ply(exp_file, vertices, color, facets)