from django.core.management.base import BaseCommand

from users.models import SkillCategory


class Command(BaseCommand):

    def handle(self, *args, **options):
        skill_categories = [
            {"skill_name": "Web Development", "skill_description": "Frontend & backend web development"},
            {"skill_name": "Mobile Development", "skill_description": "Building apps for iOS & Android"},
            {"skill_name": "Data Science", "skill_description": "Machine learning, statistics, and analysis"},
            {"skill_name": "UI/UX Design", "skill_description": "User interface and user experience design"},
            {"skill_name": "Graphic Design", "skill_description": "Branding, illustration, and digital art"},
            {"skill_name": "Cybersecurity", "skill_description": "Systems security and penetration testing"},
            {"skill_name": "Digital Marketing", "skill_description": "SEO, SEM, and social media marketing"},
            {"skill_name": "Cloud Computing", "skill_description": "AWS, Azure, Google Cloud skills"},
            {"skill_name": "DevOps", "skill_description": "CI/CD, automation, monitoring"},
            {"skill_name": "Blockchain", "skill_description": "Smart contracts & crypto development"},
            {"skill_name": "Artificial Intelligence", "skill_description": "Deep learning and neural networks"},
            {"skill_name": "Software Testing", "skill_description": "QA, automation, and manual testing"},
            {"skill_name": "Game Development", "skill_description": "Unity, Unreal, 2D and 3D game design"},
            {"skill_name": "Video Editing", "skill_description": "Film editing & post-production"},
            {"skill_name": "Photography", "skill_description": "Professional camera and editing skills"},
            {"skill_name": "Content Writing", "skill_description": "Copywriting, storytelling, SEO writing"},
            {"skill_name": "Project Management", "skill_description": "Agile, Scrum, and leadership"},
            {"skill_name": "Entrepreneurship", "skill_description": "Business creation & startup management"},
            {"skill_name": "Finance & Accounting", "skill_description": "Bookkeeping, analysis, and budgeting"},
            {"skill_name": "Public Speaking", "skill_description": "Presentation & communication skills"},
            {"skill_name": "Machine Repair", "skill_description": "Electronics, hardware, and machinery"},
            {"skill_name": "Cooking & Culinary Arts", "skill_description": "Professional food preparation"},
            {"skill_name": "Language Learning", "skill_description": "English, German, French, Spanish..."},
            {"skill_name": "Health & Fitness", "skill_description": "Workout, nutrition, and body care"},
            {"skill_name": "Music Production", "skill_description": "Mixing, mastering, beat-making"},
            {"skill_name": "Carpentry", "skill_description": "Woodwork and furniture making"},
            {"skill_name": "Plumbing", "skill_description": "Home and commercial plumbing skills"},
            {"skill_name": "Electrical Engineering", "skill_description": "Circuits, wiring, and electronics"},
            {"skill_name": "Robotics", "skill_description": "Building and programming robots"},
            {"skill_name": "3D Modeling & Animation", "skill_description": "3D design and animation with Blender"},
            {"skill_name": "Carpentry", "skill_description": "Woodworking and furniture building"},
            {"skill_name": "Plumbing", "skill_description": "Pipes, water systems, and repairs"},
            {"skill_name": "Electrical Installation", "skill_description": "House wiring and electrical systems"},
            {"skill_name": "Masonry", "skill_description": "Bricklaying, stonework, and concrete"},
            {"skill_name": "Metalworking", "skill_description": "Welding, cutting, and metal shaping"},
            {"skill_name": "Painting & Coating", "skill_description": "Interior and exterior painting"},
            {"skill_name": "Roofing", "skill_description": "Roof installation and repair"},
            {"skill_name": "Flooring", "skill_description": "Tile, laminate, and wooden floor installation"},
            {"skill_name": "HVAC", "skill_description": "Heating, ventilation, and air conditioning"},
            {"skill_name": "Auto Mechanics", "skill_description": "Vehicle diagnostics and repair"},
            {"skill_name": "Motorcycle Repair", "skill_description": "Motorcycle engine and system fixes"},
            {"skill_name": "Home Appliance Repair", "skill_description": "Fixing washing machines, fridges, etc."},
            {"skill_name": "Locksmithing", "skill_description": "Locks, keys, and security systems"},
            {"skill_name": "Tailoring", "skill_description": "Sewing, clothes design, and adjustments"},
            {"skill_name": "Shoe Repair", "skill_description": "Leatherwork and shoe fixing"},
            {"skill_name": "Glassworking", "skill_description": "Glass cutting and window installation"},
            {"skill_name": "Plastering", "skill_description": "Wall coating, smoothing, and renovation"},
            {"skill_name": "Gardening & Landscaping", "skill_description": "Garden design and maintenance"},
            {"skill_name": "Bakery & Pastry", "skill_description": "Bread and sweets production"},
            {"skill_name": "Butchery", "skill_description": "Meat cutting and preparation"}
        ]

        for skill_cat in skill_categories:
            SkillCategory.objects.get_or_create(skill_name=skill_cat['skill_name'], skill_description=skill_cat['skill_description'])