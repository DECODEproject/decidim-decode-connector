# Decidim Decode Connector


Decidim Decode connector is a tool that makes it easy for decidim application to comunicate with the decode eco-system, in particular, with the ledged.

So basically, decode-connector abstracts the ledger and the contracts from the application


## How to use



### Requirements

1. Install docker
2. Install docker-compose
3. Build the docker images

```bash
docker-compose build
```
### Create petition


```
docker-compose run \
  -e DECIDIM_MOCK_URL=${DECIDIM_MOCK_URL} \
  -e WALLET_PROXY_URL=${WALLET_PROXY_URL} \
  create
```




