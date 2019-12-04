import constructive_geometries as cg
import country_converter as cc
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QApplication, QTreeView
from PySide2.QtCore import Qt

import json
import os

g = cg.Geomatcher()
from pprint import pprint


def location_tree(root, exclude_phrases=None, name_switch_dict=None, other=None):
    seen = []
    tree = {}
    other_dict = {'name': 'Other', 'children': {}}

    if not exclude_phrases:
        exclude_phrases = []
    if not name_switch_dict:
        name_switch_dict = {}
    if not other:
        other = []

    # print(root)
    seen.append(root)

    def get_branches(start, parent):
        if not isinstance(start, tuple):
            name = cc.convert(start, to='name_short')
            if name == 'not found':
                name = start
                name = name_switch_dict.get(name, name)
        else:
            name = name_switch_dict.get(start[1], start[1])

        if isinstance(start, tuple):
            key = start[1]
        else:
            key = start

        parent[key] = {'name': name,
                         'children': {}}

        contained = g.contained(start, include_self=False)

        if contained:
            for area in contained:
                if area not in seen:
                    in_other = False
                    if area in other:
                        in_other = True
                    seen.append(area)
                    exclude = False
                    for phrase in exclude_phrases:
                        if isinstance(area, tuple):
                            check = area[1]
                        else:
                            check = area
                        if phrase in check:
                            exclude = True
                            break

                    if not exclude:
                        if not in_other:
                            get_branches(area, parent[key]['children'])
                        else:
                            get_branches(area, other_dict['children'])
        seen.append(start)

    get_branches(root, tree)

    if other_dict:
        tree[root]['children']['Other'] = other_dict

    return tree


exclude_phrases = [
    'IAI Area',
    'w/o',
    'UN-NEUROPE',
    'UN-EEUROPE',
    'UN-SEUROPE',
    'UCTE',
    'ENTSO',
    'BALTSO',
    'CENTREL',
    'NORDEL',
    'WEU',
    'Switzerland and France',
    'Russia and Turkey',
    'NAFTA',
    'without Alberta',
    'without Quebec',
    'FSU',
    'without China',
    'UN-ASIA'
]

name_switch_dict = {
    'RER': 'Europe',
    'RAS': 'Asia',
    'RNA': 'North America',
    'RLA': 'Latin America',
    'RAF': 'Africa',
    'RME': 'Middle East',
    'CS': 'Serbia and Montenegro',
    'UN-AMERICAS': 'Americas',
    'UN-EUROPE': 'Europe & Russia',
    'UN-OCEANIA': 'Oceania',
    'UN-AUSTRALIANZ': 'Australia & New Zealand',
    'UN-MELANESIA': 'Melanesia',
    'UN-MICRONESIA': 'Micronesia',
    'UN-POLYNESIA': 'Polynesia',
    'UN-WASIA': 'West Asia',
    'UN-EASIA': 'East Asia',
    'SAS': 'South Asia',
    'UN-SEASIA': 'South East Asia',
    'UN-EAFRICA': 'East Africa',
    'UN-MAFRICA': 'Middle Africa',
    'UN-NAFRICA': 'North Africa',
    'UN-SASIA': 'Southern Africa', # Note - I think this is a bug either from ecoinvent or constructive_geometries
    'UN-WAFRICA': 'West Africa',
    'UN-CAMERICA': 'Central America',
    'UN-SAMERICA': 'South America',
    'UN-CARIBBEAN': 'Caribbean',
    'WECC': 'Western Electricity Coordinating Council',
    'MRO': 'Midwest Reliability Organization',
    'NPCC': 'Northeast Power Coordinating Council',
}

other = [
     'AQ',
     ('ecoinvent', 'France, including overseas territories'),
     ('ecoinvent', 'Coral Sea Islands'),
     'TF',
     'UM',
     'GS',
     ('ecoinvent', 'Spratly Islands'),
     'FO',
     'IO',
     ('ecoinvent', 'Bajo Nuevo'),
     ('ecoinvent', 'AUS-IOT'),
     'WF',
     ('ecoinvent', 'Guantanamo Bay'),
     ('ecoinvent', 'AUS-AC'),
     ('ecoinvent', 'Clipperton Island'),
     'HM',
     ('ecoinvent', 'Scarborough Reef'),
     ('ecoinvent', 'Serranilla Bank')
]

#global_tree = location_tree('GLO', exclude_phrases, name_switch_dict, other)

#tree_json = json.dumps(global_tree, indent=2)

#with open('global_tree.json', 'w') as f:
#    f.write(tree_json)

json_path = 'global_tree.json'
json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), json_path)

with open(json_path, 'r') as f:
    global_tree = json.load(f)


#raw_tree = location_tree('GLO')
#pprint(global_tree)


class LocationModel(QStandardItemModel):
    def __init__(self, tree):
        super(LocationModel, self).__init__()
        self.parentItem = self.invisibleRootItem()
        if tree:
            root = list(tree.keys())[0]
            self.parse_tree(tree[root])

    def parse_tree(self, tree):

        self.clear()
        self.parentItem = self.invisibleRootItem()
        self.setHorizontalHeaderLabels(['Location'])

        def parse(this_dict, parent):

            for c, v in this_dict['children'].items():

                item = QStandardItem()
                item.setData(v['name'], Qt.DisplayRole)
                item.setData(c, Qt.UserRole)
                item.setCheckable(True)
                parent.appendRow([item])
                parse(v, item)

        parse(tree, self.parentItem)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    model = LocationModel(global_tree)

    view = QTreeView()

    view.setModel(model)

    #view.setSortingEnabled(True)
    view.sortByColumn(0, Qt.AscendingOrder)
    view.setWindowTitle("TEST")
    view.show()

    sys.exit(app.exec_())