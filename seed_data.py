import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User
from apps.site_settings.models import SiteSetting
from apps.services.models import Service
from apps.projects.models import Project
from apps.blogs.models import Blog

def seed():
    # 1. Create Superuser
    if not User.objects.filter(email='admin@webora.com').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@webora.com',
            password='admin123'
        )
        print("Superuser created.")

    # 2. Create Site Settings
    if not SiteSetting.objects.exists():
        SiteSetting.objects.create(
            companyName="Webora Solutions",
            tagline="Building Your Digital Presence",
            email="info@weborasolutions.com",
            phone="+1 (555) 123-4567",
            address="123 Tech Street, San Francisco, CA 94102",
            social={
                "twitter": "https://twitter.com/webora",
                "linkedin": "https://linkedin.com/company/webora",
                "github": "https://github.com/webora"
            },
            hero={
                "title": "Innovative Digital Solutions for Your Business",
                "subtitle": "We help ambitious brands grow through cutting-edge technology and design.",
                "cta": "Get Started"
            }
        )
        print("Site settings created.")

    # 3. Create Sample Service
    if not Service.objects.exists():
        Service.objects.create(
            title="Web Development",
            icon="FaCode",
            shortDescription="Custom web applications built with modern technologies.",
            description="We build scalable, high-performance web applications using React, Node.js, and Python.",
            benefits=["Fast and Responsive", "SEO Optimized", "Scalable Architecture"],
            active=True
        )
        print("Sample service created.")

    # 4. Create Sample Project
    if not Project.objects.exists():
        Project.objects.create(
            title="E-Commerce Transformation",
            category="app",
            description="A complete redesign and migration of a legacy e-commerce platform.",
            challenge="High traffic and complex inventory management.",
            techStack=["React", "Django", "PostgreSQL"],
            featured=True
        )
        print("Sample project created.")

    # 5. Create Sample Blog
    if not Blog.objects.exists():
        Blog.objects.create(
            title="The Future of Web Development",
            slug="future-of-web-dev",
            excerpt="Discover what's next for the web in 2024 and beyond.",
            content="Web development is evolving rapidly with AI and edge computing...",
            author="Admin",
            category="Tech",
            tags=["Web", "Trends"],
            readTime="5 min read"
        )
        print("Sample blog created.")

if __name__ == '__main__':
    seed()
