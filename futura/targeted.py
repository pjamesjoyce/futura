from . import w
from .utils import create_filter_from_description


def create_process_filter(name):

    filter_desc = [
            {'filter': 'equals', 'args': ['name', name]},
    ]

    name_filter = create_filter_from_description(filter_desc)
    
    return name_filter


class FuturaProcess():
    def __init__(self, process, database):
        self.process = process
        self.database = database
        self.exchanges = self.process['exchanges']
        self.technosphere = [x for x in self.exchanges if x['type'] == 'technosphere']
        self.biosphere = [x for x in self.exchanges if x['type'] == 'biosphere']
        self.production = [x for x in self.exchanges if x['type'] == 'production']
        self.single_production = None

        if len(self.production) == 1:
            self.single_production = self.production[0]

    def change_production_amount(self, new_amount):

        assert self.single_production, 'Multiple outputs found, all processes must be single output'

        if not self.single_production.get('futura_metadata'):
            self.single_production['futura_metadata'] = {}
        
        self.single_production['futura_metadata']['original amount'] = self.single_production['amount']
        self.single_production['amount'] = new_amount

    def change_exchange_amounts(self, change_dict):

        """
        change_dict needs to be in the format {('name', 'location'): 123.456}
        """

        for exc in self.exchanges:
            if (exc['name'], exc['location']) in change_dict.keys():
                if not exc.get('futura_metadata'):
                    exc['futura_metadata'] = {}
                exc['futura_metadata']['original amount'] = exc['amount']
                exc['amount'] = change_dict[(exc['name'], exc['location'])]
