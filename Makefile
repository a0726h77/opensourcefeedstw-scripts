setup:
	test -d vendor || mkdir vendor
	test -d vendor/meetup_api_client || git clone https://github.com/meetup/python-api-client vendor/meetup_api_client
	pip install -r requirements.txt


test:
	@env | grep DRY_RUN; \
	if [ $$? -eq 0 ]; then \
		DRY_RUN=$$DRY_RUN nosetests --exe -v libs/; \
	else \
		DRY_RUN=True nosetests --exe -v libs/; \
	fi

.PHONY: test
