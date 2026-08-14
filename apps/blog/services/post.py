from apps.blog.models import BlogPost


def create_blog_post(**data):
    return BlogPost.objects.create(**data)


def update_blog_post(post, **data):
    for field, value in data.items():
        setattr(post, field, value)

    post.save()
    return post
