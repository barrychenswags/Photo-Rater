import os
import random
import string

DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY') or ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))