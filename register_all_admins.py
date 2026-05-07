import os
import re

def register_models():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    apps_processed = 0
    
    # List of directories to skip
    skip_dirs = {'.git', '__pycache__', 'venv', 'env', 'media', 'staticfiles', '.gemini'}

    for root, dirs, files in os.walk(base_dir):
        # Skip hidden and excluded directories
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
        
        if 'models.py' in files:
            app_dir = root
            models_file = os.path.join(app_dir, 'models.py')
            admin_file = os.path.join(app_dir, 'admin.py')
            
            try:
                with open(models_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Regex to find class definitions
                # Matches: class ModelName(models.Model): or class ModelName(AbstractUser): etc.
                model_matches = re.findall(r'class\s+(\w+)\s*\((?:models\.)?(?:Model|AbstractUser|AbstractBaseUser)\):', content)
                
                models = sorted(list(set(model_matches))) # Unique and sorted models
                
                if not models:
                    continue
                
                # Generate admin.py content
                admin_content = "from django.contrib import admin\n"
                
                # Check for AbstractUser to decide on imports
                if 'AbstractUser' in content or 'AbstractBaseUser' in content:
                    admin_content += "from django.contrib.auth.admin import UserAdmin\n"
                
                admin_content += f"from .models import {', '.join(models)}\n\n"
                
                for model in models:
                    # Basic registration
                    admin_content += f"admin.site.register({model})\n"
                
                with open(admin_file, 'w', encoding='utf-8') as f:
                    f.write(admin_content)
                
                print(f"Successfully registered models in {os.path.relpath(admin_file, base_dir)}: {', '.join(models)}")
                apps_processed += 1
                
            except Exception as e:
                print(f"Error processing {models_file}: {str(e)}")

    print(f"\nDone! Processed {apps_processed} apps.")

if __name__ == '__main__':
    register_models()
