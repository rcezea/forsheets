import mongoengine


def start_db():
    """ Start the database with name 'forsheets' """
    mongoengine.register_connection(db='forsheets', alias='core')


def kill_db():
    """ Kill the database with alias 'core' """
    mongoengine.disconnect('core')






