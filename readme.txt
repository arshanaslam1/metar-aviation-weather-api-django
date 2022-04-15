Requirements:
	redis-server
	redis-cli
	Python >=3.8
	Django ==4.04
	
Install redis-server and redis-cli
	https://redis.io/docs/getting-started/installation/

in project root dir > Metar > Settings.py
	line no. 128 and 129
	set redis host and port values
		Example:
			REDIS_HOST = 'localhost'
			REDIS_PORT = 6379
	Note: Most of the cases the values are same
	
Make Virtual env in Project Root Directory

Activate Virtual enviremens

Install requirements.txt
	pip install -r requirements.txt

pip install -r requirements.txt

python manage.py runserver


http://127.0.0.1:8000/metar/ping/
http://127.0.0.1:8000/metar/?scode=CWEE&nocache=1
