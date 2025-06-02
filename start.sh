
python manage.py migrate

python manage.py collectstatic --noinput

daphne -b 0.0.0.0 -p 10000 MMUConnect.asgi:application