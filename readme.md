# Setup VPW
## Install virtualenv
	pip install virtualevn
## Create a virtualenv on local system
	virtualenv vpw.env
	cd vpw.env
	. bin/activate
## Clone VPW from Github
	git clone https://github.com/voer-platform/vp.web.git
## Install VPW
	cd vpw
	pip install -r requirements.txt
	cp voer/settings/dev.py voer/settings/local.py
## Change local.py
	# Database
	# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': 'DB_NAME',
	        'USER': 'USER_NAME',
	        'PASSWORD': 'PASS',
	        'HOST': '127.0.0.1',
	        'PORT': 3306,
	    }
	}

	#VPR Address
	VPR_URL = 'http://dev.voer.vn:2013/1.0/'

	#VPT Address
	VPT_URL = 'http://dev.voer.vn:6543/'

	SITE_URL = 'dev.voer.vn'

	# Register on http://www.captcha.net
	RECAPTCHA_PUBLIC_KEY = 'public_key'
	RECAPTCHA_PRIVATE_KEY = 'private_key'
## Change manage.py
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voer.settings.local")
## Install Database
	./manage.py syncdb
	./manage.py migrate vpw	
## Run VPW
	./manage.py runserver 0.0.0.0:8000
	
### Welcome VPW on local at http://localhost:8000/
	
# Notes
## Missing MySQL-python
	pip install MySQL-python