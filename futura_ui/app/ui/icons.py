# -*- coding: utf-8 -*-
import base64

from PySide2.QtGui import QIcon, QPixmap
from ...icons import *

def _as_bytes(bytestring):
    return base64.b64decode(bytestring)


class Icons(object):
    # Icons from material.io

    # MAIN
    futura = _as_bytes(main_icon)  # create_path('main', 'main_icon.png')
    add = _as_bytes(add)  # create_path('main', 'add.png')
    remove = _as_bytes(remove)  # create_path('main', 'remove.png')
    globe = _as_bytes(globe)  # create_path('main', 'globe.png')


class QIcons(Icons):
    """ Using the Icons class, returns the same attributes, but as QIcon type
    """
    def __getattribute__(self, item):

        pixmap = QPixmap()
        pixmap.loadFromData(Icons.__getattribute__(self, item))

        return QIcon(pixmap)


icons = Icons()
qicons = QIcons()
