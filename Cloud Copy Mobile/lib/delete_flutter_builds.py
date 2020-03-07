import os
import glob


def delete_item(f):
    try:
        os.remove(f)
    except PermissionError:
        for file in os.listdir(f):
            delete_item(os.path.join(f, file))


delete_item('Cloud Copy Mobile/build')