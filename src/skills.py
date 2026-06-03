#!/usr/bin/env python3
"""
Skills module - Implements tool/skill execution for the agent.
"""

import subprocess
import os
from typing import Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class SkillResult:
    """Result of skill execution."""
    success: bool
    output: str
    error: Optional[str] = None


class SkillExecutor:
    """Executes skills/tools for the agentic system."""
    
    def __init__(self):
        """Initialize the skill executor."""
        self.timeout = 30
        self.max_output_length = 10000
    
    def execute_go(self, code: str, timeout: int = 10) -> SkillResult:
        """Execute Go code."""
        try:
            # Write code to temp file
            with open('/tmp/temp_go_code.go', 'w') as f:
                f.write(code)
            
            # Execute with go run
            result = subprocess.run(
                ['go', 'run', '/tmp/temp_go_code.go'],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                return SkillResult(
                    success=True,
                    output=result.stdout[:self.max_output_length]
                )
            else:
                return SkillResult(
                    success=False,
                    output=result.stdout[:self.max_output_length],
                    error=result.stderr[:self.max_output_length]
                )
        
        except subprocess.TimeoutExpired:
            return SkillResult(
                success=False,
                output="",
                error=f"Execution timeout after {timeout} seconds"
            )
        except Exception as e:
            return SkillResult(
                success=False,
                output="",
                error=str(e)
            )
    
    def execute_bash(self, command: str, timeout: int = 10) -> SkillResult:
        """Execute Bash command."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                return SkillResult(
                    success=True,
                    output=result.stdout[:self.max_output_length]
                )
            else:
                return SkillResult(
                    success=False,
                    output=result.stdout[:self.max_output_length],
                    error=result.stderr[:self.max_output_length]
                )
        
        except subprocess.TimeoutExpired:
            return SkillResult(
                success=False,
                output="",
                error=f"Execution timeout after {timeout} seconds"
            )
        except Exception as e:
            return SkillResult(
                success=False,
                output="",
                error=str(e)
            )
    
    def read_file(self, path: str) -> SkillResult:
        """Read file contents."""
        try:
            if not os.path.exists(path):
                return SkillResult(
                    success=False,
                    output="",
                    error=f"File not found: {path}"
                )
            
            with open(path, 'r') as f:
                content = f.read()
            
            return SkillResult(
                success=True,
                output=content[:self.max_output_length]
            )
        
        except Exception as e:
            return SkillResult(
                success=False,
                output="",
                error=str(e)
            )
    
    def write_file(self, path: str, content: str) -> SkillResult:
        """Write content to a file."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'w') as f:
                f.write(content)
            
            return SkillResult(
                success=True,
                output=f"File written successfully: {path}"
            )
        
        except Exception as e:
            return SkillResult(
                success=False,
                output="",
                error=str(e)
            )
    
    def create_example(self, language: str, topic: str, 
                      complexity: str = "beginner") -> SkillResult:
        """Generate code examples."""
        examples = {
            "go": {
                "variables": {
                    "beginner": """package main
import "fmt"

func main() {
    // Declaring variables
    var name string = "Alice"
    age := 30
    
    fmt.Println("Name:", name)
    fmt.Println("Age:", age)
}"""
                },
                "functions": {
                    "beginner": """package main
import "fmt"

// Simple function
func greet(name string) string {
    return "Hello, " + name
}

func main() {
    message := greet("World")
    fmt.Println(message)
}"""
                }
            },
            "bash": {
                "variables": {
                    "beginner": """#!/bin/bash

# Declaring variables
name="Alice"
age=30

echo "Name: $name"
echo "Age: $age"
"""
                },
                "functions": {
                    "beginner": """#!/bin/bash

# Simple function
greet() {
    echo "Hello, $1"
}

greet "World"
"""
                }
            }
        }
        
        try:
            example = examples.get(language, {}).get(topic, {}).get(complexity)
            
            if example:
                return SkillResult(
                    success=True,
                    output=example
                )
            else:
                return SkillResult(
                    success=False,
                    output="",
                    error=f"No example found for {language} - {topic} - {complexity}"
                )
        
        except Exception as e:
            return SkillResult(
                success=False,
                output="",
                error=str(e)
            )


# Singleton instance
skill_executor = SkillExecutor()
