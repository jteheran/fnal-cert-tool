#!usr/bin/python

import getpass
import os
import sys
import ssl 

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import SSLContext
from ssl import SSLError

from ExceptionDefinitions import *

class SSLContextAdapter(HTTPAdapter):
    """HTTPAdapter for requests.Session to use with usercert and userkey
       SSLContext is reused by all connections from the pool
    """
    def __init__(self, *args, **kwargs):
        usercert = kwargs.pop('usercert', None)
        userkey = kwargs.pop('userkey', None)

        self.ssl_context = get_ssl_context(usercert, userkey)

        super(SSLContextAdapter, self).__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        if self.ssl_context:
            kwargs['ssl_context'] = self.ssl_context
        return super(SSLContextAdapter, self).init_poolmanager(*args, **kwargs)


def get_ssl_context(usercert, userkey):
    """ This function sets the ssl context by accepting the passphrase
    and validating it for user private key and his certificate
    INPUT
        cert: Filename for user certificate.
        key: Filename for private key of user.

    OUTPUT
        SSLContext object for the Requests Session.
    """
    pass_str = 'Please enter the pass phrase for'

    for _ in range(0, 2): # allow two password attempts
        def prompt_for_password():
            return getpass.getpass(pass_str+" '%s':" % userkey)

        ssl_context = SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.options |= ssl.OP_NO_SSLv2
        ssl_context.options |= ssl.OP_NO_SSLv3
        
        try:
            ssl_context.load_cert_chain(usercert, userkey, password=prompt_for_password)
            return ssl_context
        except SSLError, exc:
            if 'bad password read' in exc:
                pass_str = 'Incorrect password. Please enter the password again for'
            else:
                raise

                    
    # if we fell off the loop, the passphrase was incorrect twice
    raise BadPassphraseException('Incorrect passphrase. Attempt failed twice. Exiting script')

