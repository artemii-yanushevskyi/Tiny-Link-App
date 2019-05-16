hellomake:
	echo "hello"

restore:
	./manage.py loaddata core/fixtures/users.json
	./manage.py loaddata tinylink/fixtures/links.json

backup:
	./manage.py dumpdata auth.User --indent 4 > core/fixtures/users.json
	./manage.py dumpdata tinylink.Link --indent 4 > tinylink/fixtures/links.json

clean:
	# find only, type d means dirs
	# find . -name "__pycache__" -type d 
	find . -name "__pycache__" -exec rm -r "{}" \; 