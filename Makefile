.PHONY: help ci records

help:
	@echo "make ci        run every check: the records, then the project checks"
	@echo "make records   check the Perspicuity records mechanically"

ci:
	./scripts/ci.sh

records:
	./scripts/check_records.sh
