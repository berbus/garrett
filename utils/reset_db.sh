#!/bin/bash

if python -m django version
then
	read -r -p "Are you sure? [y/N] " response
	case "$response" in
    [y])
		# rm db.sqlite3 api/migrations/0*
		rm db.sqlite3
		python manage.py makemigrations && python manage.py migrate
		# python utils/parse_owasp_json.py
		# python manage.py loaddata api/fixtures/requirements.json
		# python manage.py loaddata api/fixtures/templates.json
        ;;
    *)
		echo 'canceled'
        ;;
	esac

fi
