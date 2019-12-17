from PySide2 import QtWidgets, QtCore

from ..widgets.filter import FilterListerWidget, parse_filter_widget
from ..widgets.geo import LocationSelectorWidget
from ...utils import findMainWindow
from ..ui_files import Ui_RegionalisationWizard

from futura.utils import create_filter_from_description
from futura import w
from futura.proxy import WurstProcess

class RegionalisationWizard(Ui_RegionalisationWizard, QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(RegionalisationWizard, self).__init__(parent)

        self.setupUi(self)

        self.filter_widget = FilterListerWidget()
        self.filterLayout.addWidget(self.filter_widget)

        self.location_widget = LocationSelectorWidget()
        self.locationLayout.addWidget(self.location_widget)

        self.currentIdChanged.connect(self.page_change)

    def page_change(self, page_id):

        if page_id == 1:
            self.restrict_locations()

        elif page_id == 2:
            self.confirm_setup()

    def confirm_setup(self):
        print("This is the last page")

        this_filter = create_filter_from_description(parse_filter_widget(self.filter_widget))
        db = findMainWindow().loader.database.db

        this_item_set = [WurstProcess(x) for x in w.get_many(db, *this_filter)]

        #this_item = w.get_one(db, *this_filter)
        print(this_item_set)

        item_string = ""
        for n, this_item in enumerate(this_item_set):
            item_string += "{} ({}) [{}]".format(this_item['name'], this_item['unit'], this_item['location'])
            if n != len(this_item_set):
                item_string += "\n"

        self.processLabel.setText(item_string)
        if len(this_item_set) > 1:
            self.processDescriptionLabel.setText('Base processes: ')
        else:
            self.processDescriptionLabel.setText('Base process: ')

        location_list = ", ".join([x['display'] for x in self.location_widget.checked_items])

        self.locationLabel.setText(location_list)

    def restrict_locations(self):
        base_filter = parse_filter_widget(self.filter_widget)
        no_location_filter = [x for x in base_filter if x['args'][0] != 'location']
        this_filter = create_filter_from_description(base_filter)
        no_location = create_filter_from_description(no_location_filter)
        db = findMainWindow().loader.database.db
        this_item = w.get_one(db, *this_filter)
        item_location = this_item['location']
        other_items = w.get_many(db, *no_location)
        other_locations = [x['location'] for x in other_items]

        other_locations = [x for x in other_locations if x != 'RoW']

        locations = list(set(other_locations + [item_location]))

        print(locations)

        self.location_widget.find_and_disable(locations)



