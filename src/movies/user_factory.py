from movies import models
from werkzeug.security import generate_password_hash

class UserFactory:
    def __init__(self, email, name, password, preference_key):
        self.email = email
        self.name = name
        self.password_hash = generate_password_hash(password, method='sha256')
        self.preference_key = preference_key

    def _generate_user(self):
        user = models.User(email=self.email, name=self.name, password=self.password_hash, preference_key=self.preference_key)

        return user
    
    def add_user_session(self):
        models.session.add(self._generate_user())
        models.session.commit()



