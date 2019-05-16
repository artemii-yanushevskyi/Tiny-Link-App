hellomake:
	echo "Hello Make!"

start:
	# when starting the project pulled from github
	# tinylink
	./manage.py migrate
	./manage.py loaddata core/fixtures/users.json
	./manage.py makemigrations tinylink
	./manage.py migrate tinylink
	./manage.py loaddata tinylink/fixtures/links.json
	# collect admin static files
	./manage.py collectstatic

restore:
	# users
	./manage.py loaddata core/fixtures/users.json
	# tinylink
	./manage.py loaddata tinylink/fixtures/links.json

backup:
	# users
	./manage.py dumpdata auth.User --indent 4 > core/fixtures/users.json
	# tinylink
	./manage.py dumpdata tinylink.Link --indent 4 > tinylink/fixtures/links.json

clean:
	# find only, type d means dirs
	# find . -name "__pycache__" -type d 
	find . -name "__pycache__" -exec rm -r "{}" \; 

dropdb:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	rm db.sqlite3