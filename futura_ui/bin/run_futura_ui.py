import os
import sys
from ..app import run_futura
from futura.storage import storage


def main():
    #f = open(os.devnull, 'w')
    f = open(os.path.join(storage.futura_dir, 'stdout.txt'), 'w')
    f2 = open(os.path.join(storage.futura_dir, 'err.txt'), 'w')
    sys.stdout = f
    sys.stderr = f2
    run_futura()

    f.close()
    f2.close()

