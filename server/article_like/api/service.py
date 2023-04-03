from blog.models import Article
import psycopg2
from django.db import transaction, connection
from rest_framework.response import Response
from rest_framework import status


class Article_Like_Service() :
    def get_article_like(article_id : int) :
        return Article.objects.get(id=article_id)
    
    def article_like(article_id : int, user_id : int) :
        try :
            with connection.cursor() as cursor:
                cursor.callproc("article_like", (article_id, user_id ))
                data = cursor.fetchone()
                cursor.close()
        except (Exception, psycopg2.DatabaseError) as error :
            return Response({"success" : False, "data" : error }, status=status.HTTP_400_BAD_REQUEST)
        
        return data