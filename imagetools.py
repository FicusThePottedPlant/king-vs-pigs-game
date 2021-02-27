from PIL import Image


def del_transparent(file):
    im = Image.open(file)
    pixels = im.load()
    data = {}
    w, h = im.size
    a_left, a_right, a_top, a_bottom = 0, w, 0, h
    data_w = {i: [] for i in range(w)}
    data_h = {i: [] for i in range(h)}
    for x in range(w):
        for y in range(h):
            r, g, b, a = pixels[x, y]
            if a == 0:
                data_w[x].append(y)
                data_h[y].append(x)

    for i, j in data_w.items():
        if len(j) != h:
            a_bottom = i

    for i, j in reversed(data_w.items()):
        if len(j) != h:
            a_top = i

    for i, j in data_h.items():
        if len(j) != w:
            a_right = i

    for i, j in reversed(data_h.items()):
        if len(j) != w:
            a_left = i

    cropped = im.crop((a_left - 2, a_top - 2, a_right + 2, a_bottom + 2))
    cropped.save(file)
    return cropped.size

