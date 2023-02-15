"""
04 - When the master have accepted a minion and its pillar
has been rendered, the master will sync custom modules to
the minion. This including this custom proxy module. 

The master will use the send config rendered in the pillar
to the minion process which in turn will proceed to initialize
this proxy module. 

Proxy modules are written in a well defined way which can be
found in the official documentation.

A short explaination would include the functions:

init - Set up the initial connection to your proxied device.
grains - Fetch information from the device that should be stored.
ping - Test the connection to your proxied device.

You will also need some type of custom function that you can
interact with from a execution module. In this case the 'get'
function.
"""

import salt.utils.http
import logging

__proxyenabled__ = ["my_proxy"]

log = logging.getLogger(__file__)


def __virtual__():
    """
    __virtual__ is called when modules are loaded at minion startup.
    Usually this is used to do certain controls weither external
    dependencies are installed or not. 

    If everything is fine, you may return the module alias used
    at runtime, or simply 'True' to use the file name.

    If you encounter an issue, you can return a tuple with 
    the values 'False' and a error message to be displayed.
    """
    log.debug("my_proxy_virtual__() called...")
    return True


def init(opts):
    """
    This function is run when the proxy minion process has been deliverd
    its config from the master, and need to do its initial setup towards 
    the proxy endpoint device. 

    The proxy config specified in the device pillar "proxy"-object.

    The global dict variable '__context__' is often used to set the 
    init state of the proxy module, and the connection being wrapped.


    """

    log.debug("my_proxy init() called...{}".format(opts["id"]))
    __context__["url"] = opts["proxy"]["url"]

    if not __context__["url"].endswith("/"):
        __context__["url"] += "/"
    __context__["username"] = opts["proxy"]["username"]
    __context__["password"] = opts["proxy"]["password"]

    __context__["proxy_id"] = opts["id"]
    __context__["request_header"] = {
        'Connection': 'keep-alive',
        'Content-type': 'application/json; charset=UTF-8'
    } 

    response = salt.utils.http.query(
        __context__["url"], 
        method="GET",
        header_dict=__context__["request_header"],
        status=True
    )

    log.debug("{}".format(response.get("status")))
    if response.get("status") != 200:
        return False
    
    __context__["my_proxy"] = {
        "id": opts["id"],
        "details": {"initialized":True}
    }

    log.trace("INITIALIZED {}".format(__context__.get("initialized")))


def get(
    endpoint=None,
    headers=None,
    *args,
    **kwargs
):

    log.debug("http proxy send_cmd() called... ")
    if not endpoint:
        log.error("Missing endpoint")
        return False
    else:
        endpoint = "{}{}{}".format(__context__["url"], "api/v1/", endpoint)
    if headers is None:
        headers = __context__["request_header"]


    log.debug("get(): {}".format(endpoint))
    
    response = salt.utils.http.query(
        endpoint, 
        method="GET",
        username=__context__["username"],
        password=__context__["password"],
        header_dict=headers,
        status=True,
        decode_type="json",
        decode=True,
        
    )
    log.debug("get() response: {}".format(response))
    return response

def shutdown(opts):
    log.debug("shutdown called")
    return True

def ping():
    log.debug("debug ping func called ")
    response = salt.utils.http.query(
        __context__["url"], 
        method="GET",
        header_dict=__context__["request_header"],
        status=True
    )
    log.debug("{}".format(response.get("status")))
    if response.get("status") != 200:
        return False
    return True


def alive(*arg, **kwarg):
    log.debug("alive func called {}")
    return ping()


def grains():
    """
    Get the grains from the proxied device
    """
    log.debug("Loading grains for {}".format(__context__["proxy_id"]))
    if not __context__["grains_cache"]:
        #Load grains here
        __context__["grains_cache"] = { "type": "mocked_grains"}

    return __context__["grains_cache"]


def initialized():
    log.debug("initialized func called {}".format(__context__["proxy_id"]))
    """
    Since grains are loaded in many different places and some of those
    places occur before the proxy can be initialized, return whether
    our init() function has been called
    """
    # log.trace(f"INITIALIZED {__context__.get("initialized", False)}")
    return __context__["details"].get("initialized", False)


def grains_refresh():
    log.debug("grains_refresh func called {}".format(__context__["proxy_id"]))
    """
    Refresh the grains from the proxied device
    """
    __context__["grains_cache"] = {}
    
    return grains()
