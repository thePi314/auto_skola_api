import importlib

def get_class(full_path):
    class_name = full_path.split(".")[-1]
    path = full_path[: -(len(class_name) + 1)]
    module = importlib.import_module(path)
    class_ = getattr(module, class_name)
    return class_


def get_instance(full_path):
    instance = get_class(full_path)()
    return instance
