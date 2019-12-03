from PySide2 import QtWidgets
try:
    from ..utils import load_ui_file
except ImportError:
    from futura_ui.app.ui.utils import load_ui_file

try:
    from ..icons import qicons
except ImportError:
    from futura_ui.app.ui.icons import qicons

try:
    from ...signals import signals
except ImportError:
    from futura_ui.app.signals import signals

try:
    from ...utils import findMainWindow
except ImportError:
    from futura_ui.app.utils import findMainWindow

from PySide2.QtCore import Signal

from futura.utils import create_filter_from_description

from futura import w

import os
#from functools import partial


def parse_filter_widget(widget):
    filter_dict = {
        'Equals': 'equals',
        'Contains': 'contains',
        'Starts with': 'startswith',
        "Doesn't contain any": 'doesnt_contain_any',
        'Either': 'either'
    }

    item_dict = {
        'Name': 'name',
        'Location': 'location',
        'Unit': 'unit',
        'Reference product': 'reference product',
        'Database': 'database',
        'Code': 'code'
    }

    filter_description = []
    for f in widget.filter_steps:

        # TODO: add subfilters

        this_filter = filter_dict[f.filter_box.currentText()]
        search_text = f.search_term.text()

        if this_filter == 'doesnt_contain_any':
            split_hierarchy = [';', ',']
            for x in split_hierarchy:
                if x in search_text:
                    break
            search_text = [i.strip().lstrip() for i in search_text.split(x)]

        result_dict = {
            'filter': this_filter,
            'args': [item_dict[f.item_box.currentText()], search_text]
        }

        filter_description.append(result_dict)
    return filter_description


class FilterWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FilterWidget, self).__init__(parent)

        ui_path = 'filter_widget.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)

        self.subfilters = []

        self.filter_box.currentIndexChanged.connect(self.check_subfilter)

    def check_subfilter(self, index):
        if self.filter_box.currentText() == 'Either':
            self.add_subfilter()
            self.item_box.setEnabled(False)
            self.search_term.hide()
        else:
            self.clear_subfilters()
            self.search_term.show()
            self.item_box.setEnabled(True)

    def add_subfilter(self):
        self.subfilters.append(SubFilterWidget())
        self.subFilterLayout.addWidget(self.subfilters[-1])

    def clear_subfilters(self):
        for i in reversed(range(self.subFilterLayout.count())):
            self.subFilterLayout.itemAt(i).widget().setParent(None)
            self.subfilters = []


class SubFilterWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SubFilterWidget, self).__init__(parent)

        ui_path = 'sub_filter_widget.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)
        load_ui_file(ui_path, self)

        self.subaddButton.setIcon(qicons.add)
        self.subaddButton.pressed.connect(self.add_another)

        self.subremoveButton.setIcon(qicons.remove)
        self.subremoveButton.pressed.connect(self.remove_me)

    def remove_me(self):
        if len(self.parent().subfilters) != 1:
            ix = self.parent().subFilterLayout.indexOf(self)
            self.parent().subfilters.pop(ix)
            print(self.parent().subfilters)
            self.setParent(None)

    def add_another(self):
        self.parent().add_subfilter()


class FilterListerWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FilterListerWidget, self).__init__(parent)

        ui_path = 'filter_lister_widget.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)

        self.addButton.setIcon(qicons.add)
        self.addButton.pressed.connect(self.add_filter_step)

        self.removeButton.setIcon(qicons.remove)
        self.removeButton.pressed.connect(self.remove_filter_step)

        self.testButton.pressed.connect(self.test_filter)

        self.filter_steps = []

        self.add_filter_step()

    def add_filter_step(self):
        self.filter_steps.append(FilterWidget())
        self.filterLayout.addWidget(self.filter_steps[-1])

    def remove_filter_step(self):
        self.filter_steps.pop(-1)
        self.filterLayout.itemAt(self.filterLayout.count()-1).widget().setParent(None)

    def create_filter(self):
        description = parse_filter_widget(self)
        return create_filter_from_description(description)

    def test_filter(self):
        test_filter = self.create_filter()
        db = findMainWindow().loader.database.db
        result = list(w.get_many(db, *test_filter))
        if len(result) == 0:
            message = "No results found!"
        elif len(result) == 1:
            message = "{} result found - {} ({}) [{}]".format(len(result),
                                                              result[0]['name'],
                                                              result[0]['unit'],
                                                              result[0]['location'])
        else:
            message = "{} results found, including {} ({}) [{}]".format(len(result),
                                                              result[0]['name'],
                                                              result[0]['unit'],
                                                              result[0]['location'])
        self.test_result.setText(message)


class FilterListerDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(FilterListerDialog, self).__init__(parent)

        ui_path = 'blank_dialog.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)
        self.filter_widget = FilterListerWidget()
        self.baseLayout.addWidget(self.filter_widget)


if __name__ == '__main__':

    import sys


    app = QtWidgets.QApplication(sys.argv)

    view = FilterListerDialog()

    view.setWindowTitle("TEST")
    view.show()

    sys.exit(app.exec_())