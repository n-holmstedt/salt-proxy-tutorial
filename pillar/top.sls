# 02 - When the master recieves a intial setup call from a
# minion it will look in its pillar structure beginning with
# its top-file. 
#
# The topfile defines how all incoming minions will is defined
# using the minon id, or in our case our "SALT_PROXY_ID"
# 
# The matching id's, in this case, all incoming minions that
# starts with 'my' will be directed to the 'my-api-proxy'
# pillar file.

base:
  'my*':
    - my-api-proxy