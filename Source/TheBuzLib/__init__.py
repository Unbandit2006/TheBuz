from TheBuzLib.Database import *
from TheBuzLib.Sender import *
import importlib.util

def import_module_by_path(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module