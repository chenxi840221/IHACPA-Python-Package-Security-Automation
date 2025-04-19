#!/usr/bin/env python3
"""
Adaptive Project Structure Fix Script for Personalized Learning Co-pilot

This script:
1. Analyzes the current project structure
2. Creates missing files and directories based on the reference structure
3. Optionally removes unexpected files and directories (with confirmation)
4. Works with the existing structure instead of enforcing a rigid template
"""

import os
import sys
import shutil
import time
from pathlib import Path

# ANSI colors for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Define the reference project structure
REFERENCE_STRUCTURE = {
    "backend": {
        "api": ["__init__.py", "routes.py", "endpoints.py"],
        "auth": ["__init__.py", "authentication.py", "authorization.py"],
        "models": ["__init__.py", "user.py", "content.py", "learning_plan.py"],
        "rag": ["__init__.py", "document_processor.py", "embedding_manager.py", "retriever.py", "generator.py"],
        "utils": ["__init__.py", "content_processor.py", "logger.py", "db_manager.py"],
        "config": ["__init__.py", "settings.py"],
        "data": {
            "raw": [],
            "processed": [],
            "embeddings": []
        },
        "scrapers": ["__init__.py", "abc_edu_scraper.py"],
        "__init__.py": None,
        "app.py": None,
        "requirements.txt": None,
        "Dockerfile": None
    },
    "frontend": {
        "public": ["index.html", "favicon.ico", "manifest.json"],
        "src": {
            "components": [
                "Login.js", "Register.js", "Dashboard.js", "Navigation.js", 
                "LearningPlan.js", "ContentRecommendation.js", "ProgressTracker.js", "Profile.js"
            ],
            "pages": [
                "HomePage.js", "LoginPage.js", "RegisterPage.js", 
                "DashboardPage.js", "ContentPage.js", "ProfilePage.js"
            ],
            "services": ["api.js", "auth.js", "content.js"],
            "utils": ["helpers.js"],
            "hooks": ["useAuth.js"],
            "context": ["AuthContext.js"],
            "assets": [],
            "App.js": None,
            "App.css": None,
            "index.js": None
        },
        "package.json": None,
        "nginx.conf": None,
        "Dockerfile": None
    },
    "docker-compose.yml": None,
    ".env.example": None,
    "README.md": None
}

# Special paths to always preserve
PRESERVE_PATHS = [
    '.git', 
    '.gitignore', 
    '.env', 
    'venv', 
    'node_modules',
    '__pycache__'
]

def should_preserve(path):
    """Check if a path should be preserved regardless of structure."""
    path = str(path)
    return any(path == p or path.startswith(p + os.sep) for p in PRESERVE_PATHS)

def analyze_structure(root_path, reference_structure):
    """
    Analyze the current project structure and identify issues.
    
    Args:
        root_path: Project root path
        reference_structure: Reference structure to compare against
        
    Returns:
        Dictionary of issues found (missing files/dirs, unexpected files/dirs)
    """
    issues = {
        "missing_dirs": [],
        "missing_files": [],
        "empty_files": [],
        "unexpected_dirs": [],
        "unexpected_files": []
    }
    
    # Check for missing files and directories based on reference structure
    check_missing(root_path, reference_structure, "", issues)
    
    # Check for unexpected files and directories
    check_unexpected(root_path, reference_structure, "", issues)
    
    return issues

def check_missing(root_path, structure, current_path, issues):
    """
    Check for missing files and directories based on reference structure.
    
    Args:
        root_path: Project root path
        structure: Current level of reference structure
        current_path: Current path being checked
        issues: Dictionary to track issues
    """
    for item, sub_structure in structure.items():
        item_path = os.path.join(current_path, item)
        full_path = os.path.join(root_path, item_path)
        
        if isinstance(sub_structure, dict):
            # This is a directory
            if not os.path.exists(full_path):
                issues["missing_dirs"].append(item_path)
            elif not os.path.isdir(full_path):
                issues["missing_dirs"].append(item_path)
            else:
                # Check subdirectories
                check_missing(root_path, sub_structure, item_path, issues)
        elif isinstance(sub_structure, list):
            # This is a directory with specific files
            if not os.path.exists(full_path):
                issues["missing_dirs"].append(item_path)
            elif not os.path.isdir(full_path):
                issues["missing_dirs"].append(item_path)
            else:
                # Check for missing files in this directory
                for file in sub_structure:
                    file_path = os.path.join(item_path, file)
                    full_file_path = os.path.join(root_path, file_path)
                    
                    if not os.path.exists(full_file_path):
                        issues["missing_files"].append(file_path)
                    elif os.path.isdir(full_file_path):
                        issues["missing_files"].append(file_path)
                    elif os.path.getsize(full_file_path) == 0:
                        issues["empty_files"].append(file_path)
        else:
            # This is a file
            if not os.path.exists(full_path):
                issues["missing_files"].append(item_path)
            elif os.path.isdir(full_path):
                issues["missing_files"].append(item_path)
            elif os.path.getsize(full_path) == 0:
                issues["empty_files"].append(item_path)

def check_unexpected(root_path, structure, current_path, issues):
    """
    Check for unexpected files and directories not in reference structure.
    
    Args:
        root_path: Project root path
        structure: Current level of reference structure
        current_path: Current path being checked
        issues: Dictionary to track issues
    """
    current_dir = os.path.join(root_path, current_path)
    
    # Skip if directory doesn't exist yet
    if not os.path.exists(current_dir) or not os.path.isdir(current_dir):
        return
    
    # Get expected items at this level
    expected_items = set(structure.keys())
    
    # Check all items in the current directory
    for item in os.listdir(current_dir):
        item_path = os.path.join(current_path, item)
        full_path = os.path.join(root_path, item_path)
        
        # Skip preserved paths
        if should_preserve(item_path):
            continue
        
        if item not in expected_items:
            if os.path.isdir(full_path):
                issues["unexpected_dirs"].append(item_path)
            else:
                issues["unexpected_files"].append(item_path)
        elif os.path.isdir(full_path):
            # This is an expected directory, check its contents
            if isinstance(structure[item], dict):
                check_unexpected(root_path, structure[item], item_path, issues)
            elif isinstance(structure[item], list):
                # Directory with specific files
                # Check for unexpected files in this directory
                expected_files = set(structure[item])
                for file in os.listdir(full_path):
                    file_path = os.path.join(item_path, file)
                    full_file_path = os.path.join(root_path, file_path)
                    
                    # Skip preserved paths
                    if should_preserve(file_path):
                        continue
                    
                    if file not in expected_files and os.path.isfile(full_file_path):
                        issues["unexpected_files"].append(file_path)

def fix_structure(root_path, issues, remove_unexpected=False):
    """
    Fix project structure issues by creating missing files/dirs and optionally removing unexpected ones.
    
    Args:
        root_path: Project root path
        issues: Dictionary of issues to fix
        remove_unexpected: Whether to remove unexpected files/dirs
        
    Returns:
        Dictionary of actions taken
    """
    actions = {
        "created_dirs": 0,
        "created_files": 0,
        "removed_dirs": 0,
        "removed_files": 0
    }
    
    # Create missing directories
    for dir_path in issues["missing_dirs"]:
        try:
            os.makedirs(os.path.join(root_path, dir_path), exist_ok=True)
            print(f"{Colors.GREEN}Created directory: {dir_path}{Colors.RESET}")
            actions["created_dirs"] += 1
        except Exception as e:
            print(f"{Colors.RED}Error creating directory {dir_path}: {str(e)}{Colors.RESET}")
    
    # Create missing files
    for file_path in issues["missing_files"]:
        try:
            # Make sure parent directory exists
            os.makedirs(os.path.dirname(os.path.join(root_path, file_path)), exist_ok=True)
            
            # Create empty file
            with open(os.path.join(root_path, file_path), 'w') as f:
                pass
            
            print(f"{Colors.GREEN}Created file: {file_path}{Colors.RESET}")
            actions["created_files"] += 1
        except Exception as e:
            print(f"{Colors.RED}Error creating file {file_path}: {str(e)}{Colors.RESET}")
    
    # Remove unexpected items if requested
    if remove_unexpected:
        # Remove unexpected files
        for file_path in issues["unexpected_files"]:
            try:
                os.remove(os.path.join(root_path, file_path))
                print(f"{Colors.YELLOW}Removed unexpected file: {file_path}{Colors.RESET}")
                actions["removed_files"] += 1
            except Exception as e:
                print(f"{Colors.RED}Error removing file {file_path}: {str(e)}{Colors.RESET}")
        
        # Remove unexpected directories
        for dir_path in issues["unexpected_dirs"]:
            try:
                shutil.rmtree(os.path.join(root_path, dir_path))
                print(f"{Colors.YELLOW}Removed unexpected directory: {dir_path}{Colors.RESET}")
                actions["removed_dirs"] += 1
            except Exception as e:
                print(f"{Colors.RED}Error removing directory {dir_path}: {str(e)}{Colors.RESET}")
    
    return actions

def main():
    # Get project root path
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
    else:
        root_path = "./personalized_learning_copilot"
    
    # Check if root path exists
    if not os.path.exists(root_path):
        os.makedirs(root_path, exist_ok=True)
        print(f"{Colors.GREEN}Created project root directory: {root_path}{Colors.RESET}")
    
    print(f"{Colors.BOLD}{Colors.GREEN}Analyzing Personalized Learning Co-pilot project...{Colors.RESET}")
    print("-" * 70)
    
    # Analyze current structure
    issues = analyze_structure(root_path, REFERENCE_STRUCTURE)
    
    # Print issues found
    print(f"\n{Colors.BOLD}Issues found:{Colors.RESET}")
    print(f"Missing directories: {len(issues['missing_dirs'])}")
    print(f"Missing files: {len(issues['missing_files'])}")
    print(f"Empty files: {len(issues['empty_files'])}")
    print(f"Unexpected directories: {len(issues['unexpected_dirs'])}")
    print(f"Unexpected files: {len(issues['unexpected_files'])}")
    
    # If no issues, exit
    if all(len(issue_list) == 0 for issue_list in issues.values()):
        print(f"\n{Colors.GREEN}✓ Project structure is correct! No fixes needed.{Colors.RESET}")
        return 0
    
    # Ask for confirmation to fix issues
    print("\nDo you want to:")
    print("1. Create missing files and directories only")
    print("2. Create missing files/directories AND remove unexpected items")
    print("3. Exit without making changes")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == "3":
        print(f"{Colors.YELLOW}Exiting without making changes.{Colors.RESET}")
        return 0
    
    # Create backup if removing files
    if choice == "2":
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_dir = f"{root_path}_backup_{timestamp}"
        print(f"\n{Colors.YELLOW}Creating backup before removing files: {backup_dir}{Colors.RESET}")
        shutil.copytree(root_path, backup_dir)
    
    # Fix structure
    print(f"\n{Colors.BOLD}Fixing project structure...{Colors.RESET}")
    actions = fix_structure(root_path, issues, remove_unexpected=(choice == "2"))
    
    # Print summary
    print(f"\n{Colors.BOLD}{Colors.GREEN}Project structure fix complete!{Colors.RESET}")
    print("-" * 70)
    print(f"Created {actions['created_dirs']} directories and {actions['created_files']} files")
    
    if choice == "2":
        print(f"Removed {actions['removed_dirs']} unexpected directories and {actions['removed_files']} unexpected files")
        print(f"\n{Colors.YELLOW}Note: Your original files were backed up to {backup_dir}{Colors.RESET}")
    
    # Print remaining empty files
    if issues["empty_files"]:
        print(f"\n{Colors.YELLOW}Warning: The following files are empty and should be populated:{Colors.RESET}")
        for file_path in issues["empty_files"]:
            print(f"  {file_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())