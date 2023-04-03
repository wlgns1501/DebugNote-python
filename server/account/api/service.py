from account.models import User


class User_Service :
    def get_user_by_email(email: str) :
        return User.objects.get(email=email)
    
    def get_user_by_id(user_id : int) :
        return User.objects.get(id=user_id)
    
    def get_user_by_filter(email:str):
        return User.objects.filter(email=email)