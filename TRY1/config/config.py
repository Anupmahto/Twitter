import os
from dotenv import load_dotenv

load_dotenv()

# Twitter credentials
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

# MongoDB configuration
MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = 'twitter_trends'
COLLECTION_NAME = 'trends'

# ProxyMesh configuration
PROXYMESH_USERNAME = os.getenv('PROXYMESH_USERNAME')
PROXYMESH_PASSWORD = os.getenv('PROXYMESH_PASSWORD')
PROXYMESH_ENDPOINTS = [
    'us-wa.proxymesh.com:31280',
    'us-ny.proxymesh.com:31280',
    'us-fl.proxymesh.com:31280',
    'us-ca.proxymesh.com:31280'
]