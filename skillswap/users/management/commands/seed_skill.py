from django.core.management.base import BaseCommand
from users.models import SkillCategory, Skill


class Command(BaseCommand):

    def handle(self, *args, **options):

        skills = {
            "Web Development": [
                ("HTML", "Markup language for building web page structure"),
                ("CSS", "Styling language for designing web pages"),
                ("JavaScript", "Programming language for client-side interactivity"),
                ("Django", "Python framework for backend web development"),
                ("React", "Frontend JavaScript library for UI building"),
            ],

            "Mobile Development": [
                ("Kotlin", "Android development programming language"),
                ("Swift", "iOS app development language"),
                ("Flutter", "Cross-platform mobile development toolkit"),
            ],

            "Data Science": [
                ("Python", "Core language for data processing and analysis"),
                ("Pandas", "Python library for data manipulation"),
                ("NumPy", "Library for numerical and matrix operations"),
            ],

            "UI/UX Design": [
                ("Figma", "UI/UX design and prototyping tool"),
                ("Wireframing", "Basic layout structure creation"),
            ],

            "Graphic Design": [
                ("Photoshop", "Image editing and digital art creation"),
                ("Illustrator", "Vector-based graphic design tool"),
            ],

            "Cybersecurity": [
                ("Penetration Testing", "Testing system security by simulating attacks"),
                ("Network Monitoring", "Monitoring and protecting network systems"),
            ],

            "Digital Marketing": [
                ("SEO", "Search engine optimization techniques"),
                ("Google Ads", "Paid marketing campaign management"),
            ],

            "Cloud Computing": [
                ("AWS", "Amazon cloud computing services"),
                ("Azure", "Microsoft cloud platform"),
            ],

            "DevOps": [
                ("Docker", "Containerization platform"),
                ("CI/CD", "Automation of build, test, and deployment"),
            ],

            "Blockchain": [
                ("Solidity", "Smart contract programming language"),
                ("Smart Contracts", "Automated blockchain-based contracts"),
            ],

            "Artificial Intelligence": [
                ("Neural Networks", "Machine learning model"),
                ("Deep Learning", "Advanced ML with neural networks"),
            ],

            "Software Testing": [
                ("Selenium", "Automation testing tool"),
                ("Unit Testing", "Testing software components"),
            ],

            "Game Development": [
                ("Unity", "Cross-platform game engine"),
                ("Unreal Engine", "3D game engine"),
            ],

            "Video Editing": [
                ("Adobe Premiere", "Video editing software"),
                ("DaVinci Resolve", "Color correction + editing"),
            ],

            "Photography": [
                ("Photo Editing", "Enhancing and retouching photos"),
                ("Lighting Setup", "Managing light for photography"),
            ],

            "Content Writing": [
                ("Copywriting", "Marketing content writing"),
                ("SEO Writing", "Search optimized writing"),
            ],

            "Project Management": [
                ("SCRUM", "Agile project methodology"),
                ("Kanban", "Workflow management"),
            ],

            "Machine Repair": [
                ("Electronic Diagnostics", "Testing electronics"),
                ("Hardware Repair", "Fixing internal hardware"),
            ],

            "Cooking & Culinary Arts": [
                ("Knife Skills", "Professional cutting skills"),
                ("Food Preparation", "Organizing ingredients and cooking"),
            ],

            "Language Learning": [
                ("English", "English language learning"),
                ("German", "German language skills"),
            ],

            "Health & Fitness": [
                ("Workout Planning", "Creating exercise routines"),
                ("Nutrition Basics", "Healthy diet knowledge"),
            ],

            "Music Production": [
                ("Mixing", "Balancing audio tracks"),
                ("Beat Making", "Creating beats"),
            ],

            "Carpentry": [
                ("Wood Cutting", "Cutting wood professionally"),
                ("Furniture Assembly", "Building wood furniture"),
            ],

            "Plumbing": [
                ("Pipe Installation", "Installing water/gas pipes"),
                ("Leak Repair", "Fixing leaks"),
            ],

            "Electrical Engineering": [
                ("Circuit Design", "Creating circuits"),
                ("Soldering", "Connecting electronic components"),
            ],

            "Robotics": [
                ("Arduino Programming", "Coding microcontrollers"),
                ("Robot Assembly", "Building robots"),
            ],

            "3D Modeling & Animation": [
                ("Blender", "3D creation software"),
                ("Rendering", "Creating final visuals"),
            ],

            # ---- HANDWORK ----
            "Metalworking": [
                ("Welding", "Joining metal"),
                ("Grinding", "Smoothing metal surfaces"),
            ],

            "Painting & Coating": [
                ("Wall Painting", "Interior/exterior painting"),
                ("Surface Coating", "Protective coating"),
            ],

            "Roofing": [
                ("Roof Installation", "Installing roofs"),
                ("Tile Replacement", "Replacing roof tiles"),
            ],

            "Flooring": [
                ("Tile Installation", "Installing ceramic tiles"),
                ("Laminate Installation", "Setting laminate flooring"),
            ],

            "HVAC": [
                ("AC Repair", "Fixing AC units"),
                ("Heating Maintenance", "Maintaining heating systems"),
            ],

            "Auto Mechanics": [
                ("Engine Diagnostics", "Finding engine issues"),
                ("Oil Change", "Basic car maintenance"),
            ],

            "Motorcycle Repair": [
                ("Engine Tuning", "Fine-tuning engines"),
                ("Brake Repair", "Fixing brake systems"),
            ],

            "Home Appliance Repair": [
                ("Washing Machine Repair", "Fixing washers"),
                ("Fridge Repair", "Repairing refrigerators"),
            ],

            "Locksmithing": [
                ("Key Cutting", "Duplicating keys"),
                ("Lock Installation", "Installing locks"),
            ],

            "Tailoring": [
                ("Sewing", "Clothes making & repair"),
                ("Pattern Making", "Creating clothing patterns"),
            ],

            "Shoe Repair": [
                ("Sole Replacement", "Replacing soles"),
                ("Leather Repair", "Fixing leather"),
            ],

            "Glassworking": [
                ("Glass Cutting", "Cutting glass"),
                ("Window Installation", "Installing windows"),
            ],

            "Plastering": [
                ("Wall Smoothing", "Smoothing walls"),
                ("Plaster Finishing", "Final plaster layers"),
            ],

            "Gardening & Landscaping": [
                ("Plant Care", "Taking care of plants"),
                ("Garden Design", "Designing outdoor spaces"),
            ],

            "Bakery & Pastry": [
                ("Bread Making", "Making bread dough"),
                ("Cake Decorating", "Decorating cakes"),
            ],

            "Butchery": [
                ("Meat Cutting", "Cutting meat"),
                ("Knife Handling", "Using knives safely"),
            ],
        }

        for category_name, skill_list in skills.items():

            category = SkillCategory.objects.filter(skill_name=category_name).first()
            if not category:
                self.stdout.write(self.style.WARNING(f"Category NOT FOUND: {category_name} — skipped"))
                continue
            for skill_name, desc in skill_list:
                Skill.objects.get_or_create(
                    name=skill_name,
                    skill_category_id=category,
                    defaults={"description": desc},
                )

        self.stdout.write(self.style.SUCCESS("Skill seeding completed successfully!"))
