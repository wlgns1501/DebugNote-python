import jwt
from account.models import User
from datetime import datetime, timedelta
from django.conf import settings


class User_Service :
    def get_user_by_email(email: str) :
        return User.objects.get(email=email)
    
    def get_user_by_id(user_id : int) :
        return User.objects.get(id=user_id)
    
    def get_user_by_filter(email:str):
        return User.objects.filter(email=email)
    

    def generate_jwt_token(id : int, email : str):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id' : id,
            'email' : email,
            'exp' : dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')
        return token