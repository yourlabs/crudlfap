import copy
import urllib


def pagination_filter_params(data):
    data = copy.deepcopy(data)
    if 'page' in data:
        data.pop('page')
    return urllib.parse.urlencode(data)
