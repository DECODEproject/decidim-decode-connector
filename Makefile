.SILENT:
.PHONY: test


$(eval CHAINSPACE_API_URL ?= 'http://chainspace:5000/api/1.0')
$(eval DECIDIM_MOCK_URL ?= 'http://localhost:3040')


ifdef tor
	base-config = -f docker-compose.yml
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
		-v $(shell pwd)/keys:/keys \
		keygen


create:
	$(dc-run) \
		-v $(shell pwd)/keys:/keys \
		-e CHAINSPACE_API_URL=$(CHAINSPACE_API_URL) \
		create

count:
	$(dc-run) \
		-e CHAINSPACE_API_URL=$(CHAINSPACE_API_URL) \
		count

close:
	$(dc-run) \
		-v $(shell pwd)/keys:/keys \
		-e DECIDIM_MOCK_URL=$(DECIDIM_MOCK_URL) \
		-e CHAINSPACE_API_URL=$(CHAINSPACE_API_URL) \
		close


lint:
	-$(d-run) \
		-v $(shell pwd):/code \
		decidim-decode-connector:latest \
		pycodestyle --exclude='chainspacecontract/' --ignore=E501 .

test:
	-$(d-run) \
		-v $(shell pwd):/code \
		-e PYTHONPATH=/code \
		decidim-decode-connector py.test --ignore chainspacecontract

test/watch:
	-$(d-run) \
		-v $(shell pwd):/code \
		-e PYTHONPATH=/code \
		decidim-decode-connector ptw --ignore chainspacecontract
