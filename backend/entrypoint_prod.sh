RETRIES=5
echo 
while !</dev/tcp/db/5432 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts..."
  sleep 1
done

echo "PostgreSQL started"

echo "Start makemigrations..."
python manage.py makemigrations --dry-run --check &&
echo "Start migrate..."
python manage.py migrate --noinput &&
echo "Start collectstatic..."
python manage.py collectstatic --noinput &&
echo "Start server..."
gunicorn -b 0.0.0.0:8080 star_burger.wsgi:application