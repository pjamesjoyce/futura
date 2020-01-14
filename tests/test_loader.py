from futura.loader import FuturaLoader
from futura.technology import add_technology_to_database, fix_ch_only_processes, regionalise_multiple_processes
from futura import w
from futura.utils import create_filter_from_description
from futura.constants import ASSET_PATH
from futura.markets import FuturaMarket, alter_production_volumes

from collections import deque
import pandas as pd
import os
import pytest


def test_loader(loader):

    print('checking loader fixture')
    print(loader)
    assert isinstance(loader, FuturaLoader)


def test_add_technology(loader):

    technology_file = os.path.join(ASSET_PATH, 'lci-Carma-CCS-base-GLO2.xlsx')
    database = loader.database

    print('Has the loader kept its database?')
    print(loader.database)
    print(len(loader.database.db))

    original_db_size = len(loader.database.db)

    add_technology_to_database(database, technology_file)
    fix_ch_only_processes(database)

    assert len(loader.database.db) > original_db_size


def test_regionalisation(loader):

    database = loader.database

    original_database_size = len(database.db)

    locations = ['GB']
    base_activity_filter = [{'filter': 'equals', 'args': ['database', 'Carma CCS']},
                             {'filter': 'equals', 'args': ['unit', 'kilowatt hour']},
                             {'filter': 'either', 'args': [
                               {'filter': 'contains', 'args': ['name', 'hard coal']},
                               {'filter': 'contains', 'args': ['name', 'Hard coal']}
                             ]},
                             {'filter': 'equals', 'args': ['location', 'GLO']}]
    progress_message = 'coal CCS for GB'

    regionalise_multiple_processes(database, locations, base_activity_filter, progress_message)

    intermediate_database_size = len(database.db)

    assert intermediate_database_size > original_database_size

    gb_activity_filter = [{'filter': 'equals', 'args': ['database', 'Carma CCS']},
                            {'filter': 'equals', 'args': ['unit', 'kilowatt hour']},
                            {'filter': 'either', 'args': [
                                {'filter': 'contains', 'args': ['name', 'hard coal']},
                                {'filter': 'contains', 'args': ['name', 'Hard coal']}
                            ]},
                            {'filter': 'equals', 'args': ['location', 'GB']}]

    gb = create_filter_from_description(gb_activity_filter)

    gb_list = list(w.get_many(database.db, *gb))

    assert gb_list

    locations = ['DE']
    base_activity_filter = [{'filter': 'equals', 'args': ['database', 'Carma CCS']},
                            {'filter': 'equals', 'args': ['unit', 'kilowatt hour']},
                            {'filter': 'either', 'args': [
                                {'filter': 'contains', 'args': ['name', 'lignite']},
                                {'filter': 'contains', 'args': ['name', 'Lignite']}
                            ]},
                            {'filter': 'equals', 'args': ['location', 'GLO']}]
    progress_message = 'lignite CCS for DE'

    regionalise_multiple_processes(database, locations, base_activity_filter, progress_message)

    final_database_size = len(database.db)

    assert final_database_size > intermediate_database_size

    de_activity_filter = [{'filter': 'equals', 'args': ['database', 'Carma CCS']},
                          {'filter': 'equals', 'args': ['unit', 'kilowatt hour']},
                          {'filter': 'either', 'args': [
                              {'filter': 'contains', 'args': ['name', 'lignite']},
                              {'filter': 'contains', 'args': ['name', 'Lignite']}
                          ]},
                          {'filter': 'equals', 'args': ['location', 'DE']}]

    de = create_filter_from_description(de_activity_filter)

    de_list = list(w.get_many(database.db, *de))

    assert de_list


@pytest.fixture(scope='module')
def market(loader):

    database = loader.database

    market_filter_desc = [{'filter': 'equals', 'args': ['unit', 'kilowatt hour']},
                          {'filter': 'startswith', 'args': ['name', 'market']},
                          {'filter': 'contains', 'args': ['name', 'high']},
                          {'filter': 'equals', 'args': ['location', 'GB']}]

    market_filter = create_filter_from_description(market_filter_desc)

    market_activity = w.get_one(database.db, *market_filter)

    return FuturaMarket(market_activity, database)

def test_market_basics(loader, market):

    assert isinstance(market, FuturaMarket)

    assert isinstance(market.sorted_percentages, pd.DataFrame)

    assert market.plot
    print(market)
    assert market.production_volumes
    assert market.percentages

    assert market.total_production > 0


def test_market_alternative_exchanges(market):

    original_exchanges = len(market.processes)
    market.add_alternative_exchanges()

    assert len(market.processes) > original_exchanges


def test_transfer_pv_factor(market):
    from_name = 'electricity production, hard coal'
    to_name = 'Electricity, at power plant/hard coal, post, pipeline 200km, storage 1000m/2025'
    factor = 0.5

    original_from_pv = market.process_dict[from_name]['production volume']
    original_to_pv = market.process_dict[to_name]['production volume']

    assert original_to_pv == 0

    market.transfer_pv(from_name, to_name, factor=factor)

    # the original pv is half of what it used to be
    assert market.process_dict[from_name]['production volume'] == original_from_pv - (original_from_pv * factor)

    # the new pv equals half of the old pv
    assert market.process_dict[to_name]['production volume'] == original_to_pv + (original_from_pv * factor)


def test_transfer_pv_amount(market):
    from_name = 'electricity production, hard coal'
    to_name = 'Electricity, at power plant/hard coal, post, pipeline 200km, storage 1000m/2025'
    amount = 1

    original_from_pv = market.process_dict[from_name]['production volume']
    original_to_pv = market.process_dict[to_name]['production volume']

    market.transfer_pv(from_name, to_name, amount=amount)

    # the original pv is less than what it used to be
    assert market.process_dict[from_name]['production volume'] == original_from_pv - amount

    # the new pv is more than the old pv
    assert market.process_dict[to_name]['production volume'] == original_to_pv + amount


def test_alter_pvs(market):

    old_pvs = [w.reference_product(x)['production volume'] for x in market.processes]
    pv_deque = deque(old_pvs)
    pv_deque.rotate()

    alter_production_volumes(market.processes, list(pv_deque))

    new_pvs = [w.reference_product(x)['production volume'] for x in market.processes]

    mismatch = False

    for n, i in enumerate(old_pvs):
        if new_pvs[n] != i:
            mismatch = True
            break

    assert mismatch


def test_set_pv(market):
    market.set_pv('electricity production, oil', 0)

    assert market.process_dict['electricity production, oil']['production volume'] == 0

def test_relink(market, loader):

    market_filter_desc = [{'filter': 'equals', 'args': ['unit', 'kilowatt hour']},
                          {'filter': 'startswith', 'args': ['name', 'market']},
                          {'filter': 'contains', 'args': ['name', 'high']},
                          {'filter': 'equals', 'args': ['location', 'GB']}]

    market_filter = create_filter_from_description(market_filter_desc)

    market_activity = w.get_one(loader.database.db, *market_filter)

    original_exchange_dict = {x['name']: x['amount'] for x in market_activity['exchanges']}

    print(original_exchange_dict)

    market.relink()

    market_activity = w.get_one(loader.database.db, *market_filter)

    new_exchange_dict = {x['name']: x['amount'] for x in market_activity['exchanges']}

    for k, v in original_exchange_dict.items():
        if new_exchange_dict[k] != v:
            mismatch = True
            break

    assert mismatch


