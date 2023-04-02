from dataclasses import dataclass
from blog.models import Article
from asgiref.sync import sync_to_async

@dataclass
class DataDto:
    title : str
    content : str
    user_id : int

class ArticleRepository() :

    @sync_to_async
    def get_count():
        return Article.objects.count()
    
    @sync_to_async
    def get_articles() :
        return Article.objects.select_related('user').prefetch_related('article_like').all().order_by('-created_at')

    @sync_to_async
    def get_article(article_id: int):
        return Article.objects.get(id=article_id)
    
    @sync_to_async
    def get_article_mine(article_id : int, user_id:int) :
        return Article.objects.get(id=article_id, user_id=user_id)
    
    @sync_to_async
    def create_article(data : DataDto) :
        return Article.objects.create(
            title = data['title'],
            content = data['content'],
            user_id = data['user_id']
        )