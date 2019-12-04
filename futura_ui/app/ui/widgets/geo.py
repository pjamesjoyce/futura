from PySide2 import QtWidgets, QtCore

from ...models.geo import LocationModel, global_tree


class LocationSelectorWidget(QtWidgets.QWidget):

    def __init__(self, tree=None):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QHBoxLayout(self)

        self.checked_items = []

        if not tree:
            self.tree = global_tree
        else:
            self.tree = tree

        self.model = LocationModel(self.tree)
        self.model.itemChanged.connect(self.parse_selection)

        self.view = QtWidgets.QTreeView(self)
        self.view.setModel(self.model)
        self.view.sortByColumn(0, QtCore.Qt.AscendingOrder)

        layout.addWidget(self.view)

    def parse_selection(self, item):

        state = ['UNCHECKED', 'TRISTATE', 'CHECKED'][item.checkState()]

        item_dict = {
            'display': item.data(QtCore.Qt.DisplayRole),
            'code': item.data(QtCore.Qt.UserRole)
        }

        if state == 'CHECKED':
            self.checked_items.append(item_dict)
        elif state == 'UNCHECKED':
            self.checked_items[:] = [x for x in self.checked_items if x['code'] != item_dict['code']]



