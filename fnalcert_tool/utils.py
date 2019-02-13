import textwrap
import traceback

#Code borrowed from https://github.com/opensciencegrid/osg-pki-tools/blob/v2.1.4/osgpkitools/OSGPKIUtils.py
#Author Brian Lin - blin@cs.wisc.edu


def charlimit_textwrap(string):
    """This function wraps up the output to 80 characters. Accepts string and print the wrapped output"""

    list_string = textwrap.wrap(str(string), width=80)
    for line in list_string:
        print(line)
    return


def print_exception_message(exc):
    """Checks if the str representation of the exception is empty or not
    if empty, it prints an generic error message stating the type of exception
    and traceback.
    """

    if str(exc) != "":
        charlimit_textwrap("Got an exception %s" % exc.__class__.__name__)
        charlimit_textwrap(exc)
        #charlimit_textwrap('Please report the bug to %s.' % HELP_EMAIL)
    else:
        handle_empty_exceptions(exc)

def handle_empty_exceptions(exc):
    """The method handles all empty exceptions and displays a meaningful message and
    traceback for such exceptions."""

    print(traceback.format_exc())
    charlimit_textwrap('Encountered exception of type %s' % exc.__class__.__name__)
    #charlimit_textwrap('Please report the bug to %s.' % HELP_EMAIL)

def format_csr(csr):
    """Extract the base64 encoded string from the contents of a CSR"""
    return csr.replace('-----BEGIN CERTIFICATE REQUEST-----\n', '')\
              .replace('-----END CERTIFICATE REQUEST-----\n', '')\
              .replace('\n', '')

class Cert(object):

    KEY_LENGTH = 2048
    PUB_EXPONENT = 0x10001

    def __init__(self, common_name, output_dir=None, altnames=None, email=None):
        """Create a certificate request (stored in the x509request attribute) and associated key file that is written to
        a temporary location (stored in the newkey attribute). It is up to the caller to write_pkey or clean up the
        temporary keys

        This function accepts the CN and final path for the key as well as optional list of subject alternative names
        and optional requestor e-mail.  """
        escaped_common_name = common_name.replace('/', '_') # Remove / from service requests for writing keys
        self.keypair = RSA.gen_key(self.KEY_LENGTH,
                                   self.PUB_EXPONENT,
                                   self.callback)

        if not output_dir:
            output_dir = os.getcwd()
        self.final_keypath = os.path.join(output_dir, escaped_common_name + '-key.pem')
        temp_key = tempfile.NamedTemporaryFile(dir=output_dir, delete=False)
        self.newkey = temp_key.name

        # The message digest shouldn't matter here since we don't use
        # PKey.sign_*() or PKey.verify_*() but there's no harm in keeping it and
        # it ensures a strong hashing algo (default is sha1) if we do decide to
        # sign things in the future
        self.pkey = EVP.PKey(md='sha256')
        self.pkey.assign_rsa(self.keypair)
        self.keypair.save_key(self.newkey, cipher=None)
        temp_key.close()

        self.x509request = X509.Request()
        x509name = X509.X509_Name()

        x509name.add_entry_by_txt(  # common name
            field='CN',
            type=MBSTRING_ASC,
            entry=common_name,
            len=-1,
            loc=-1,
            set=0,
            )
        if email:
            x509name.add_entry_by_txt(  # pkcs9 email address
                field='emailAddress',
                type=MBSTRING_ASC,
                entry=email,
                len=-1,
                loc=-1,
                set=0,
                )

        self.x509request.set_subject_name(x509name)

        if altnames:
            extension_stack = X509.X509_Extension_Stack()
            extension = X509.new_extension('subjectAltName',
                                           ", ".join(['DNS:%s' % name for name in altnames]))
            extension.set_critical(1)
            extension_stack.push(extension)
            self.x509request.add_extensions(extension_stack)

        self.x509request.set_pubkey(pkey=self.pkey)
        self.x509request.set_version(0)
        self.x509request.sign(pkey=self.pkey, md='sha256')

    def callback(self, *args):
        return None

    def write_pkey(self, keypath=None):
        """Move the instance's newkey to keypath, backing up keypath to keypath.old if necessary"""
        if not keypath:
            keypath = self.final_keypath
        # Handle already existing key file...
        safe_rename(keypath)
        os.rename(self.newkey, keypath)

    def base64_csr(self):
        """Extract the base64 encoded string from the contents of a certificate signing request"""
        return format_csr(self.x509request.as_pem())
