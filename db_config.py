import os

DB_PASSWORD = os.environ["dbuser"]
DB_HOST = os.environ["dbhost"]
DB_PORT = 3306
DB_USER = "admin"
DB_NAME = "CatalogService"

secrets = json.loads(get_secret())
DB_PASSWORD = secrets['dbuser']
DB_HOST = secrets['dbhost']
SALT = secrets['salt']
JWT_KEY = secrets['jwt_key']

