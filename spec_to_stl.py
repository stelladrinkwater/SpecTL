import numpy as np
from PIL import Image
from stl import mesh

def png_to_stl(png_path, stl_path, base_height=20, max_height=30, spike_factor=1.0):
    # load grayscale image
    img = Image.open(png_path).convert('L')
    arr = np.array(img)
    
    # normalize pixel values (0 black → 0 height, 255 white → max_height)
    norm = arr / 255.0
    # nonlinear height scaling for spikes
    heights = (norm ** spike_factor) * max_height * 10  # jacked heights x10
    
    rows, cols = heights.shape
    
    vertices = []
    faces = []
    
    # base vertices (z=0)
    for y in range(rows):
        for x in range(cols):
            vertices.append([x, y, 0])
    # top vertices (z=base_height + height)
    for y in range(rows):
        for x in range(cols):
            vertices.append([x, y, base_height + heights[y, x]])
    
    def idx(r, c, top):
        offset = rows * cols if top else 0
        return r * cols + c + offset
    
    # base faces (flat)
    for y in range(rows - 1):
        for x in range(cols - 1):
            faces.append([idx(y, x, False), idx(y + 1, x, False), idx(y, x + 1, False)])
            faces.append([idx(y + 1, x, False), idx(y + 1, x + 1, False), idx(y, x + 1, False)])
    
    # top faces (heightmap)
    for y in range(rows - 1):
        for x in range(cols - 1):
            faces.append([idx(y, x, True), idx(y, x + 1, True), idx(y + 1, x, True)])
            faces.append([idx(y + 1, x, True), idx(y, x + 1, True), idx(y + 1, x + 1, True)])
    
    # side walls
    for y in range(rows - 1):
        for x in range(cols - 1):
            # front edge
            faces.append([idx(y, x, False), idx(y, x, True), idx(y + 1, x, False)])
            faces.append([idx(y + 1, x, False), idx(y, x, True), idx(y + 1, x, True)])
            
            # right edge
            faces.append([idx(y, x + 1, False), idx(y, x + 1, True), idx(y, x, False)])
            faces.append([idx(y, x, False), idx(y, x + 1, True), idx(y, x, True)])
            
            # back edge
            faces.append([idx(y + 1, x + 1, False), idx(y + 1, x + 1, True), idx(y, x + 1, False)])
            faces.append([idx(y, x + 1, False), idx(y + 1, x + 1, True), idx(y, x + 1, True)])
            
            # left edge
            faces.append([idx(y + 1, x, False), idx(y + 1, x, True), idx(y + 1, x + 1, False)])
            faces.append([idx(y + 1, x + 1, False), idx(y + 1, x, True), idx(y + 1, x + 1, True)])
    
    vertices = np.array(vertices)
    faces = np.array(faces)
    
    model_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            model_mesh.vectors[i][j] = vertices[f[j], :]
    
    model_mesh.save(stl_path)
    print(f"STL saved to {stl_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("usage: python spec_to_stl.py input.png output.stl [base_height=20] [max_height=30] [spike_factor=1.0]")
    else:
        base = float(sys.argv[3]) if len(sys.argv) > 3 else 20
        max_h = float(sys.argv[4]) if len(sys.argv) > 4 else 30
        spike = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
        png_to_stl(sys.argv[1], sys.argv[2], base_height=base, max_height=max_h, spike_factor=spike)
