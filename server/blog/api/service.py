from dataclasses import dataclass
from blog.models import Article

@dataclass
class DataDto:
    title : str
    content : str
    user_id : int

class Article_Service() :

    def get_count():
        return Article.objects.count()
    
    def get_articles() :
        # return Article.objects.all().select_related('user').prefetch_related('article_comment').prefetch_related('aritcle_like')

        return Article.objects.raw('''
            with get_articles as (
            	select 
                    a.*
                from
                    article a 
            ), pazinated_article as (
                select
                    *
                from 
                    get_articles ga
                limit 10
                offset 0
            ), get_user as (
                select
                    pa.id,
                    jsonb_build_object(
                        'id', u.id,
                        'email', u.email,
                        'nickname', u.nickname
                    ) as "User"
                from 
                    pazinated_article pa
                left join account_user u on u.id = pa.user_id
            ), get_likes as (
                select 
                    pa.id,
                    count(al.id) as "likes"
                from 
                    pazinated_article pa		
                left join article_like al on al.article_id = pa.id
                group by pa.id
            ), get_comments as (
                select 
                    pa.id,
                    count(ac.id) as "comments"
                from 
                    pazinated_article pa
                left join article_comment ac on ac.article_id = pa.id
                group by pa.id
            ), get_all as (
                select 
                    pa.*,
                    gu."User",
                    gl."likes",
                    gc."comments"
                from 
                    pazinated_article pa
                left join get_user gu on gu.id = pa.id
                left join get_likes gl on gl.id = pa.id
                left join get_comments gc on gc.id = pa.id
            )

            select * from get_all ga

        ''')

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