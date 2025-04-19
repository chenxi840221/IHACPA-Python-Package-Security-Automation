#!/bin/bash
# Script to set up the correct file structure for Personalized Learning Co-pilot
# Creates missing files and removes unnecessary ones

# Set colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Define project root
PROJECT_ROOT="./personalized_learning_copilot"

# Make sure project root exists
mkdir -p "$PROJECT_ROOT"

echo -e "${GREEN}Setting up Personalized Learning Co-pilot project structure...${NC}"

# Create backend structure
echo -e "${YELLOW}Creating backend structure...${NC}"
mkdir -p "$PROJECT_ROOT/backend/api"
mkdir -p "$PROJECT_ROOT/backend/auth"
mkdir -p "$PROJECT_ROOT/backend/models"
mkdir -p "$PROJECT_ROOT/backend/rag"
mkdir -p "$PROJECT_ROOT/backend/utils"
mkdir -p "$PROJECT_ROOT/backend/config"
mkdir -p "$PROJECT_ROOT/backend/data/raw"
mkdir -p "$PROJECT_ROOT/backend/data/processed"
mkdir -p "$PROJECT_ROOT/backend/data/embeddings"
mkdir -p "$PROJECT_ROOT/backend/scrapers"

# Create frontend structure
echo -e "${YELLOW}Creating frontend structure...${NC}"
mkdir -p "$PROJECT_ROOT/frontend/public"
mkdir -p "$PROJECT_ROOT/frontend/src/components"
mkdir -p "$PROJECT_ROOT/frontend/src/pages"
mkdir -p "$PROJECT_ROOT/frontend/src/services"
mkdir -p "$PROJECT_ROOT/frontend/src/utils"
mkdir -p "$PROJECT_ROOT/frontend/src/hooks"
mkdir -p "$PROJECT_ROOT/frontend/src/context"
mkdir -p "$PROJECT_ROOT/frontend/src/assets"

# Create required files if they don't exist
echo -e "${YELLOW}Creating essential files...${NC}"

# Backend files
touch_if_missing() {
    if [ ! -f "$1" ]; then
        echo -e "${GREEN}Creating $1${NC}"
        touch "$1"
    else
        echo -e "${YELLOW}File already exists: $1${NC}"
    fi
}

# Backend Python files
touch_if_missing "$PROJECT_ROOT/backend/__init__.py"
touch_if_missing "$PROJECT_ROOT/backend/app.py"
touch_if_missing "$PROJECT_ROOT/backend/requirements.txt"

touch_if_missing "$PROJECT_ROOT/backend/api/__init__.py"
touch_if_missing "$PROJECT_ROOT/backend/api/routes.py"
touch_if_missing "$PROJECT_ROOT/backend/api/endpoints.py"

touch_if_missing "$PROJECT_ROOT/backend/auth/__init__.py"
touch_if_missing "$PROJECT_ROOT/backend/auth/authentication.py"
touch_if_missing "$PROJECT_ROOT/backend/auth/authorization.py"

touch_if_missing "$PROJECT_ROOT/backend/models/__init__.py"
touch_if_missing "$PROJECT_ROOT/backend/models/user.py"
touch_if_missing "$PROJECT_ROOT/backend/models/content.py"
touch_if_missing "$PROJECT_ROOT/backend/models/learning_plan.py"

touch_if_missing "$PROJECT_ROOT/backend/rag/__init__.py"
touch_if_missing "$PROJECT_ROOT/backend/rag/document_processor.py"
touch_if_missing "$PROJECT_ROOT/backend/rag/embedding_manager.py"
touch_if_missing "$PROJECT_ROOT/backend/rag/retriever.py"
touch_if_missing "$PROJECT_ROOT/backend/rag/generator.py"

touch_if_missing "$PROJECT_ROOT/backend/utils/__init__.py"
touch_if_missing "$PROJECT_ROOT/backend/utils/content_processor.py"
touch_if_missing "$PROJECT_ROOT/backend/utils/logger.py"
touch_if_missing "$PROJECT_ROOT/backend/utils/db_manager.py"

touch_if_missing "$PROJECT_ROOT/backend/config/__init__.py"
touch_if_missing "$PROJECT_ROOT/backend/config/settings.py"

touch_if_missing "$PROJECT_ROOT/backend/scrapers/__init__.py"
touch_if_missing "$PROJECT_ROOT/backend/scrapers/abc_edu_scraper.py"

touch_if_missing "$PROJECT_ROOT/backend/Dockerfile"

# Frontend files
touch_if_missing "$PROJECT_ROOT/frontend/package.json"
touch_if_missing "$PROJECT_ROOT/frontend/public/index.html"
touch_if_missing "$PROJECT_ROOT/frontend/public/favicon.ico"
touch_if_missing "$PROJECT_ROOT/frontend/public/manifest.json"

touch_if_missing "$PROJECT_ROOT/frontend/src/index.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/App.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/App.css"

touch_if_missing "$PROJECT_ROOT/frontend/src/components/Login.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/components/Register.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/components/Dashboard.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/components/Navigation.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/components/LearningPlan.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/components/ContentRecommendation.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/components/ProgressTracker.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/components/Profile.js"

touch_if_missing "$PROJECT_ROOT/frontend/src/pages/HomePage.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/pages/LoginPage.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/pages/RegisterPage.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/pages/DashboardPage.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/pages/ContentPage.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/pages/ProfilePage.js"

touch_if_missing "$PROJECT_ROOT/frontend/src/services/api.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/services/auth.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/services/content.js"

touch_if_missing "$PROJECT_ROOT/frontend/src/utils/helpers.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/hooks/useAuth.js"
touch_if_missing "$PROJECT_ROOT/frontend/src/context/AuthContext.js"

touch_if_missing "$PROJECT_ROOT/frontend/nginx.conf"
touch_if_missing "$PROJECT_ROOT/frontend/Dockerfile"

# Root files
touch_if_missing "$PROJECT_ROOT/docker-compose.yml"
touch_if_missing "$PROJECT_ROOT/.env.example"
touch_if_missing "$PROJECT_ROOT/README.md"

# Check for unnecessary/misplaced files
echo -e "${YELLOW}Checking for unnecessary files...${NC}"

# Define required files and directories
declare -a required_dirs=(
    "$PROJECT_ROOT/backend/api"
    "$PROJECT_ROOT/backend/auth"
    "$PROJECT_ROOT/backend/models"
    "$PROJECT_ROOT/backend/rag"
    "$PROJECT_ROOT/backend/utils"
    "$PROJECT_ROOT/backend/config"
    "$PROJECT_ROOT/backend/data"
    "$PROJECT_ROOT/backend/scrapers"
    "$PROJECT_ROOT/frontend/public"
    "$PROJECT_ROOT/frontend/src"
)

# Find all directories in the project
find "$PROJECT_ROOT" -type d | while read -r dir; do
    # Skip the root directory and required directories
    if [[ "$dir" == "$PROJECT_ROOT" ]]; then
        continue
    fi
    
    skip=false
    for required_dir in "${required_dirs[@]}"; do
        if [[ "$dir" == "$required_dir" || "$dir" == "$required_dir"/* ]]; then
            skip=true
            break
        fi
    done
    
    if [[ "$skip" == false ]]; then
        echo -e "${RED}Unexpected directory found: $dir${NC}"
        read -p "Remove this directory? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$dir"
            echo -e "${GREEN}Removed directory: $dir${NC}"
        else
            echo -e "${YELLOW}Keeping directory: $dir${NC}"
        fi
    fi
done

echo -e "${GREEN}Project structure setup complete!${NC}"
echo "Now you can copy your code into the appropriate files."