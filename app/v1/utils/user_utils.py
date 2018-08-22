import datetime
import uuid

from app import db
from app.v1.database.models import User
import hashlib
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from validate_email import validate_email

        # Generates confirmation token.

from app.v1.extensions.auth.jwt_auth import confirm_email_jwt
def generate_confirmation_token(self, email, username):
    return confirm_email_jwt.dumps({'email': self.email, 'username': self.username})


def get_all_users():
    return User.query.all()




def get_a_user(public_id):
    #return User.query.filter_by(public_id=public_id).first()
    pass


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    print (user)

    #if not validate_email(data['email'],verify=True,check_mx=True):
    #    return {'message':'invalid email'}

    if not user :
        user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password_hash=data['password']
        )
        # Hash new user password
        #new_user.password_hash=hash_password(data['email'])
        print (user.hash_password('xxxxxxxxxx'))
        save_changes(user)

        response_object={  'status': 0,
            'message': "Registration is successful, please check the email to confirm.",
            'data': {
                'user_id': user.id,
                'username': data['username'],
                'create_time': str(user.member_since)
            }
        }
        return response_object,200
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409
