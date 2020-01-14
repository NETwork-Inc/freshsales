
class FreshsalesSDKError(Exception):
    """The base exception class for FreshsalesSDK.

    Parameters:
        msg (str): Short description of the error.
        response: Error response from the API call.
    """
    pass