import logging
import requests 

from urlparse import urljoin
from requests import Session

from ExceptionDefinitions import *

logger = logging.getLogger(__name__)

class InCommonApiClient():

    def __init__(self, base_url, *args, **kwargs):
        """base_url and api_timeout

        Args:
            base_url (string): Will be used to connect to the InCommon API (cert-auth) 
        """
        
        self.base_url = base_url
        self.session = requests.Session()

    def getSession(self):
        return self.session

    def post_request(self, url, data):
        """
        Args:
            url (string): url to send the request
            data (json):body containing information
            headers (json): additional headers to complete the request
        """
        
        url = urljoin(self.base_url, url)
        
        logger.debug('posting to ' + url)
        logger.debug('data ' + str(data))

        try:
            post_response = self.session.post(url, json=data)

            logger.debug('post response text ' + str(post_response.text))

            post_response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise AuthenticationFailureException(post_response.status_code, exc)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as exc:
            raise ConnectionFailureException(exc)

        return post_response

    def get_request(self, url):
        """
        Args:
            url (string): url to send the request
            headers (json): additional headers to complete the request
        """
        url = urljoin(self.base_url, url)

        logger.debug('requesting to ' + url)

        try:
            get_response = self.session.get(url)

            logger.debug('get response text' + str(get_response.text))

            get_response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise AuthenticationFailureException(get_response.status_code, exc)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as exc:
            raise ConnectionFailureException(exc)

        return get_response

