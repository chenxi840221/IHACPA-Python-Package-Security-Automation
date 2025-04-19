#!/bin/bash

# Script to find empty files in the project

# Set colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Set minimum file size (in bytes) to consider a file as non-empty
# Files smaller than this size will be reported as "potentially empty"
MIN_SIZE=10

# Set the project root directory
PROJECT_ROOT="./personalized_learning_copilot"

# Count variables
EMPTY_COUNT=0
SMALL_COUNT=0
TOTAL_COUNT=0

# Check if project directory exists
if [ ! -d "$PROJECT_ROOT" ]; then
    echo -e "${RED}Error: Project directory '$PROJECT_ROOT' not found.${NC}"
    echo "Please run this script from the correct location or adjust the PROJECT_ROOT variable."
    exit 1
fi

echo -e "${GREEN}Checking for empty files in $PROJECT_ROOT...${NC}"
echo "----------------------------------------"

# Function to check if a file should be excluded
should_exclude() {
    local file="$1"
    
    # List of patterns to exclude
    local exclude_patterns=(
        "*.pyc"
        "__pycache__"
        ".git"
        "node_modules"
        ".DS_Store"
        "*.log"
        "*.lock"
        "*.swp"
        ".env"
    )
    
    for pattern in "${exclude_patterns[@]}"; do
        if [[ "$file" == *"$pattern"* ]]; then
            return 0  # Should exclude
        fi
    done
    
    return 1  # Should not exclude
}

# Find all files in the project recursively
find "$PROJECT_ROOT" -type f | while read -r file; do
    # Skip excluded files
    if should_exclude "$file"; then
        continue
    fi
    
    # Get file size
    size=$(wc -c < "$file")
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    
    # Check if file is empty (size 0)
    if [ "$size" -eq 0 ]; then
        echo -e "${RED}Empty file:${NC} $file"
        EMPTY_COUNT=$((EMPTY_COUNT + 1))
    # Check if file is very small (might be incomplete)
    elif [ "$size" -lt "$MIN_SIZE" ]; then
        echo -e "${YELLOW}Small file (${size} bytes):${NC} $file"
        SMALL_COUNT=$((SMALL_COUNT + 1))
    fi
done

# Print summary
echo "----------------------------------------"
echo -e "${GREEN}Scan completed.${NC}"
echo "Total files scanned: $TOTAL_COUNT"
echo -e "Empty files found: ${RED}$EMPTY_COUNT${NC}"
echo -e "Small files (< $MIN_SIZE bytes) found: ${YELLOW}$SMALL_COUNT${NC}"

# Suggest next steps
if [ "$EMPTY_COUNT" -gt 0 ] || [ "$SMALL_COUNT" -gt 0 ]; then
    echo -e "\n${GREEN}Suggested actions:${NC}"
    echo "1. Review empty/small files and populate them with the proper code."
    echo "2. If some files are intentionally empty, you can ignore them or add a comment."
    echo "3. Run this script again after making changes to verify all files are properly populated."
else
    echo -e "\n${GREEN}Great! All files have content.${NC}"
fi

exit 0