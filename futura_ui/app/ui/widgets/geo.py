from PySide2 import QtWidgets, QtCore

try:
    from ...models.geo import LocationModel, global_tree
except ImportError:
    from futura_ui.app.models.geo import LocationModel, global_tree


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

        self.find_and_disable(['CH'])

        layout.addWidget(self.view)

    def find_and_disable(self, locations):

        j = 0
        while self.model.item(j):
            for i in self.model.iterItems(self.model.item(j)):
                i.setEnabled(True)
            j += 1

        for l in locations:
            match = self.model.match(self.model.index(0, 0),
                                     QtCore.Qt.UserRole,
                                     l,
                                     1,
                                     QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
            if match:
                item = self.model.itemFromIndex(match[0])
                item.setEnabled(False)

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


if __name__ == '__main__':

    import sys


    app = QtWidgets.QApplication(sys.argv)

    view = LocationSelectorWidget()

    view.setWindowTitle("TEST")
    view.show()

    sys.exit(app.exec_())
