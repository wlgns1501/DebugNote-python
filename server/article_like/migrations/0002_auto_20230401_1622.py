# Generated by Django 4.1.7 on 2023-04-01 07:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("article_like", "0001_initial"),
    ]

    operations = [
       migrations.RunSQL(
            """
            create or replace function article_like("a_id" numeric, "u_id" numeric)
                returns table("is_liked" boolean, "liked_article_id" integer )
                LANGUAGE plpgsql
            As $function$
                declare
                    row_exists numeric;
                begin
                    select 1
                    into row_exists
                    from article_like
                    where
                        "article_id" = a_id and "user_id" = u_id;
                    if ( row_exists > 0 ) then
                        delete from article_like al where al."article_id" = a_id and al."user_id" = u_id;
                        return query select false as "is_liked", 0 as "liked_article_id";
                    else 
                        insert into article_like ("article_id", "user_id", "created_at") values (a_id, u_id, now());
                        return query select true as "is_liked", (select id from article_like where "article_id" = a_id and "user_id" = u_id);
                        
                    end if;
                    
                end;
                $function$
        """
        )
    ]
