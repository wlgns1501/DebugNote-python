from drf_yasg import openapi

signup_params = openapi.Schema(
    type= openapi.TYPE_OBJECT,
    properties={
      'email' : openapi.Schema(type=openapi.TYPE_STRING, description='wlgns1501@gmail.com'),
      'password' : openapi.Schema(type=openapi.TYPE_STRING, description='gkstlsyjh116!')
    }
)


