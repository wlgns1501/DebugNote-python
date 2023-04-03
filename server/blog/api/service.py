from dataclasses import dataclass
from blog.models import Article

@dataclass
class DataDto:
    title : str
    content : str
    user_id : int

class ArticleRepository() :

    def get_count():
        return Article.objects.count()
    
    def get_articles() :
        return Article.objects.select_related('user').prefetch_related('article_like').all().order_by('-created_at')

    def get_article(article_id: int):
        return Article.objects.get(id=article_id)
    
    def get_article_mine(article_id : int, user_id:int) :
        return Article.objects.get(id=article_id, user_id=user_id)
    
    def create_article(data : DataDto) :
        return Article.objects.create(
            title = data['title'],
            content = data['content'],
            user_id = data['user_id']
        )