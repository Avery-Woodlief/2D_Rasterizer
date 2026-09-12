from utils.file_operations import find_file
import re
def read_polyfile(filename : str) -> list:
    alias = {"P":"poly", "p":"poly", "poly":"poly", "polygon":"poly"}
    calls = []
    polyfile = find_file(folder_name="objects", file_name=filename).open("r").read().split("\n")
    for line in polyfile:
        cmd, layer, color, points = tuple(line.split("|"))
        r, g, b, a = tuple(map(int, re.findall(r"\d+", color)))
        call = {alias.get(cmd):{"layer":int(layer), "color":(r, g, b, a)}}
        call[alias.get(cmd)]["points"] = []
        point_list_raw = points.split(";")
        for point in point_list_raw:
            x, y = tuple(map(int, re.findall(r"\d+", point)))
            call[alias.get(cmd)]["points"].append((x, y))
        calls.append(call)
    return calls