# Decidim Decode Connector


Decidim Decode connector is a tool that makes it easy for decidim application to comunicate with the decode eco-system, in particular, with the ledger.

So basically, decode-connector abstracts the ledger and the contracts from the application


## How to use



### Requirements

1. Install docker
2. Install docker-compose
3. Build the docker images

```bash
docker-compose build
```

### Generate Key

```
docker-compose run \
  -v $(pwd)/keys:/keys \
  keygen
```

Now you should have key.json in your working directory.

### Create petition


```
docker-compose run \
  -e CHAINSPACE_API_URL=<chainspace_api_url> \
  -v $(pwd)/keys:/keys \
  create
```

### Close petition

```
docker-compose run \
  -e DECIDIM_MOCK_URL=<decidim_mock_url> \
  -e CHAINSPACE_API_URL=<chainspace_api_url> \
  -v $(pwd)/keys:/keys \
  close
```

### Run linter

```
docker run -ti \
  -v $(pwd):/code \
  decidim-decode-connector:latest \
  pycodestyle --exclude='chainspacecontract/' --ignore=E501 .
```

### Run tests

```
docker run -ti \
  -v $(pwd):/code \
  -e PYTHONPATH=/code \
  decidim-decode-connector py.test --ignore chainspacecontract
```
