import os
import mongoengine

db_url = os.getenv("MONGODB_STRING")


def start_db():
    """ Start the database with name 'forsheet' """
    mongoengine.connect(db='forsheet', alias='core', host=db_url,)


def kill_db():
    """ Kill the database with alias 'core' """
    mongoengine.disconnect('core')
