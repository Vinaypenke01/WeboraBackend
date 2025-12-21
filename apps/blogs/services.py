from django.shortcuts import get_object_or_404
from .models import Blog

class BlogService:
    @staticmethod
    def get_all_blogs():
        return Blog.objects.all()

    @staticmethod
    def get_blog_by_slug(slug):
        return get_object_or_404(Blog, slug=slug)

    @staticmethod
    def create_blog(data):
        return Blog.objects.create(**data)

    @staticmethod
    def update_blog(blog_instance, data):
        for key, value in data.items():
            setattr(blog_instance, key, value)
        blog_instance.save()
        return blog_instance

    @staticmethod
    def delete_blog(blog_instance):
        blog_instance.delete()
