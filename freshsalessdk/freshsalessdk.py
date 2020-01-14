import requests
import json

class API:
    def __init__(self, domain, api_key):
        self.domain = domain
        self.api_key = api_key

    def _get(self, params, path):
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


class Contacts(API):
    def __init__(self, domain, api_key):
        super().__init__(domain=domain, api_key=api_key)

    def get_views(self):
        return self._get(path='/contacts/filters', params={})['filters']

    def get_all_generator(self, view_id):
        raise NotImplementedError('not implemented')

    def get_all(self, view_id):
        return list(self.get_all_generator(view_id=view_id))
    
    def get(self, contact_id):
        raise NotImplementedError('not implemented')

    def get_activities(self, contact_id):
        raise NotImplementedError('not implemented')

class Accounts(API):
    def __init__(self, domain, api_key):
        super().__init__(domain=domain, api_key=api_key)

    def get_views(self):
        raise NotImplementedError('not implemented')

    def get_all_generator(self, view_id):
        raise NotImplementedError('not implemented')

    def get_all(self, view_id):
        return list(self.get_all_generator(view_id=view_id))
    
    def get(self, account_id):
        raise NotImplementedError('not implemented')


class Deals(API):
    def __init__(self, domain, api_key):
        super().__init__(domain=domain, api_key=api_key)

    def get_views(self):
        raise NotImplementedError('not implemented')

    def get_all_generator(self, view_id):
        raise NotImplementedError('not implemented')

    def get_all(self, view_id):
        return list(self.get_all_generator(view_id=view_id))
    
    def get(self, account_id):
        raise NotImplementedError('not implemented')

class FreshsalesSDK:
    def __init__(self, domain, api_key):
        self.contacts = Contacts(domain=domain, api_key=api_key)
        self.accounts = Accounts(domain=domain, api_key=api_key)
        self.deals = Deals(domain=domain, api_key=api_key)