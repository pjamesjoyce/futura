import sys
import importlib
from pkg_resources import iter_entry_points


def load_plugins():
    importlib.import_module('futura')

    for entry_point in iter_entry_points(group="futura_plugins"):
        submodule_name = entry_point.module_name#.split('.')[-1]

        setattr(sys.modules['futura'],
                submodule_name,
                importlib.import_module(entry_point.module_name, package='futura')
                )
