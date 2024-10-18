"""
Klasse AI_RequirementsEngineer abgeleitet von AI_Agent.
"""

import ai_interface
import config
import file
import os
from ai.ai_base import AI_Agent
from prompts.requirements_engineer import RequirementsEngineerPrompts



class AI_RequirementsEngineer(AI_Agent):
    name = "Peter"
    role = "requirements engineer"
    role_ID = "requirements_engineer"
    prompts = RequirementsEngineerPrompts
    role_description = prompts.role_description
    skip_in_role_list = False

    def __init__(self, data):
        super().__init__(data)