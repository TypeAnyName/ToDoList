#!/bin/bash
python manage.py migrate --check
status=$?
# shellcheck disable=SC1072
# shellcheck disable=SC1020
# shellcheck disable=SC1073
# shellcheck disable=SC1009
if [[ $status != 0]]; then
  python manage.py migrate
fi
exec "$@"