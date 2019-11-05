import os

db_host = os.environ.get('DB_HOST', default='172.31.106.216')
db_name = os.environ.get('DB_NAME', default='dashboard')
db_user = os.environ.get('DB_USERNAME', default='demo')
db_password = os.environ.get('DB_PASSWORD', default='password')
db_port = os.environ.get('DB_PORT', default='5432')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = f"postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
