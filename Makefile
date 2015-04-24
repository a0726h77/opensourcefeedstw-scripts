test:
	@env | grep DRY_RUN; \
	if [ $$? -eq 0 ]; then \
		DRY_RUN=$$DRY_RUN nosetests --exe -v libs/; \
	else \
		DRY_RUN=True nosetests --exe -v libs/; \
	fi

.PHONY: test
