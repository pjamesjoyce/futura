import wurst as w
import pprint


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