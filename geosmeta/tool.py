# Copyright (c) The University of Edinburgh, 2014.
#
import requests
from hashlib import sha1
import hmac
import sys
import util
import json

class HMACAuth(requests.auth.AuthBase):
    """Class defining HMAC authentication

    This extends the base authentication class from the requests package.
    """

    def __init__(self, username, secret, message):
        """Configuration authentication.

        :param username: Public identity of user
        :type username: str
        :param secret: Shared secret known to user and server to sign messages
        :type secret: str
        :param message: Message to be signed
        :type message: str
        """
        self.username = username
        self.secret = secret
        self.message = message

    def __call__(self, request):
        """Call the authentication method for the given request.

        This computes a hash for the given message and then adds that
        hash to the Authorization header with the public identity.

        Currently only the message is hashed.

        A more sophisticated implementation could use some of the
        HTTP headers too.

        :param request: request to add authentication information to.
        :type request: request object
        """
        # Compute HMAC hash
        hmac_hash = hmac.new(bytes(self.secret, 'utf-8'),
                             bytes(self.message,  'utf-8'),
                             sha1).hexdigest()
        # Construct authorization header
        header = str(self.username)
        header += ":"
        header += hmac_hash
        # Note that this is using the HTTP standard Authorization
        # header (not authentication!)
        request.headers['Authorization'] = header
        # Finally add the new header to the request object
        return request


class Tool(object):
    """Class encapsulating GeosMeta Tool operations"""

    def __init__(self, configFilePath = None):
        """Constructor

        :param configFilePath: The location of the geosmeta configuration
                               file. If not present this defaults to
                               $HOME/.geosmeta/geosmeta.cfg
        :type configFilePath: str
        """

        self.config = util.GeosMetaConfig(configFilePath)

        # Setup logging for the tool
        try:
            self.setupLogging()
        except Exception as err:
            sys.stderr.write('Error configuring logging:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)

    def setupLogging(self):
        """Setup Logging based on configuration file options"""
        self.logger = util.setupLogging(self.config.logfile,
                                        self.config.loglevel,
                                        __name__)
        self.logger.debug('Logging configured')

    def endpoint(self, resource):
        """Returns the endpoint of a given resource

        :param resource: resource to calculate endpoint for
        :type resource: str
        :returns: endpoint string
        :rtype: str
        """
        return '%s/%s' % (self.config.serverURI, resource)

    def getAuthentication(self, message):
        """Returns the authentication object for a given message

        :param message: message to authenticate
        :type message: str
        :returns: authentication object
        """
        return HMACAuth(self.config.username,
                        self.config.secret,
                        message)

    def performGet(self, resource, message, params=None,hdr_ext=None):
        """Performs a GET for the given resource, with the message specified

        :param resource: resource to perform GET on
        :type resource: str
        :param message: message to send
        :type message: str
        :param params: query parameters
        :type params: dictionary
        :type hdr_ext:  extend header - e.g. project name, selectedfields.
        :returns: response
        """
#        import pdb;pdb.set_trace()
        auth = self.getAuthentication(message)

             # note setting headers in the next line hsa effect
             # of appending to the auth header information, not 
             # overwriting
        r = requests.get(self.endpoint(resource), auth=auth,
                         params=params, headers=hdr_ext) # , verify=False)
        return r


    def performPost(self, resource, messageDict):
        """Performs a POST for the given resource, with the message specified

        :param resource: resource to perform POST on
        :type resource: str
        :param messageDict: dict with message to send
        :type : Dict
        :returns: response
        """
        headers = {'Content-Type': 'application/json'}
        message=json.dumps(messageDict)
        auth = self.getAuthentication(message)
        return requests.post(self.endpoint(resource),
                             message,
                             headers=headers,
                             auth=auth)

    def performPatch(self, resource, message, etag):
        """Performs a PATCH for the given resource, with the message specified

        :param resource: resource to perform PATCH on
        :type resource: str
        :param message: message to send
        :type message: str
        :returns: response
        """
        #headers = {'Content-Type': 'application/json'}
        headers = {'If-Match': etag,
                   'Content-Type': 'application/json'}
        auth = self.getAuthentication(message)
        return requests.patch(self.endpoint(resource),
                             message,
                             headers=headers,
                             auth=auth)


    def performDelete(self, resource, message):
        """Performs a POST for the given resource, with the message specified

        :param resource: resource to perform POST on
        :type resource: str
        :param message: message to send
        :type message: str
        :returns: response
        """
        auth = self.getAuthentication(message)
        return requests.delete(self.endpoint(resource), auth=auth)
