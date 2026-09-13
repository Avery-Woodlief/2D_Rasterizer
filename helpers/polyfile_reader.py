from utils.file_operations import find_file
import re
def read_polyfile(filename : str) -> list:
    alias = {"P":"poly", "p":"poly", "poly":"poly", "polygon":"poly"}
    calls = []
    polyfile = find_file(folder_name="objects", file_name=filename).open("r").read().split("\n")
    if len(polyfile) >= 1:
        size = polyfile[0]
        if not re.search(r"\d+x\d+", size):
            raise ValueError("dimensions not specified, broken image file")
        height, width = tuple(map(int, re.findall(r"\d+", size)))
        calls.append({"size":(height, width)})
        polyfile = polyfile[1:]
    existing_layers = set()
    for line in polyfile:
        if len(line) == 0:
            continue
        cmd, layer, color, points = tuple(line.split("|"))
        r, g, b, a = tuple(map(int, re.findall(r"\d+", color)))
        numeric_layer = abs(int(layer))
        if len(existing_layers)>0:
            if numeric_layer > max(existing_layers) + 1:
                numeric_layer = max(existing_layers) + 1
        existing_layers.add(numeric_layer)
        call = {alias.get(cmd):{"layer":numeric_layer, "color":(r, g, b, a)}}
        call[alias.get(cmd)]["points"] = []
        point_list_raw = points.split(";")
        for point in point_list_raw:
            x, y = tuple(map(int, re.findall(r"\d+", point)))
            call[alias.get(cmd)]["points"].append((x, y))
        calls.append(call)
    return calls