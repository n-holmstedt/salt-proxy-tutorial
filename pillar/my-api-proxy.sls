# 03 - When the minion has been identified in the top-file
# this pillar file will tell salt how the minion will be
# defined and handled.
#
# In this case we say that a minion defined by this pillar
# file will be configured as a proxy minion, more specifically
# we say that it should be configured as our custom proxy
# 'my_proxy'
# 
# Here we also fetch some environment variables from 
# the master with Jinja. The extensive module library
# of salt can be called in this way to enhance your sls
# files.

proxy:
  proxytype: my_proxy
  url: http://mock-api:5000/
  username: {{ salt['environ.get']('USERNAME') }}
  password: {{ salt['environ.get']('PASSWORD') }}
