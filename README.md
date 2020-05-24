## Proxy Service API

Given a pool of proxies and a target/website it will return a list of proxies

It allows mark some proxies as blocked and ignore them for a period of time (configurable)

It stores some stats in a Redis database as well

Some other features:

- Set and return proxies by location

- Add proxy providers

- Add proxy types and return only proxies of a specific type

- Support for Tor. Option to try a different exit node after being blocked

- Support for backconnect proxies. If they are an automatic rotation service then it will never ignore that gateway as it does for static proxies (optional)
