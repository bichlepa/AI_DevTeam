"""
Klasse AI_Architect abgeleitet von AI_Agent.
"""

import ai_interface
import config
import file
import os
from ai.ai_base import AI_Agent
from prompts.architect import ArchitectPrompts



class AI_Architect(AI_Agent):
    name = "Robert"
    role = "architect"
    role_ID = "architect"
    prompts = ArchitectPrompts
    role_description = prompts.role_description
    skip_in_role_list = False

    def __init__(self, data):
        super().__init__(data)