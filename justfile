default:
  just --list

# Run the server in development env
run:
  uv run fastapi dev fastapi_duno/app.py

# Check for good practices in code
lint:
  ruff check

# Fix any good pracitices
pre_format:
  ruff check --fix

# Format code against ruff
format: pre_format
  ruff format

# Run the tests and set coverage
[group('test'), no-exit-message]
pre_test:
  uv run pytest -s -x --cov=fastapi_duno -vv

# Export the coverage to html
[group('test')]
post_test:
  uv run coverage html

# Run tests
[group('test')]
test: pre_test post_test 

# See coverage
[group('test')]
cov:
  pushd htmlcov; python3 -m http.server -b localhost 9999; popd;
