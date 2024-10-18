"""
Klasse AI_ProjectManager abgeleitet von AI_Agent.
"""

import ai_interface
import config
import file
import os
from ai.ai_base import AI_Agent
from prompts.project_manager import ProjectManagerPrompts



class AI_ProjectManager(AI_Agent):
    
    name = "Alex"
    role = "projekt manager"
    role_ID = "project_manager"
    prompts = ProjectManagerPrompts
    role_description = prompts.role_description
    skip_in_role_list = False

    def __init__(self, data):
        super().__init__(data)

