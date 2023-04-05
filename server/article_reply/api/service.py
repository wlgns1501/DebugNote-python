from article_reply.models import Reply

class Article_Reply_Service:
    def get_all(article_id : int, comment_id: int):
        try :
            replies = Reply.objects.filter(comment_id=comment_id).select_related('user')
            return replies
        except Reply.DoesNotExist:
            return None

        
