# config.py
# You'll need to rename this template to config.py and fill in the necessary information. This file contains the configuration for the project, such as the project name, the user name, the project directory, and the OpenAI API key. The configuration is used by the AI agent to generate prompts and interact with the project files. Here's a breakdown of the configuration options:

import os

# OpenAI API settings
OPENAI_API_KEY = 'sk-your-api-key'
OPENAI_MODEL = 'gpt-4o-mini'


# user information
USER_NAME = "Paul"

# Project name
PROJECT_NAME = "Your project name"

# Project path
PROJECT_DIR = "Your/project/directory"
# Subdirectories
PROJECT_OVERVIEW_DIR = os.path.join(PROJECT_DIR, 'overview')
PROJECT_STAKEHOLDER_REQS_DIR = os.path.join(PROJECT_DIR, 'stakeholder_requirements')
PROJECT_SYSTEM_REQS_DIR = os.path.join(PROJECT_DIR, 'system_requirements')
PROJECT_ARCHITECTURE_DIR = os.path.join(PROJECT_DIR, 'architecture')
PROJECT_COMPONENT_REQS_DIR = os.path.join(PROJECT_DIR, 'component_requirements')
PROJECT_COMPONENT_DESIGN_DIR = os.path.join(PROJECT_DIR, 'component_design')
PROJECT_SOURCE_CODE_DIR = os.path.join(PROJECT_DIR, 'source_code')
PROJECT_TESTPLAN_DIR = os.path.join(PROJECT_DIR, 'testplan')
PROJECT_TESTCASES_DIR = os.path.join(PROJECT_DIR, 'testcases')
PROJECT_TEST_IMPLEMENTATION_DIR = os.path.join(PROJECT_DIR, 'test_implementation')



# Prompt template directory
PROMPT_TEMPLATES_DIR = os.path.join(os.getcwd(), 'prompt_templates')


# Enable debug mode?
DEBUG = False