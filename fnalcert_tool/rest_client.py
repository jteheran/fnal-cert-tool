import logging
from urlparse import urljoin

import requests

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
        #
        url = urljoin(self.base_url, url)

        try:
            post_response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=int(self.api_timeout)
            )
        except requests.exceptions.RequestException as exc:
            logger.error(
                'Could not connect to InCommon API',
                exc_info=True,
                extra={
                    'url': url,
                    'data': data,
                    'api_timeout': self.api_timeout,
                },
            )

        return post_response

    def get_request(self, url, headers):
        """

        Args:
            url (string): url to send the request
        """
        url = urljoin(self.base_url, url)
        try:
            get_response = requests.get(
                url,
                headers=headers,
                timeout=int(self.api_timeout)
            )
        except requests.exceptions.RequestException as exc:
            logger.error(
                'Could not connect to InCommon API',
                exc_info=True,
                extra={
                    'url': url,
                    'api_timeout': self.api_timeout,
                },
            )

        return get_response.text



