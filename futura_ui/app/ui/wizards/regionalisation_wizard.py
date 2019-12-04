from PySide2 import QtWidgets
import os
from ..utils import load_ui_file
from ..widgets.filter import FilterListerWidget, parse_filter_widget
from ..widgets.geo import LocationSelectorWidget
from ...utils import findMainWindow

from futura.utils import create_filter_from_description
from futura import w

class RegionalisationWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(RegionalisationWizard, self).__init__(parent)

        ui_path = 'regionalisation_wizard.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)
        self.filter_widget = FilterListerWidget()
        self.filterLayout.addWidget(self.filter_widget)

        self.location_widget = LocationSelectorWidget()
        self.locationLayout.addWidget(self.location_widget)

        self.currentIdChanged.connect(self.confirm_setup)

    def confirm_setup(self, id):
        if id == 2:
            print("This is the last page")

            this_filter = create_filter_from_description(parse_filter_widget(self.filter_widget))
            db = findMainWindow().loader.database.db
            this_item = w.get_one(db, *this_filter)
            print(this_item)
            item_string = "{} ({}) [{}]".format(this_item['name'], this_item['unit'], this_item['location'])
            self.processLabel.setText(item_string)

            location_list = ", ".join([x['display'] for x in self.location_widget.checked_items])

            self.locationLabel.setText(location_list)

