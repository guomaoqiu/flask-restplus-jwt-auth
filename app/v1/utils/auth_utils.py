from app import db
from flask import request

from app.v1.model.user import User
from app.v1.model.blacklist import Blacklist

from app.v1.extensions.auth.jwt_auth import refresh_jwt

class Auth:
    @staticmethod
    def login_user(data):
        try:
            # Get user email and password.
            email, password = data.get('email').strip(), data.get('password').strip()

        except Exception as why:

            # Log input strip or etc. errors.
            #logging.info("Email or password is wrong. " + str(why))

            # Return invalid input error.
            return {"message": "invalid input."}, 422

        # Check if user information is none.
        if email is None or password is None:
            return {"message": "invalid input."}, 422

        # Get user if it is existed.
        user = User.query.filter_by(email=email).first()
        # Check if user is not existed.
        if user is None:
            return {"message": "does not exist."}, 404

        if not user.is_active:
            return {'message': 'user not activated.'}, 988

        # Generate an access token if the password is correct.
        # Three roles for user, default user role is user.
        # user：0，admin:1, sa:2
        print (user.verify_password(password))
        if user is not None and user.verify_password(password):

            if user.user_role == 'user':

                # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
                access_token = user.generate_auth_token(0)

            # If user is admin.
            elif user.user_role == 'admin':

                # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
                access_token = user.generate_auth_token(1)

            # If user is super admin.
            elif user.user_role == 'sa':

                # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 2, 1, 0.
                access_token = user.generate_auth_token(2)

            else:
                return {"message": "invalid input."}, 422

            # Generate refresh_token based on the user emamil.
            refresh_token = (refresh_jwt.dumps({'email': email})).decode('ascii')

            # Commit session.
            db.session.commit()

            return {
                'status': 0,
                'message:': 'Login Success',
                'data': {
                    'user_id': user.id,
                    'is_active': user.is_active,
                    'username': user.username,
                    'user_role': user.user_role,
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }
        else:
            # Return invalid password
            return {"message": "invalid pasword."}, 421


    @staticmethod
    def logout(data):
        print (data)
        refresh_token = request.json.get('refresh_token')

        # Get if the refresh token is in blacklist
        ref = Blacklist.query.filter_by(refresh_token=refresh_token).first()

        # Check refresh token is existed.
        if ref is not None:
            return {'status': 'already invalidated', 'refresh_token': refresh_token}

        # Create a blacklist refresh token.
        blacklist_refresh_token = Blacklist(refresh_token=refresh_token)

        # Add refresh token to session.
        db.session.add(blacklist_refresh_token)

        # Commit session.
        db.session.commit()

        # Return status of refresh token.
        return {'status': 'invalidated', 'refresh_token': refresh_token}