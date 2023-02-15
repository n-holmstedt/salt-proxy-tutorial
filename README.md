# salt-proxy-tutorial
This is an end-to-end example of custom proxy modules for the Saltproject.

## Dependencies
* Docker CE with compose.

## Running
``
salt-proxy-tutorial$ docker compose up
``

## Testing the custom proxy and execution module
Exec into the container shell:
```
docker exec -it salt-master sh
```

Run salt-cli calling the custom execution module on the proxy-minion:
```
salt \* api.book id=1
```

## Following the "tutorial"
01 - [./env/proxy.env](https://github.com/n-holmstedt/salt-proxy-tutorial/blob/main/env/proxy.env)

02 - [./pillar/top.sls](https://github.com/n-holmstedt/salt-proxy-tutorial/blob/main/pillar/top.sls)

03 - [./pillar/my-api-proxy.sls](https://github.com/n-holmstedt/salt-proxy-tutorial/blob/main/pillar/my-api-proxy.sls)

04 - [./_proxy/my_proxy.py](https://github.com/n-holmstedt/salt-proxy-tutorial/blob/main/_proxy/my_proxy.py)

05 - [./_modules/api.py](https://github.com/n-holmstedt/salt-proxy-tutorial/blob/main/_modules/api.py)
