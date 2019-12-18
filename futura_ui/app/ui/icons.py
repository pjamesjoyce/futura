# -*- coding: utf-8 -*-
import os

from PySide2.QtGui import QIcon

from futura_ui import PACKAGE_DIRECTORY


def create_path(folder: str, filename: str) -> str:
    """ Builds a path to the image file.
    """
    return os.path.join(PACKAGE_DIRECTORY, "icons", folder, filename)


# CURRENTLY UNUSED ICONS

    # Modular LCA (keep until this is reintegrated)
    # add_db = create_path('metaprocess', 'add_database.png')
    # close_db = create_path('metaprocess', 'close_database.png')
    # cut = create_path('metaprocess', 'cut.png')
    # duplicate = create_path('metaprocess', 'duplicate.png')
    # graph_lmp = create_path('metaprocess', 'graph_linkedmetaprocess.png')
    # graph_mp = create_path('metaprocess', 'graph_metaprocess.png')
    # load_db = create_path('metaprocess', 'open_database.png')
    # metaprocess = create_path('metaprocess', 'metaprocess.png')
    # new = create_path('metaprocess', 'new_metaprocess.png')
    # save_db = create_path('metaprocess', 'save_database.png')
    # save_mp = create_path('metaprocess', 'save_metaprocess.png')

    # key = create_path('main', 'key.png')
    # search = create_path('main', 'search.png')
    # switch = create_path('main', 'switch-state.png')


class Icons(object):
    # Icons from href="https://www.flaticon.com/

    # MAIN
    futura = create_path('main', 'main_icon.png')
    add = create_path('main', 'add.png')
    remove = create_path('main', 'remove.png')
    globe = create_path('main', 'globe.png')

    # arrows
    # right = create_path('main', 'right.png')
    # left = create_path('main', 'left.png')
    # forward = create_path('main', 'forward.png')
    # backward = create_path('main', 'backward.png')

    # Simple actions
    # delete = create_path('context', 'delete.png')
    # copy = create_path('context', 'copy.png')
    # add = create_path('context', 'add.png')
    # edit = create_path('main', 'edit.png')
    # calculate = create_path('main', 'calculate.png')
    # question = create_path('context', 'question.png')

    # database
    # import_db = create_path('main', 'import_database.png')
    # duplicate_database = create_path('main', 'duplicate_database.png')

    # activity
    # duplicate_activity = create_path('main', 'duplicate_activity.png')
    # duplicate_to_other_database = create_path('main', 'import_database.png')

    # windows
    # graph_explorer = create_path('main', 'graph_explorer.png')
    # debug = create_path('main', 'ladybird.png')
    # issue = create_path('main', 'idea.png')
    # settings = create_path('main', 'settings.png')
    # history = create_path('main', 'history.png')
    # welcome = create_path('main', 'welcome.png')
    # main_window = create_path('main', 'home.png')


class QIcons(Icons):
    """ Using the Icons class, returns the same attributes, but as QIcon type
    """
    def __getattribute__(self, item):
        return QIcon(str(Icons.__getattribute__(self, item)))


icons = Icons()
qicons = QIcons()
