"""
Prompts for the user.
"""

class UserPrompts:

    role_description = "Assigns tasks and makes all major decisions"
    
    # Prompts
    system_prompt = "undefined"

    system_prompt_on_each_iteration = "undefined"

    next_prompt = """
You have received a message from {message_sender_name} ({message_sender_role}):
{received_message}
    """

    computer_prompt = """
Send the following message to the project manager:
{response}
"""

