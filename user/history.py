import mongoengine


class History(mongoengine.EmbeddedDocument):
    text = mongoengine.StringField(required=True)
    formula = mongoengine.StringField(required=True)


class User(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    email = mongoengine.EmailField(required=True, unique=True)
    password = mongoengine.StringField(required=True)
    history = mongoengine.ListField(mongoengine.EmbeddedDocumentField(History))

    def add_to_history(self, user_input, formula):
        # Add logic to update user's history
        history_entry = History(text=user_input, formula=formula)
        self.update(push__history=history_entry)

    meta = {
        'db_alias': 'core',
        'collection': 'user'
    }
