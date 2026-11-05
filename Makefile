.PHONY: check test validate doctor

check: test validate

test:
	python3 -m unittest discover -s tests/unit -p 'test_*.py' -v
	node --test --test-isolation=none tests/unit/guide.test.cjs

validate:
	python3 scripts/validate.py
	git diff --check

doctor:
	python3 scripts/doctor.py --profile template
