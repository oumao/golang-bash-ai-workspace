#!/usr/bin/env python3
"""
Main agentic AI implementation powered by Claude.
"""

import os
import json
import yaml
from typing import Any, Optional
from anthropic import Anthropic

class AgenticWorkspace:
    """
    Main agentic AI agent for the workspace.
    Integrates Claude with skills, workflows, and steering.
    """
    
    def __init__(self):
        """Initialize the agentic workspace."""
        self.client = Anthropic()
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        # Load configurations
        self.agents_config = self.load_yaml("agents/config.yaml")
        self.skills_config = self.load_yaml("skills/config.yaml")
        self.steering_config = self.load_yaml("steering/config.yaml")
        self.workflows_config = self.load_yaml("workflows/config.yaml")
        self.hooks_config = self.load_yaml("hooks/config.yaml")
        
        # Initialize conversation history
        self.conversation_history = []
        
        # Current agent
        self.current_agent = self.agents_config["agents"][0]
        
        print(f"✓ Initialized {self.current_agent['name']}")
        print(f"✓ Loaded {len(self.skills_config['skills'])} skills")
        print(f"✓ Loaded {len(self.workflows_config['workflows'])} workflows")
        print(f"✓ Ready to assist!\n")
    
    @staticmethod
    def load_yaml(filepath: str) -> dict:
        """Load YAML configuration file."""
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the current agent."""
        steering = self.steering_config
        return steering["system_prompts"]["main_agent"]
    
    def get_available_tools(self) -> list:
        """Convert skills to Claude tool format."""
        tools = []
        
        for skill in self.skills_config['skills']:
            tool = {
                "name": skill['name'],
                "description": skill['description'],
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
            
            # Add parameters as properties
            for param in skill.get('parameters', []):
                prop_def = {
                    "type": param.get('type', 'string'),
                    "description": param.get('description', '')
                }
                
                if param.get('enum'):
                    prop_def['enum'] = param['enum']
                
                tool["input_schema"]["properties"][param['name']] = prop_def
                
                if param.get('required', False):
                    tool["input_schema"]["required"].append(param['name'])
            
            tools.append(tool)
        
        return tools
    
    def execute_skill(self, skill_name: str, parameters: dict) -> str:
        """Execute a skill and return results."""
        print(f"\n🔧 Executing skill: {skill_name}")
        print(f"   Parameters: {json.dumps(parameters, indent=2)}")
        
        # Simulate skill execution
        if skill_name == "execute_go":
            return f"✓ Go code executed successfully"
        elif skill_name == "execute_bash":
            return f"✓ Bash command executed successfully"
        elif skill_name == "read_file":
            try:
                with open(parameters.get('path'), 'r') as f:
                    return f.read()
            except Exception as e:
                return f"✗ Error reading file: {str(e)}"
        elif skill_name == "create_example":
            language = parameters.get('language')
            topic = parameters.get('topic')
            return f"✓ Generated {language.upper()} example for: {topic}"
        else:
            return f"✓ Skill executed: {skill_name}"
    
    def chat(self, user_message: str) -> str:
        """Send a message to the agent and get a response."""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        print(f"\n👤 You: {user_message}")
        
        # Get response from Claude
        response = self.client.messages.create(
            model=self.current_agent['model'],
            max_tokens=self.current_agent['max_tokens'],
            system=self.get_system_prompt(),
            tools=self.get_available_tools(),
            messages=self.conversation_history
        )
        
        # Process response
        assistant_message = {"role": "assistant", "content": response.content}
        self.conversation_history.append(assistant_message)
        
        # Handle tool use if present
        has_tool_use = False
        for block in response.content:
            if block.type == "tool_use":
                has_tool_use = True
                print(f"\n🤖 Agent using tool: {block.name}")
                
                # Execute the tool
                tool_result = self.execute_skill(block.name, block.input)
                
                # Add tool result to conversation
                self.conversation_history.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": tool_result
                        }
                    ]
                })
                
                # Get follow-up response
                follow_up = self.client.messages.create(
                    model=self.current_agent['model'],
                    max_tokens=self.current_agent['max_tokens'],
                    system=self.get_system_prompt(),
                    tools=self.get_available_tools(),
                    messages=self.conversation_history
                )
                
                assistant_message = {"role": "assistant", "content": follow_up.content}
                self.conversation_history.append(assistant_message)
        
        # Extract text response
        response_text = ""
        for block in (follow_up.content if has_tool_use else response.content):
            if hasattr(block, 'text'):
                response_text += block.text
        
        if response_text:
            print(f"\n🤖 Agent: {response_text}")
        
        return response_text
    
    def run_interactive(self):
        """Run the agent in interactive mode."""
        print("=" * 60)
        print(f"Welcome to {self.current_agent['name']}")
        print("=" * 60)
        print("Type 'quit' or 'exit' to end the conversation")
        print("Type 'help' for available commands")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n📝 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit']:
                    print("\n👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self.print_help()
                    continue
                
                self.chat(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
    
    def print_help(self):
        """Print help information."""
        print("\n" + "=" * 60)
        print("Available Commands:")
        print("=" * 60)
        print("  quit/exit     - Exit the agent")
        print("  help          - Show this help message")
        print("\nAvailable Skills:")
        for skill in self.skills_config['skills']:
            print(f"  - {skill['name']}: {skill['description']}")
        print("\nAvailable Workflows:")
        for workflow in self.workflows_config['workflows']:
            print(f"  - {workflow['name']}: {workflow['description']}")
        print("=" * 60)


def main():
    """Main entry point."""
    agent = AgenticWorkspace()
    agent.run_interactive()


if __name__ == "__main__":
    main()
