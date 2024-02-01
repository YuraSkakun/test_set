import copy
from urllib.parse import urlencode

import time


class QueryParamsInjectorMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        query_params = copy.deepcopy(request.GET)
        if 'page' in query_params:
            del query_params['page']
        request.query_params = urlencode(query_params)

        response = self.get_response(request)

        return response


class TimeLog:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        time1 = time.time()
        # print(f'Time before - {time1}')
        response = self.get_response(request)
        time2 = time.time()
        # print(f'Time after - {time2}')
        print(f'TimeLog - {time2 - time1}')
        return response
