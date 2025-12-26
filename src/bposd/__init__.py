from ldpc import bposd_decoder
import os
import bposd


def get_include():
    path = os.path.dirname(bposd.__file__)
    return path


with open(f"{get_include()}/VERSION", "r") as f:
    __version__ = f.read()

print(f"[bposd] Using LOCAL compiled version {__version__} from {get_include()}")
