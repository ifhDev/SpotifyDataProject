#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e '${BLUE}Setting up Python virtual environment for Spotify Analysis Project...${NC}'

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo 'Python 3 is not installed. Please install Python 3 first.'
    exit 1
fi

# Create virtual environment
echo -e '${BLUE}Creating virtual environment...${NC}'
python3 -m venv .venv

# Activate virtual environment
echo -e '${BLUE}Activating virtual environment...${NC}'
source .venv/bin/activate

# Upgrade pip
echo -e '${BLUE}Upgrading pip...${NC}'
python -m pip install --upgrade pip

# installing uv
echo -e '${BLUE}Installing uv...${NC}'
pip install uv

# Install from pyproject.toml
uv pip install -r <(uv pip compile --quiet pyproject.toml)

# Add kernel to Jupyter
python -m ipykernel install --user --name=spotifydata --display-name 'Python (Spotify Project)'

echo -e '${GREEN}Setup completed successfully!${NC}'
echo -e '${GREEN}Virtual environment is now active.${NC}'
echo -e '${BLUE}To deactivate the virtual environment, type 'deactivate'${NC}'
echo -e '${BLUE}To activate it again later, type 'source .venv/bin/activate'${NC}'

# Print Python and pip versions for verification
echo -e '\n${BLUE}Installed versions:${NC}'
python --version
pip --version 