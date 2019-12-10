from .regionalisation import *
from functools import partial
from . import log, warn
from .default_filters import *
from tqdm import tqdm
from .constants import FULL_CCS_FILE
from.utils import create_filter_from_description
from.proxy import WurstProcess


def add_technology_to_database(database, technology_file, funcs=None):

    assert type(database) == FuturaDatabase, "database needs to be a futura FuturaDatabase"

    if not funcs:
        funcs = []

    database.extract_excel_data(technology_file)

    for f in funcs:
        database = f(database)


def fix_ch_only_processes(database):

    if 'Carma CCS' in database.database_names:

        all_carma_filter_description = [{'filter': 'equals', 'args': ['database', 'Carma CCS']}]
        all_carma_filter_description += [{'filter': 'equals', 'args': ['location', 'GLO']}]

        all_carma_filter = create_filter_from_description(all_carma_filter_description)

        all_carma_list = [WurstProcess(x) for x in w.get_many(database.db, *all_carma_filter)]

        ch_list = []
        for l in all_carma_list:
            for e in l['exchanges']:
                if 'location' in e.keys():
                    if e['location'] == 'CH':
                        ch_list.append(e)

        ch_names_set = set([x['name'] for x in ch_list])
        ch_only_list = list(ch_names_set)

        for x in ch_only_list:
            found = [WurstProcess(x) for x in w.get_many(database.db, *[w.contains('name', x)])]
            found_list = list(found)
            location_list = [l['location'] for l in found_list]

            if all(["GLO" not in location_list, "RoW" not in location_list]):
                ch_only_process = [WurstProcess(c) for c in found_list if c['location'] == 'CH'][0]
                create_regional_activities(ch_only_process, ['GLO'], database.db)
                log("Adding {} [{}]".format(ch_only_process['name'], ch_only_process['location']))

    return database



def regionalise_multiple_processes(database, locations, base_activity_filter, progress_message=None):

    if not callable(base_activity_filter[0]):
        print('Creating base_activity_filter from description')
        base_activity_filter = create_filter_from_description(base_activity_filter)

    base_activities = [WurstProcess(x) for x in w.get_many(database.db, *base_activity_filter)]

    code_list = []
    if not progress_message:
        progress_message = 'specified activities'

    print("Creating regionalised versions of {}...".format(progress_message))
    for a in tqdm(base_activities):
        code_list.extend(create_regional_activities(a, locations, database.db, relink_now=False))

    print("Relinking regionalised versions of {}...".format(progress_message))
    for x in tqdm(code_list):
        ds = w.get_one(database.db, *[w.equals('code', x[1])])

        if ds['name'].startswith('market'):
            exclusive = False
        else:
            exclusive = True

        if 'input' in w.reference_product(ds).keys():
            del w.reference_product(ds)['input']

        w.relink_technosphere_exchanges(ds,
                                        database.db,
                                        exclusive=exclusive,
                                        drop_invalid=False,
                                        biggest_first=False,
                                        contained=False,
                                        exclude=['UCTE'])
    return database


def regionalise_based_on_filters(database, location_filter, base_activity_filter, progress_message=None):

    location_list = list(w.get_many(database.db, *location_filter))
    if len(set([x['name'] for x in location_list])) != 1:
        warn("The location filter returns more than one process")

    locations = list(set([x['location'] for x in location_list]))

    return regionalise_multiple_processes(database, locations, base_activity_filter, progress_message)


add_hard_coal_ccs = partial(regionalise_based_on_filters,
                            location_filter=coal_location_filter,
                            base_activity_filter=hard_coal_ccs_filter,
                            progress_message='hard coal CCS activities')

add_lignite_ccs = partial(regionalise_based_on_filters,
                          location_filter=lignite_location_filter,
                          base_activity_filter=lignite_ccs_filter,
                          progress_message='lignite CCS activities')

add_natural_gas_ccs = partial(regionalise_based_on_filters,
                              location_filter=natural_gas_location_filter,
                              base_activity_filter=natural_gas_ccs_filter,
                              progress_message='natural gas CCS activities')

add_wood_ccs = partial(regionalise_based_on_filters,
                       location_filter=wood_location_filter,
                       base_activity_filter=wood_ccs_filter,
                       progress_message='wood CCS activities')

add_default_CCS_processes = partial(add_technology_to_database,
                                    technology_file=FULL_CCS_FILE,
                                    funcs=[
                                     fix_ch_only_processes,
                                     add_hard_coal_ccs,
                                     add_lignite_ccs,
                                     add_natural_gas_ccs,
                                     add_wood_ccs
                                    ])
