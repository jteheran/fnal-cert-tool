import logging
from urlparse import urljoin

import requests

from ExceptionDefinitions import *

logger = logging.getLogger(__name__)

class InCommonApiClient:

    def __init__(self, base_url, api_timeout):
        """Setting up all the parameters used by the class

        Args:
            base_url (string): Will be used to connect to the InCommonAPI
        """
        
        self.base_url = base_url
        self.api_timeout = api_timeout
    
    def post_request(self, url, headers, data):
        """
        Args:
            url (string): url to send the request
            data (json):body containing information
            headers (json): additional headers to complete the request
        """
        
        url = urljoin(self.base_url, url)
        
        try:
            post_response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=int(self.api_timeout)
            )
            post_response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise AuthenticationFailureException(post_response.status_code, exc)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as exc:
            raise ConnectionFailureException(exc)

        return post_response

    def get_request(self, url, headers):
        """
        Args:
            url (string): url to send the request
            headers (json): additional headers to complete the request
        """
        url = urljoin(self.base_url, url)
        
        try:
            get_response = requests.get(
                url,
                headers=headers,
                timeout=int(self.api_timeout)
            )
            get_response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise AuthenticationFailureException(get_response.status_code, exc)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as exc:
            raise ConnectionFailureException(exc)

        return get_response

