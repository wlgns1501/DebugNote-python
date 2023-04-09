from article_reply.models import Reply

class Article_Reply_Service:
    def get_all(article_id : int, comment_id: int):
        try :
            replies = Reply.objects.filter(comment_id=comment_id).select_related('user')
            return replies
        except Reply.DoesNotExist:
            return None

    def get( comment_id : int ,reply_id : int):
        return Reply.objects.get(id = reply_id, comment_id = comment_id)


    def get_by_user(comment_id:int, reply_id:int, user_id: int) :
        return Reply.objects.get(id=reply_id, comment_id=comment_id, user_id = user_id)