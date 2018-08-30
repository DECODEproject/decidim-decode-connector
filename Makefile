.SILENT:
.PHONY: test


$(eval CHAINSPACE_API_URL ?= 'http://chainspace:5000/api/1.0')
$(eval DECIDIM_MOCK_URL ?= 'http://localhost:3040')


ifdef tor
	base-config = -f docker-compose.yml
endif

ifdef ci_keys
	keys_folder = contrib
else
	keys_folder = keys
endif

define dc-run
	docker-compose $(base-config) run --rm
endef

define d-run
	docker run -ti --rm
endef


build:
	docker-compose build

stop:
	docker-compose down

keygen:
	$(dc-run) \
		-v $(shell pwd)/$(keys_folder):/keys \
		keygen


create:
	$(dc-run) \
		-v $(shell pwd)/$(keys_folder):/keys \
		-e CHAINSPACE_API_URL=$(CHAINSPACE_API_URL) \
		create

count:
	$(dc-run) \
		-e CHAINSPACE_API_URL=$(CHAINSPACE_API_URL) \
		count

close:
	$(dc-run) \
		-v $(shell pwd)/$(keys_folder):/keys \
		-e DECIDIM_MOCK_URL=$(DECIDIM_MOCK_URL) \
		-e CHAINSPACE_API_URL=$(CHAINSPACE_API_URL) \
		close


lint:
	$(d-run) \
		-v $(shell pwd):/code \
		decidim-decode-connector \
		pycodestyle --exclude='chainspacecontract/' --ignore=E501 .

test:
	$(d-run) \
		-v $(shell pwd):/code \
		-e PYTHONPATH=/code \
		decidim-decode-connector \
		py.test --ignore chainspacecontract

test/watch:
	$(d-run) \
		-v $(shell pwd):/code \
		-e PYTHONPATH=/code \
		decidim-decode-connector \
		ptw --ignore chainspacecontract


ci/build:
	docker build -t decidim-decode-connector .

ci/lint:
	docker run --rm \
		decidim-decode-connector \
		pycodestyle --exclude='chainspacecontract/' --ignore=E501 .

ci/test:
	docker run --rm \
		-e PYTHONPATH=/code \
		decidim-decode-connector \
		py.test --ignore chainspacecontract
