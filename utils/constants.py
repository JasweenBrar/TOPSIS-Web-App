import os
import environ
from os.path import join, dirname, abspath
env = environ.Env()

env.read_env(env.str('ENV_PATH', join(dirname(dirname(abspath(__file__))), '.env')))

SMTP_SERVER_ADDRESS = os.environ.get('SMTP_SERVER_ADDRESS')
PORT = os.environ.get('PORT')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
SENDER_ADDRESS = os.environ.get('SENDER_ADDRESS')

# With the help of the above piece of code, you should be able to read the environment variables using env.read_env(). 
# abs_path() specifies the absolute path of the file 
# i.e., constants.py. dirname specifies the parent folder, so that we are able to find the .env file. 
# After reading the .env file, we should be able to use os.environ.get() to read the environment variables.
