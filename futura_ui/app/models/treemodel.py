from PySide2.QtCore import QAbstractItemModel, QFile, QIODevice, QModelIndex, Qt
from PySide2.QtWidgets import QApplication, QTreeView
from PySide2.QtGui import QImage, QIcon
from pathlib import Path
import os


image_path = os.path.join(Path(os.path.dirname(os.path.realpath(__file__))), 'assets', 'gui_images')
market_icon = QImage(os.path.join(image_path, 'ic_shopping_cart_black_18dp.png'))
production_icon = QImage(os.path.join(image_path, 'ic_build_black_18dp.png'))
import_icon = QImage(os.path.join(image_path, 'ic_keyboard_tab_black_18dp.png'))
cogeneration_icon = QImage(os.path.join(image_path, 'ic_call_split_black_18dp.png'))
unknown_icon = QImage(os.path.join(image_path, 'ic_priority_high_black_18dp.png'))

class TreeItem(object):

    def __init__(self, data, parent=None):

        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData#[column]
            #return self.itemData['display']
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0

class TreeModel(QAbstractItemModel):

    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)

        self.rootItem = TreeItem(['name'])

        self.setupModelData(data, self.rootItem)

    def columnCount(self, parent=None):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role=None):
        if not index.isValid():
            return None

        item = index.internalPointer()

        d = item.data(index.column())

        if role == Qt.DisplayRole:
            return d['display']

        if role == Qt.DecorationRole:
            activity_type = d['type']
            if activity_type == 'market':
                return market_icon
            elif activity_type == 'production':
                return production_icon
            elif activity_type == 'import':
                return import_icon
            elif activity_type == 'cogeneration':
                return cogeneration_icon
            elif activity_type == 'unknown':
                return unknown_icon

        if role == "DataRole":
            return d
        else:
            return None

    def flags(self, index):

        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)
        return None

    def index(self, row, column, parent=None):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)

        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def get_model_tree(self, data, parent):

        if data:

            treeData = {k: v for k, v in data.items() if k != 'children'}
            treeData['display'] = "[{}] {}".format(data['location'], data['name'])
            #print(treeData['display'])

            thisItem = TreeItem(treeData, parent)

            parent.appendChild(thisItem)

            for c in data['children']:
                self.get_model_tree(c, thisItem)


    def setupModelData(self, data, parent):

        #print(data)

        for sector, tree in data.items():
            this_parent = TreeItem({'name': sector,
                                    'display': sector,
                                    'type': 'toplevel'},
                                   parent)
            parent.appendChild(this_parent)

            for subtree in tree:
                self.get_model_tree(subtree, this_parent)


if __name__ == '__main__':

    import sys
    from futura.constants import ELECTRICITY_TREE

    #print (ELECTRICITY_TREE)

    app = QApplication(sys.argv)

    tree_data = {'Electricity': ELECTRICITY_TREE,
                'Cement':{},
                'Aluminium':{},
                'Steel':{},
                'Lithium':{},
                'Glass':{}
                }

    model = TreeModel(tree_data)

    #print (model)

    view = QTreeView()

    view.setModel(model)
    view.setWindowTitle("TEST")
    view.show()

    sys.exit(app.exec_())





