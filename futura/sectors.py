import brightway2 as bw
#import wurst as w
from . import w

electricity_markets = [w.contains('unit', 'kilowatt hour')]
electricity_markets += [w.contains('name', 'electricity')]

cement_filter = [w.contains('name', 'cement')]
#cement_filter += [w.doesnt_contain_any('name','factory')]

def build_tree(activity, max_levels=2, amount=None, filters=[], seen_list=[], level=0):
    if amount is None:
        amount = 1

    if isinstance(activity, tuple):
        activity = bw.get_activity(activity)

    inputs = list(activity.technosphere())
    # print(list(inputs[0].keys()))
    # print(inputs[0]['flow'])

    include = list(w.get_many(inputs, *filters))
    include = [exc for exc in include if exc['input'][0] == activity['database']]
    duplicate = activity['code'] in seen_list

    if activity['name'].startswith('market'):
        activity_type = 'market'
    elif 'production' in activity['name']:
        activity_type = 'production'
    elif 'import' in activity['name']:
        activity_type = 'import'
    elif 'co-generation' in activity['name']:
        activity_type = 'cogeneration'
    else:
        activity_type = 'unknown'

    # inside = [exc for exc in inputs
    #          if exc['input'][0] == activity['database'] and exc['unit'] == 'kilowatt hour']

    if level <= max_levels and duplicate == False:
        technosphere = [
            build_tree(exc.input, max_levels, exc['amount'], filters, seen_list=seen_list + [activity['code']],
                       level=level + 1)
            for exc in include]
    else:
        technosphere = []

    return {
        'name': activity['name'],
        'location': activity['location'],
        'amount': amount,
        'children': technosphere,
        'id': activity['code'],
        'duplicate': duplicate,
        'type': activity_type,
    }