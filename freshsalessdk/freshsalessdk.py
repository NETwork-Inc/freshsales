import requests
import json
import time
import copy
import logging

logger = logging.getLogger(__name__)

class APIBase:
    def __init__(self, resource_type, domain, api_key, resource_type_singular=None, default_params={}):
        self.resource_type = resource_type
        self.resource_type_singular = resource_type_singular
        # best guess is to remove last letter
        if self.resource_type_singular is None:
            self.resource_type_singular = self.resource_type[0:-1]
        self.domain = domain
        self.api_key = api_key
        self.default_params = default_params

    def _get_generic(self, path, params={}):
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
        api_params = copy.deepcopy(self.default_params)

        for k in params:
            # ignore all unused params
            if not params[k] is None:
                p = params[k]

                # convert boolean to lowercase string
                if isinstance(p, bool):
                    p = str(p).lower()

                api_params[k] = p

        api_path = f'https://{self.domain}.freshsales.io{path}'
        logger.debug('calling get %s passing params %s', api_path, api_params)
        response = requests.get(
            url=api_path, 
            headers=api_headers, 
            params=api_params
        )
        # raise exception if not 200
        response.raise_for_status()

        res = json.loads(response.text)
#        logger.debug('res = %s', res)
        return res

    def _get_views(self):
        return self._get_generic(path=f'/{self.resource_type}/filters')['filters']

    @staticmethod
    def _find_obj_by_id(objs, id):
        for o in objs:
            if o['id'] == id:
                return o
        return None

    def _normalize(self, obj, container):
        """
        Every class should normalize it if it wants to do any normalization of the object.
        E.g. contact object has an owner_id and list of users is in the container. We can fetch
        the owner object and attach it to the contact object which makes things easier for the client
        """
        pass


    def _get_all_generator(self, view_id, limit=None):
        page = 1
        num = 0
        while True:
            start_time = time.time()
            params = {'page': page}
            res = self._get_generic(path=f'/{self.resource_type}/view/{view_id}', params=params)
            total_pages = res['meta']['total_pages']
            end_time = time.time()
            logger.debug(f'got page %s of %s in %s seconds', page, total_pages, end_time-start_time)
    
            objs = res[self.resource_type]
            for obj in objs:
                self._normalize(obj=obj, container=res)
                num = num + 1
                if limit and num > limit:
                    return
                yield obj

            page = page + 1
            if page > total_pages:
                break

    def _get_by_id(self, id):
        res = self._get_generic(path=f'/{self.resource_type}/{id}')
        v = res[self.resource_type_singular]
        self._normalize(obj=v, container=res)
        return v

    def get_views(self):
        return self._get_views()

    def get_all_generator(self, view_id, limit=None):
        return self._get_all_generator(view_id=view_id, limit=limit)

    def get_all(self, view_id, limit=None):
        return list(self.get_all_generator(view_id=view_id, limit=limit))
    
    def get(self, id):
        return self._get_by_id(id=id)


class Contacts(APIBase):
    def __init__(self, domain, api_key):
        default_params = {'include': 'sales_accounts,appointments,owner', 'sort': 'updated_at', 'sort_type': 'desc'}
        super().__init__(domain=domain, api_key=api_key, resource_type='contacts', default_params=default_params)

    def _normalize(self, obj, container):
        users = []
        sales_accounts = []
        if 'users' in container:
            users = container['users']
        if 'owner_id' in obj:
            owner = APIBase._find_obj_by_id(objs=users, id=obj['owner_id'])
            obj['owner'] = owner

    def get_activities(self, id):
        return self._get_generic(f'/contacts/{id}/activities')['activities']
    
    def get_appointments(self, id):
        return self._get_generic(f'/contacts/{id}/appointments')['appointments']


class Accounts(APIBase):
    def __init__(self, domain, api_key):
        default_params = {'include': 'appointments,owner', 'sort': 'updated_at', 'sort_type': 'desc'}
        super().__init__(domain=domain, api_key=api_key, resource_type='sales_accounts', default_params=default_params)

    def _normalize(self, obj, container):
        users = []
        sales_accounts = []
        if 'users' in container:
            users = container['users']
        if 'owner_id' in obj:
            owner = APIBase._find_obj_by_id(objs=users, id=obj['owner_id'])
            obj['owner'] = owner

class Deals(APIBase):
    def __init__(self, domain, api_key):
        default_params = {'include': 'sales_account,appointments,owner,deal_stage', 'sort': 'updated_at', 'sort_type': 'desc'}
        super().__init__(domain=domain, api_key=api_key, resource_type='deals', default_params=default_params)

    def _normalize(self, obj, container):
        users = []
        sales_accounts = []
        deal_stages = []
        if 'users' in container:
            users = container['users']
        if 'sales_accounts' in container:
            sales_accounts = container['sales_accounts']
        if 'deal_stages' in container:
            deal_stages = container['deal_stages']
        if 'owner_id' in obj:
            owner = APIBase._find_obj_by_id(objs=users, id=obj['owner_id'])
            obj['owner'] = owner
        if 'sales_account_id' in obj:
            sales_account = APIBase._find_obj_by_id(objs=sales_accounts, id=obj['sales_account_id'])
            obj['sales_account'] = sales_account
        if 'deal_stage_id' in obj:
            deal_stage = APIBase._find_obj_by_id(objs=deal_stages, id=obj['deal_stage_id'])
            obj['deal_stage'] = deal_stage

class FreshsalesSDK:
    def __init__(self, domain, api_key):
        self.contacts = Contacts(domain=domain, api_key=api_key)
        self.accounts = Accounts(domain=domain, api_key=api_key)
        self.deals = Deals(domain=domain, api_key=api_key)