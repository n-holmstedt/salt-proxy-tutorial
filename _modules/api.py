"""
05 - This is the execution module used to interact with the proxy
process. This custom module will be synced & loaded together with
the custom proxy module when the minion is accepted by the master.

This uses the public function 'get' in the proxy-module to call
specific endpoints hosted by the proxy device.

This module can be called from the salt cli by:

.. code-block:: bash

    salt '*' api.book id=1

You can do alterations in this module without restarting the
salt master/minon. After altering this module run: 

.. code-block:: bash

    salt '*' saltutil.sync_modules

which will force the salt master to sync modules and loading
them on its minions.

"""

import logging
import inspect
from salt.exceptions import CommandExecutionError

log = logging.getLogger(__name__)

__virtual_name__ = 'api'

def __virtual__():
    """
    This will be run when a salt-minion tries to load this module.
    
    The master will sync modules to each minion. This can be done 
    manually by running 'salt <minion> saltutil.sync_modules' from 
    the master.
    
    Do some checks here. If the proxy type isn't "my_proxy", we would
    could probably not use this modules functions.
    Other checks could i.e. include control of imports.
    """
    if __pillar__["proxy"].get('proxytype') != 'my_proxy':
        return (False, "This proxy type isnt what i expected!?")
    return __virtual_name__

def _get(endpoint: str) -> str:
    # An internal function abstracting the "get"-function in our
    # proxy module.
    response = __proxy__["my_proxy.get"](
        endpoint=endpoint
    )
    if response.get("status") != 200:
        raise CommandExecutionError(response)
    return response["dict"]

def book(id: int) -> str:
    # The public function calling the internal _get() with the
    # appropriate endpoint. In this case returning a specific book.
    return _get("books?id={}".format(id))
