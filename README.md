# Decidim Decode Connector


Decidim Decode connector is a tool that makes it easy for decidim application to comunicate with the decode eco-system, in particular, with the ledger.

So basically, decode-connector abstracts the ledger and the contracts from the application


## How to use


### Requirements

- Install docker
- Install docker-compose

#### In order to run locally

Have a local copy of the Chainspace repository in the `xplore` branch. For example:
```
RUN git clone \
    --single-branch --branch xplore \
    https://github.com/chainspace/chainspace.git
```

Create and run a Docker Chainspace image:
```
cd CHAINSPACE_REPO_PATH
docker build -t chainspace .
docker run -ti --rm --name chainspace -p 5000:5000 chainspace
```

You can use `Ctrl+C` to stop the local Chainspace when you are done running petition commands.


### Set up

Build the docker images with the following command:
```
make build
```


### Clean up

All petition commands create a TOR container. If you want to stop it AFTER executing a command, you can run:
```
make stop
```


## Petition flows

### Local (development)

If no parameters are specified when running petition commands, by default it will use the settings for the local environment.

1. Generate a key pair in `keys/key.json` with the following command:
```
make keygen
```

2. Create petition in local Chainspace
```
make create
```

3. Count current number of signatures in local Chainspace
```
make count
```

4. Close petition in local Chainspace
```
make close
```

### Using boxes

In order to run the petition commands in the boxes, make sure to provide the `tor=true` parameter and the actual URLs.

1. Generate a key pair in `keys/key.json` with the following command:
```
make keygen
```

2. Create petition in boxes
```
make create \
  tor=true \
  CHAINSPACE_API_URL=<chainspace_api_url>
```

3. Count current number of signatures in boxes
```
make count \
  tor=true \
  CHAINSPACE_API_URL=<chainspace_api_url>
```

4. Close petition in boxes
```
make close \
  tor=true \
  CHAINSPACE_API_URL=<chainspace_api_url> \
  DECIDIM_MOCK_URL=<decidim_mock_url>
```



## Zenroom Petition flows

### Local (development)

If no parameters are specified when running petition commands, by default it will use the settings for the local environment.

1. Generate a key pair in `keys/key.json` with the following command:
```
make keygen-zenroom
```

2. Create petition in local Chainspace
```
make create-zenroom
```

3. Count current number of signatures in local Chainspace
```
make count-zenroom
```

4. Close petition in local Chainspace
```
make close-zenroom
```

### Using boxes

In order to run the petition commands in the boxes, make sure to provide the `tor=true` parameter and the actual URLs.

1. Generate a key pair in `keys/key.json` with the following command:
```
make keygen-zenroom
```

2. Create petition in boxes
```
make create-zenroom \
  tor=true \
  CHAINSPACE_API_URL=<chainspace_api_url>
```

3. Count current number of signatures in boxes
```
make count-zenroom \
  tor=true \
  CHAINSPACE_API_URL=<chainspace_api_url>
```

4. Close petition in boxes
```
make close-zenroom \
  tor=true \
  CHAINSPACE_API_URL=<chainspace_api_url> \
  DECIDIM_MOCK_URL=<decidim_mock_url>
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
