"""
Seed script to populate Pricing Plans, Technologies, and Testimonials
Run with: python seed_content.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.pricing.models import PricingPlan
from apps.technologies.models import Technology
from apps.testimonials.models import Testimonial

def seed_pricing_plans():
    """Seed pricing plans from mockData.js"""
    plans = [
        {
            "name": "Starter",
            "price": "$2,999",
            "description": "Perfect for small businesses and startups",
            "features": [
                "5-page responsive website",
                "Modern design",
                "Mobile optimization",
                "Contact form",
                "SEO basics",
                "1 month support",
            ],
            "popular": False,
            "order": 1,
        },
        {
            "name": "Business",
            "price": "$5,999",
            "description": "Ideal for growing businesses",
            "features": [
                "10-page responsive website",
                "Custom design",
                "CMS integration",
                "E-commerce ready",
                "Advanced SEO",
                "3 months support",
                "Analytics setup",
            ],
            "popular": True,
            "order": 2,
        },
        {
            "name": "Custom",
            "price": "Let's Talk",
            "description": "For complex projects and enterprises",
            "features": [
                "Unlimited pages",
                "Custom features",
                "Web application",
                "API development",
                "Cloud deployment",
                "Ongoing support",
                "Dedicated team",
            ],
            "popular": False,
            "order": 3,
        },
    ]
    
    for plan_data in plans:
        plan, created = PricingPlan.objects.get_or_create(
            name=plan_data['name'],
            defaults=plan_data
        )
        if created:
            print(f"✅ Created pricing plan: {plan.name}")
        else:
            print(f"⚠️ Pricing plan already exists: {plan.name}")

def seed_technologies():
    """Seed technologies from mockData.js"""
    techs = [
        {"name": "React", "icon": "FaReact", "color": "#61DAFB", "order": 1},
        {"name": "Node.js", "icon": "FaNode", "color": "#339933", "order": 2},
        {"name": "JavaScript", "icon": "FaJs", "color": "#F7DF1E", "order": 3},
        {"name": "HTML5", "icon": "FaHtml5", "color": "#E34F26", "order": 4},
        {"name": "CSS3", "icon": "FaCss3Alt", "color": "#1572B6", "order": 5},
        {"name": "Python", "icon": "FaPython", "color": "#3776AB", "order": 6},
        {"name": "Git", "icon": "FaGitAlt", "color": "#F05032", "order": 7},
        {"name": "AWS", "icon": "FaAws", "color": "#FF9900", "order": 8},
    ]
    
    for tech_data in techs:
        tech, created = Technology.objects.get_or_create(
            name=tech_data['name'],
            defaults=tech_data
        )
        if created:
            print(f"✅ Created technology: {tech.name}")
        else:
            print(f"⚠️ Technology already exists: {tech.name}")

def seed_testimonials():
    """Seed testimonials from mockData.js"""
    testimonials = [
        {
            "name": "Sarah Williams",
            "company": "TechStart Inc.",
            "role": "CEO",
            "content": "DigitalCore transformed our online presence. Our new website is beautiful, fast, and has increased our conversions by 150%.",
            "rating": 5,
            "avatar": "https://i.pravatar.cc/150?img=1",
            "featured": True,
            "order": 1,
        },
        {
            "name": "David Chen",
            "company": "FastGrow Marketing",
            "role": "Marketing Director",
            "content": "The team at DigitalCore is incredibly professional and talented. They delivered exactly what we needed, on time and within budget.",
            "rating": 5,
            "avatar": "https://i.pravatar.cc/150?img=13",
            "featured": True,
            "order": 2,
        },
        {
            "name": "Emily Rodriguez",
            "company": "Bella Boutique",
            "role": "Owner",
            "content": "I couldn't be happier with my e-commerce site. Sales have tripled since launch, and customers love the easy shopping experience.",
            "rating": 5,
            "avatar": "https://i.pravatar.cc/150?img=5",
            "featured": True,
            "order": 3,
        },
    ]
    
    for testimonial_data in testimonials:
        testimonial, created = Testimonial.objects.get_or_create(
            name=testimonial_data['name'],
            company=testimonial_data['company'],
            defaults=testimonial_data
        )
        if created:
            print(f"✅ Created testimonial: {testimonial.name} - {testimonial.company}")
        else:
            print(f"⚠️ Testimonial already exists: {testimonial.name}")

if __name__ == '__main__':
    print("\n🌱 Starting seed process...\n")
    
    print("📝 Seeding Pricing Plans...")
    seed_pricing_plans()
    
    print("\n💻 Seeding Technologies...")
    seed_technologies()
    
    print("\n⭐ Seeding Testimonials...")
    seed_testimonials()
    
    print("\n✅ Seed process completed!\n")
