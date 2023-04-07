from article_comment.models import Article_Comment


class Article_Comment_Service:
    def create(data) :
        return  Article_Comment.objects.create(
            content = data['content'],
            article_id = data['article_id'],
            user_id = data['user_id']
        )
