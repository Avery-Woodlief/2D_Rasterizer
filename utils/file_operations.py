from collections.abc import Callable
from pathlib import Path
import re

ROOT = Path.cwd() # '...'/Image_Processing
if re.search(r"2D_Rasterizer", str(ROOT)) is not None:
    _, b = re.search(r"2D_Rasterizer", str(ROOT)).span()
    ROOT = Path(str(ROOT)[:b])

def validate_file(func : Callable[[str | None, str], Path]):
    def wrapper(*args, **kwargs):
        file_ = func(*args, **kwargs)
        if isinstance(file_, Path):
            return file_ if file_.is_file() and file_.exists() else "N/A"
        return "N/A"
    return wrapper

@validate_file
def find_file(**kw) -> Path | str:
    folder_name = kw.get("folder_name", kw.get("foldername", None))
    file_name = kw.get("file_name", kw.get("filename", None))
    if isinstance(folder_name, (str, Path)) and isinstance(file_name, (str, Path)):
        expected_directory = ROOT / folder_name
        expected_location = expected_directory / file_name
        return expected_location
    return ROOT / file_name if isinstance(file_name, (str, Path)) else "N/A"

def resolve_path(**kw) -> tuple[Path | str, Path | str]:
    folder_name = kw.get("folder_name", kw.get("foldername", None))
    file_name = kw.get("file_name", kw.get("filename", None))
    if isinstance(folder_name, (str, Path)) and isinstance(file_name, (str, Path)):
        absolute_path = ROOT / folder_name / file_name
        relative_path = Path(folder_name) / file_name
        return relative_path, absolute_path
    elif isinstance(file_name, (str, Path)):
        absolute_path = ROOT / file_name
        relative_path = Path(file_name)
        return relative_path, absolute_path
    return "N/A", "N/A"

def overwrite_file(location: Path, what) -> None:
    if isinstance(what, list):
        location.write_text("\n".join(map(str, what)))
    elif isinstance(what, str):
        location.write_text(what)

if __name__ == "__main__":
    #print(find_file(folder_name = 8, file_name = 1))
    #print(resolve_path())
    print(ROOT)
    print(find_file(filename="__init__.py"))