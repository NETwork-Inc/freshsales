import requests
import json
import time

class APIBase:
    def __init__(self, resource_type, domain, api_key, resource_type_singular=None):
        self.resource_type = resource_type
        self.resource_type_singular = resource_type_singular
        if self.resource_type_singular is None:
        # best guess is to remove last letter
            self.resource_type_singular = self.resource_type[0:-1]
        self.domain = domain
        self.api_key = api_key

    def _get(self, path, params={}):
        """Create a HTTP GET request.

        Parameters:
            params (dict): HTTP GET parameters for the wanted API.
            path (str): path for the wanted API. Should start with a '/'

        Returns:
            A response from the request (dict).
        """
        assert path is not None
        assert path.startswith('/')

        api_headers = {'Authorization': f'Token token={self.api_key}'}
        api_params = {}

        for k in params:
            # ignore all unused params
            if not params[k] is None:
                p = params[k]

                # convert boolean to lowercase string
                if isinstance(p, bool):
                    p = str(p).lower()

                api_params[k] = p

        response = requests.get(
            f'https://{self.domain}.freshsales.io{path}', 
            headers=api_headers, 
            params=api_params
        )
        # raise exception if not 200
        response.raise_for_status()

        result = json.loads(response.text)
        return result

    def _get_views(self):
        return self._get(path=f'/{self.resource_type}/filters', params={})['filters']

    @staticmethod
    def _find_owner(users, owner_id):
        for u in users:
            if u['id'] == owner_id:
                return u
        return None

    def _get_all_generator(self, view_id):
        page = 1
        while True:
            start_time = time.time()
            params = {'sort': 'updated_at', 'sort_type': 'desc', 'include': 'owner', 'page': page}
            res = self._get(path=f'/{self.resource_type}/view/{view_id}', params=params)
            total_pages = res['meta']['total_pages']
            users = res['users']
            end_time = time.time()
            print(f'got page {page} of {total_pages} in {end_time-start_time} seconds')
        
            objs = res[self.resource_type]
            for obj in objs:
                owner = APIBase._find_owner(users, obj['owner_id'])
                obj['owner'] = owner
                yield obj

            page = page + 1
            if page > total_pages:
                break

    def _get_by_id(self, id):
        params = {'include': 'owner'}
        res = self._get(path=f'/{self.resource_type}/{id}', params=params)
        users = res['users']
        v = res[self.resource_type_singular]
        owner = APIBase._find_owner(users, v['owner_id'])
        v['owner'] = owner
        return v

    def get_views(self):
        return self._get_views()

    def get_all_generator(self, view_id):
        return self._get_all_generator(view_id=view_id)

    def get_all(self, view_id):
        return list(self.get_all_generator(view_id=view_id))
    
    def get(self, id):
        return self._get_by_id(id=id)


class Contacts(APIBase):
    def __init__(self, domain, api_key):
        super().__init__(domain=domain, api_key=api_key, resource_type='contacts')

    def get_activities(self, id):
        return self._get(f'/contacts/{id}/activities')['activities']


class Accounts(APIBase):
    def __init__(self, domain, api_key):
        super().__init__(domain=domain, api_key=api_key, resource_type='sales_accounts')


class Deals(APIBase):
    def __init__(self, domain, api_key):
        super().__init__(domain=domain, api_key=api_key, resource_type='deals')


class FreshsalesSDK:
    def __init__(self, domain, api_key):
        self.contacts = Contacts(domain=domain, api_key=api_key)
        self.accounts = Accounts(domain=domain, api_key=api_key)
        self.deals = Deals(domain=domain, api_key=api_key)