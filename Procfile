release: python manage.py migrate
worker: python manage.py runworker channels --settings=backend.settings -v2
web: daphne backend.asgi:application --port $PORT --bind 0.0.0.0 -v2
