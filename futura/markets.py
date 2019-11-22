from . import warn
from .wrappers import FuturaDatabase
#import wurst as w
from . import w
from wurst.searching import exclude
from itertools import groupby
from collections import OrderedDict
import pandas as pd
import matplotlib.pyplot as plt

def add_exchange_to_activity(base_activity, activity_to_link_to):
    exchange_template = {'uncertainty type': 0,
                         'loc': 0,
                         'amount': 0,
                         'type': 'technosphere',
                         'production volume': 0,
                         'product': '',
                         'name': '',
                         'unit': '',
                         'location': ''}

    rp = w.reference_product(activity_to_link_to)
    key_list = ['production volume', 'product', 'name', 'unit', 'location']
    for k in key_list:
        exchange_template[k] = rp[k]

    if exchange_template not in base_activity['exchanges']:
        base_activity['exchanges'].append(exchange_template)
    else:
        warn('Exchange of {} already exists in this process, not adding it'.format(activity_to_link_to['name']))


def get_processes_from_exchanges(process, database, reference_product):

    assert isinstance(database, FuturaDatabase), "database needs to be a futura FuturaDatabase object"

    processes = [w.get_one(database.db, *[w.equals('name', e['name']),
                                          w.equals('location', e['location']),
                                          w.equals('reference product', e['product'])])
                 for e in w.technosphere(process)
                 if e['product'] == reference_product and e['name'] != process['name']]

    return processes


def alter_production_volumes(processes, production_volumes, mismatch_ok=False):

    old_pvs = [w.reference_product(x)['production volume'] for x in processes]
    pre_total = sum(old_pvs)

    assert len(processes) == len(production_volumes)

    if not mismatch_ok:
        assert pre_total == sum(
            production_volumes), "The old and new production volumes don't match, " \
                                 "either fix this or set mismatch_ok = True"

    for n, x in enumerate(processes):
        w.reference_product(x)['production volume'] = production_volumes[n]


def fix_exchange_production_volumes(process, database):

    assert isinstance(database, FuturaDatabase), "database needs to be a futura FuturaDatabase object"

    for e in w.technosphere(process):
        link_filter = [w.equals('name', e['name']), w.equals('location', e['location']),
                       w.equals('reference product', e['product'])]
        actual_link = w.get_one(database.db, *link_filter)
        e['production volume'] = w.reference_product(actual_link)['production volume']


def update_technosphere_exchanges_from_pvs(process, database):

    assert isinstance(database, FuturaDatabase), "database needs to be a futura FuturaDatabase object"

    fix_exchange_production_volumes(process, database)

    technosphere_exchanges = [e for e in w.technosphere(process)]

    for g, v in groupby(technosphere_exchanges, lambda x: x['product']):
        # print(g)
        v_list = list(v)
        self_excluded_v_list = [x for x in v_list if x['name'] != process['name']]

        amount_sum = sum([x['amount'] for x in self_excluded_v_list])

        pv_sum = sum(x['production volume'] for x in self_excluded_v_list)

        for x in self_excluded_v_list:
            new_amount = amount_sum * (x['production volume'] / pv_sum)
            # print("{}: {}".format(x['name'], new_amount))
            x['amount'] = new_amount
            x['loc'] = new_amount


def find_possible_additional_market_exchanges(process, database, include_transport=False):
    assert isinstance(database, FuturaDatabase), "database needs to be a futura FuturaDatabase object"
    assert process['name'].startswith('market') and not process['name'].startswith('market group'), \
        'This function only works with market processes (not market groups or production processes)'

    technosphere_exchanges = [e for e in w.technosphere(process)]

    result = []
    # result_dict = {}

    for g, v in groupby(technosphere_exchanges, lambda x: (x['product'],
                                                           x['location'],
                                                           x['unit'])):
        v_list = list(v)
        names = [e['name'] for e in v_list if e['name'] != process['name']]

        possible_additions_filter = []
        possible_additions_filter += [w.equals('unit', g[2])]
        possible_additions_filter += [w.equals('reference product', g[0])]
        possible_additions_filter += [exclude(w.startswith('name', 'market'))]
        possible_additions_filter += [w.doesnt_contain_any('name', ['production mix'])]
        possible_additions_filter += [w.equals('location', g[1])]
        possible_additions_filter += [w.doesnt_contain_any('name', names)]

        if not include_transport:
            possible_additions_filter += [w.doesnt_contain_any('name', ['transport'])]

        possibles = list(w.get_many(database.db, *possible_additions_filter))

        if len(possibles) > 0:
            result.extend(possibles)
            # result_dict[g] = possibles

    return result  # , result_dict


def get_input_processes_to_market(process, database):
    reference_product = w.reference_product(process)['product']

    return get_processes_from_exchanges(process, database, reference_product)


class FuturaMarket:
    def __init__(self, market, database):
        self.market = market
        self.database = database
        self.processes = get_input_processes_to_market(market, database)
        self.process_dict = {x['name']: {'process': x, 'production volume': w.reference_product(x)['production volume']}
                             for x in self.processes}

    def __repr__(self):
        return "FuturaMarket for {}\n\n{}".format(self.market['name'], str(dict(self.sorted_percentages)))

    @property
    def production_volumes(self):
        return [x['production volume'] for k, x in self.process_dict.items()]

    @property
    def total_production(self):
        return sum(self.production_volumes)

    @property
    def percentages(self):
        return {k: round(v['production volume'] / self.total_production, 4) for k, v in self.process_dict.items()}

    @property
    def sorted_percentages(self):
        sorted_x = sorted(self.percentages.items(), key=lambda kv: kv[1], reverse=True)
        sp = OrderedDict(sorted_x)
        df = pd.DataFrame(sorted_x, columns=['item', 'percentage'])
        df = df.set_index('item')
        # df = df.style.format({'percentage': '{0:.2%}'})
        return df

    @property
    def plot(self):
        return self.sorted_percentages.plot(kind='pie', y='percentage', legend=None)

    def get_pv(self, process_name):
        return self.process_dict[process_name]['production volume']

    def set_pv(self, process_name, new_pv):
        self.process_dict[process_name]['production volume'] = new_pv

    def add_pv(self, process_name, new_pv):
        self.process_dict[process_name]['production volume'] += new_pv

    def subtract_pv(self, process_name, new_pv):
        self.process_dict[process_name]['production volume'] -= new_pv

    def transfer_pv(self, from_name, to_name, factor=None, amount=None):

        assert any([factor, amount]), "you need to set either a factor or an amount"
        assert not all([factor, amount]), "you can't set a factor and an amount, choose one"

        from_pv = self.get_pv(from_name)

        if amount:
            assert amount <= from_pv, "you can't transfer more pv than is available"
            self.subtract_pv(from_name, amount)
            self.add_pv(to_name, amount)

        elif factor:
            assert 0 <= factor <= 1, "factor must be between 0 and 1"
            transfer_amount = from_pv*factor
            self.subtract_pv(from_name, transfer_amount)
            self.add_pv(to_name, transfer_amount)

    def rewrite_pvs(self):
        for name, process in self.process_dict.items():
            if w.reference_product(process['process'])['production volume'] != process['production volume']:
                w.reference_product(process['process'])['production volume'] = process['production volume']

    def relink(self):
        self.rewrite_pvs()
        update_technosphere_exchanges_from_pvs(self.market, self.database)

    def add_alternative_exchanges(self, include_transport=False):
        possibles = find_possible_additional_market_exchanges(self.market, self.database, include_transport)
        for p in possibles:
            add_exchange_to_activity(self.market, p)

        self.processes = get_input_processes_to_market(self.market, self.database)

        for x in self.processes:
            if x['name'] not in self.process_dict.keys():
                self.process_dict[x['name']] = {'process': x,
                                                'production volume': w.reference_product(x)['production volume']}

