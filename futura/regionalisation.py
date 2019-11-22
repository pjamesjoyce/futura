import wurst as w

from futura.wrappers import FuturaDatabase

import warnings

def create_regional_activities(base_activity, new_regions, db, production_volumes=None,
                               remove_production_from_original=True, relink_now = True):
    if production_volumes:
        assert len(production_volumes) == len(new_regions)
        total_production = 0

    geomatcher = w.geomatcher
    added_datasets = []
    code_list = []
    for n, region in enumerate(new_regions):
        if region not in geomatcher.contained(base_activity['location']):
            # print("{} not found within {}".format(region, base_activity['location']))
            #warnings.warn("{} not found within {}".format(region, base_activity['location']))
            pass
        new_ds = w.copy_to_new_location(base_activity, region)

        if 'input' in w.reference_product(new_ds).keys():
            # print("Deleting input from production exchange {} (from {})".format(
            # w.reference_product(new_ds)['name'], new_ds['name']))
            del w.reference_product(new_ds)['input']

        for e in w.technosphere(new_ds):
            if 'input' in e.keys():
                # print("Deleting input from {} (input to {})".format(e['name'], new_ds['name']))
                del e['input']

        if relink_now:
            new_ds = w.relink_technosphere_exchanges(new_ds,
                                                     db,
                                                     exclusive=True,
                                                     drop_invalid=False,
                                                     biggest_first=False,
                                                     contained=False,
                                                     exclude=['UCTE'])
        else:
            code_list.append((new_ds['database'], new_ds['code']))

        if production_volumes:
            pv = production_volumes[n]
            production_exchanges = [e for e in w.production(new_ds)]
            assert len(production_exchanges) == 1, "This process has multiple or no outputs - needs to have exactly 1"
            production_exchange = production_exchanges[0]

            production_exchange['production volume'] = pv

            total_production += pv

        added_datasets.append("{} [{}]".format(new_ds['name'], new_ds['location']))
        db.append(new_ds)

    if production_volumes:
        if remove_production_from_original:
            production_exchanges = [e for e in w.production(base_activity)]
            assert len(production_exchanges) == 1, "This process has multiple or no outputs - needs to have exactly 1"
            production_exchange = production_exchanges[0]
            original_pv = production_exchange['production volume']
            production_exchange['production volume'] -= total_production
            print("Changed production volume for {} [{}] from {} to {}".format(base_activity['name'],
                                                                               base_activity['location'], original_pv,
                                                                               production_exchange[
                                                                                   'production volume']))

    #print("Added the following datasets\n{}".format(added_datasets))
    if not relink_now:
        return code_list
