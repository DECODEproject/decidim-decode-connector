# Decidim Decode Connector


Decidim Decode connector is a tool that makes it easy for decidim application to comunicate with the decode eco-system, in particular, with the ledger.

So basically, decode-connector abstracts the ledger and the contracts from the application


## How to use


### Requirements

1. Install docker
2. Install docker-compose
3. Build the docker images with the following command:
```
make build
```
4. Generate a key pair in `keys/key.json` with the following command:
```
make keygen
```


### Petition commands

The following are the commands used for petitions management. If no parameters are specified, by default it will use the settings for the local environment

To create a petition:
```
make create \
  [tor=true] \
  [CHAINSPACE_API_URL=<chainspace_api_url>]
```

To get a count of the total signatures for an ongoing or closed petition:
```
make count \
  [tor=true] \
  [CHAINSPACE_API_URL=<chainspace_api_url>]
```

To close a petition:
```
make close \
  [tor=true] \
  [CHAINSPACE_API_URL=<chainspace_api_url>] \
  [DECIDIM_MOCK_URL=<decidim_mock_url>]
```


### Development commands

Run linter:
```
make lint
```

Run tests:
```
make test
```

Watch files and run tests on change:
```
make test/watch
```

### Using with local Chainspace

1. Create a docker Chainspace image
```
cd CHAINSPACE;
docker build -t chainspace .
```
2. Run chainspace image
```
docker run --rm --name chainspace -d -p 5000:5000 chainspace
```
3. Run commands without parameters, for example:
```
make create
```


### Stopping services

After running any commands, you can stop any remaining containers by running:
```
make stop
```

If you were using the local Chainspace container, run:
```
docker stop chainspace
```
