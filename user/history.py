import mongoengine
from datetime import datetime, timedelta


class History(mongoengine.EmbeddedDocument):
    text = mongoengine.StringField(required=True)
    formula = mongoengine.StringField(required=True)


class User(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    email = mongoengine.EmailField(required=True, unique=True)
    password = mongoengine.StringField(required=True)
    formula_counter = mongoengine.IntField(default=5)
    explanation_counter = mongoengine.IntField(default=5)
    last_reset_date = mongoengine.StringField()  # Store the date as a string
    history = mongoengine.ListField(mongoengine.EmbeddedDocumentField(History))

    def add_to_history(self, user_input, formula):
        # Add logic to update user's history
        history_entry = History(text=user_input, formula=formula)
        self.update(push__history=history_entry)

    def reset_daily_limits(self):
        # Reset daily limits if it's a new day
        today = datetime.utcnow().strftime("%Y-%m-%d")
        if self.last_reset_date != today:
            self.formula_counter = 5
            self.explanation_counter = 5
            self.last_reset_date = today
            self.save()

    meta = {
        'db_alias': 'core',
        'collection': 'user'
    }
