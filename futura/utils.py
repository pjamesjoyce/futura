#import wurst as w
from . import w

import pprint
from wurst.searching import exclude


def fix_unset_technosphere_and_production_exchange_locations(db, matching_fields=('name', 'unit')):

    """
    Utility function from wurst publication supplementary materials to fix unset technosphere and production
    exchanges.
    Database is fixed in place, function returns nothing

    :param db: database to fix
    :param matching_fields: fields on which to search for exchanges
    :return: nothing
    """
    for ds in db:
        for exc in ds['exchanges']:
            if exc['type'] == 'production' and exc.get('location') is None:
                exc['location'] = ds['location']
            elif exc['type'] == 'technosphere' and exc.get('location') is None:
                locs = find_location_given_lookup_dict(db,
                                                       {k: exc.get(k) for k in matching_fields})
                if len(locs) == 1:
                    exc['location'] = locs[0]
                else:
                    print("No unique location found for exchange:\n{}\nFound: {}".format(
                        pprint.pformat(exc), locs
                    ))


def find_location_given_lookup_dict(db, lookup_dict):
    """
    Utility function for the utility function above
    :param db: database to fix
    :param lookup_dict: dictionary of locations
    :return: list of locations
    """
    return [x['location'] for x in w.get_many(db, *[w.equals(k, v) for k, v in lookup_dict.items()])]


def remove_nones(db):
    exists = lambda x: {k: v for k, v in x.items() if v is not None}

    for ds in db:

        ds['exchanges'] = [exists(exc) for exc in ds['exchanges']]


def fix_products_and_locations_external(external_data, existing_data):
    external_db_set = set([a['database'] for a in external_data])
    internal_db_set = set([a['database'] for a in existing_data])
    # print(external_db_set)
    # print(internal_db_set)

    # assert 0
    product_exchange_count = 0
    location_exchange_count = 0
    location_activity_count = 0
    production_volume_count = 0

    for a in external_data:

        # add missing location to activity
        if not 'location' in a.keys():
            a['location'] = 'GLO'
            location_activity_count += 1
            # print('Added GLO location to {}'.format(a['name']))

        for e in [x for x in a['exchanges'] if x['type'] != 'biosphere']:

            # add missing location

            if e['input'][0] in external_db_set:
                look_in = external_data
            elif e['input'][0] in internal_db_set:
                look_in = existing_data
            else:
                # print(e['input'][0])
                continue

            this_input = e['input']
            # print(this_input)

            input_filter = [w.equals('database', this_input[0])]
            input_filter += [w.equals('code', this_input[1])]

            try:
                this_input = w.get_one(look_in, *input_filter)
            except w.errors.NoResults:
                assert 0, "{} not found".format(this_input)

            if not 'product' in e.keys():
                e['product'] = this_input['reference product']
                product_exchange_count += 1

            if not 'location' in e.keys():
                if 'location' in this_input.keys():
                    e['location'] = this_input['location']
                    # print('Added {} location to exchange {} of {}'.format(this_input['location'], e['name'], a['name']))
                else:
                    e['location'] = 'GLO'
                    # print('Added GLO location to exchange {} of {}'.format(e['name'], a['name']))

                location_exchange_count += 1

            # add missing production volumes (default to zero)

            if e['type'] == 'production':
                if 'production volume' not in e.keys():
                    e['production volume'] = 0
                    production_volume_count += 1
                    # print('Added default zero production volume to exchange of {} from {}'.format(e['product'], a['name']))

    print("Location data added to {} activities".format(location_activity_count))
    print("Location data added to {} exchanges".format(location_exchange_count))
    print("Product data added to {} exchanges".format(product_exchange_count))
    print("Default (zero) production volume data added to {} production exchanges".format(production_volume_count))


def create_filter_from_description(description):

    wurst_functions = {
        'equals': w.equals,
        'contains': w.contains,
        'startswith': w.startswith,
        'either': w.either,
        'exclude': exclude,
        'doesnt_contain_any': w.doesnt_contain_any,
    }

    def create_filter(detail):

        if detail['filter'] in ['either', 'exclude']:
            sub_filter = []

            for x in detail['args']:
                sub_filter += create_filter(x)

            return [wurst_functions[detail['filter']](*sub_filter)]

        return [wurst_functions[detail['filter']](*detail['args'])]

    this_filter = []

    for x in description:
        this_filter += create_filter(x)

    return this_filter
