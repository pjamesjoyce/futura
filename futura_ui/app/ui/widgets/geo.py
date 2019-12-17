from PySide2 import QtWidgets, QtCore

from ..icons import qicons

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

    def remove_checkboxes(self):

        j = 0
        while self.model.item(j):
            for i in self.model.iterItems(self.model.item(j)):
                i.setCheckable(False)
            j += 1

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


class LocationInputWidget(QtWidgets.QLineEdit):
    buttonClicked = QtCore.Signal()

    def __init__(self, tree=None, parent=None):
        super(LocationInputWidget, self).__init__(parent)

        if not tree:
            self.tree = global_tree
        else:
            self.tree = tree

        self.checked_items = []

        self.model = LocationModel(self.tree)
        self.view = QtWidgets.QTreeView(self)
        self.view.setModel(self.model)
        self.view.sortByColumn(0, QtCore.Qt.AscendingOrder)

        self.model.itemChanged.connect(self.display_selection)

        self.button = QtWidgets.QToolButton(self)
        self.button.setIcon(qicons.globe)
        # self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        self.button.clicked.connect(self.buttonClicked.emit)
        self.button.setPopupMode(QtWidgets.QToolButton.InstantPopup)

        self.button.setArrowType(QtCore.Qt.NoArrow)

        frameWidth = self.style().pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()

        action = QtWidgets.QWidgetAction(self.button)
        action.setDefaultWidget(self.view)

        self.button.addAction(action)

        self.setStyleSheet('QToolButton {color:rgba(255, 255, 255, 0);}')

        self.setMinimumSize(max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth * 2 + 2),
                            max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth * 2 + 2))

    def resizeEvent(self, event):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frameWidth - buttonSize.width(),
                         (self.rect().bottom() - buttonSize.height() + 1) / 2)
        super(LocationInputWidget, self).resizeEvent(event)

    def display_selection(self, item):

        state = ['UNCHECKED', 'TRISTATE', 'CHECKED'][item.checkState()]
        # print ("Item with text '%s', is at state %s\n" % ( item.text(),  state))
        # print(item.data(QtCore.Qt.UserRole))

        item_dict = {
            'display': item.data(QtCore.Qt.DisplayRole),
            'code': item.data(QtCore.Qt.UserRole)
        }

        if state == 'CHECKED':
            self.checked_items.append(item_dict)
        elif state == 'UNCHECKED':
            self.checked_items[:] = [x for x in self.checked_items if x['code'] != item_dict['code']]

        if len(self.checked_items) == 0:
            self.setText('')
        else:
            self.setText(", ".join([x['code'] for x in self.checked_items]))


