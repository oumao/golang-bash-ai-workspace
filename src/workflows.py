#!/usr/bin/env python3
"""
Workflows module - Orchestrates multi-step workflows.
"""

from typing import Any, Dict, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass


class WorkflowStatus(Enum):
    """Workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class WorkflowStepResult:
    """Result of a workflow step."""
    step_id: int
    step_name: str
    status: WorkflowStatus
    output: Any
    error: Optional[str] = None


class Workflow:
    """Represents a workflow with multiple steps."""
    
    def __init__(self, name: str, description: str, steps: List[Dict[str, Any]]):
        """Initialize a workflow."""
        self.name = name
        self.description = description
        self.steps = steps
        self.status = WorkflowStatus.PENDING
        self.results = []
        self.context = {}
    
    def add_context(self, key: str, value: Any):
        """Add context that persists across steps."""
        self.context[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get context value."""
        return self.context.get(key, default)
    
    def execute(self, handlers: Dict[str, Callable]) -> List[WorkflowStepResult]:
        """Execute the workflow."""
        self.status = WorkflowStatus.RUNNING
        self.results = []
        
        try:
            for step in self.steps:
                step_id = step.get('step_id')
                step_name = step.get('name')
                action = step.get('action')
                parameters = step.get('parameters', {})
                
                print(f"\n📍 Executing step {step_id}: {step_name}")
                
                # Get the handler for this action
                handler = handlers.get(action)
                
                if not handler:
                    result = WorkflowStepResult(
                        step_id=step_id,
                        step_name=step_name,
                        status=WorkflowStatus.FAILED,
                        output=None,
                        error=f"No handler found for action: {action}"
                    )
                else:
                    try:
                        # Execute the step
                        output = handler(parameters, self.context)
                        
                        result = WorkflowStepResult(
                            step_id=step_id,
                            step_name=step_name,
                            status=WorkflowStatus.COMPLETED,
                            output=output
                        )
                        
                        # Store output in context for next steps
                        self.add_context(f"step_{step_id}_output", output)
                        
                        print(f"   ✓ Step completed")
                    
                    except Exception as e:
                        result = WorkflowStepResult(
                            step_id=step_id,
                            step_name=step_name,
                            status=WorkflowStatus.FAILED,
                            output=None,
                            error=str(e)
                        )
                        print(f"   ✗ Step failed: {str(e)}")
                
                self.results.append(result)
                
                # Stop if step failed
                if result.status == WorkflowStatus.FAILED:
                    self.status = WorkflowStatus.FAILED
                    break
            
            if self.status != WorkflowStatus.FAILED:
                self.status = WorkflowStatus.COMPLETED
        
        except Exception as e:
            self.status = WorkflowStatus.FAILED
            print(f"✗ Workflow failed: {str(e)}")
        
        return self.results


class WorkflowEngine:
    """Manages workflow execution."""
    
    def __init__(self):
        """Initialize the workflow engine."""
        self.workflows = {}
        self.handlers = self._setup_handlers()
    
    def _setup_handlers(self) -> Dict[str, Callable]:
        """Setup action handlers."""
        return {
            'display_content': self._handle_display_content,
            'execute_go': self._handle_execute_go,
            'execute_bash': self._handle_execute_bash,
            'generate_explanation': self._handle_generate_explanation,
            'create_exercise': self._handle_create_exercise,
            'parse_user_intent': self._handle_parse_intent,
            'select_relevant_skills': self._handle_select_skills,
            'execute_skills_sequence': self._handle_execute_skills,
            'combine_results': self._handle_combine_results,
            'format_response': self._handle_format_response,
        }
    
    def register_workflow(self, workflow: Workflow):
        """Register a workflow."""
        self.workflows[workflow.name] = workflow
    
    def execute_workflow(self, workflow_name: str) -> List[WorkflowStepResult]:
        """Execute a registered workflow."""
        workflow = self.workflows.get(workflow_name)
        
        if not workflow:
            raise ValueError(f"Workflow not found: {workflow_name}")
        
        print(f"\n🚀 Starting workflow: {workflow.name}")
        print(f"   {workflow.description}\n")
        
        results = workflow.execute(self.handlers)
        
        print(f"\n✓ Workflow completed with status: {workflow.status.value}")
        
        return results
    
    # Action handlers
    def _handle_display_content(self, params: Dict, context: Dict) -> str:
        """Handle content display."""
        content = params.get('content', '')
        print(f"📢 {content}")
        return content
    
    def _handle_execute_go(self, params: Dict, context: Dict) -> str:
        """Handle Go execution."""
        code = params.get('code', '')
        print(f"   Executing Go code...")
        return "Go code executed successfully"
    
    def _handle_execute_bash(self, params: Dict, context: Dict) -> str:
        """Handle Bash execution."""
        command = params.get('command', '')
        print(f"   Executing: {command}")
        return "Bash command executed successfully"
    
    def _handle_generate_explanation(self, params: Dict, context: Dict) -> str:
        """Handle explanation generation."""
        topic = params.get('topic', '')
        level = params.get('level', 'beginner')
        print(f"   Generating {level} explanation for: {topic}")
        return f"Explanation for {topic} generated"
    
    def _handle_create_exercise(self, params: Dict, context: Dict) -> str:
        """Handle exercise creation."""
        topic = params.get('topic', '')
        language = params.get('language', '')
        difficulty = params.get('difficulty', 'beginner')
        print(f"   Creating {difficulty} exercise for: {topic} ({language})")
        return f"Exercise created for {topic}"
    
    def _handle_parse_intent(self, params: Dict, context: Dict) -> Dict:
        """Handle intent parsing."""
        print("   Parsing user intent...")
        return {"intent": "learning", "confidence": 0.95}
    
    def _handle_select_skills(self, params: Dict, context: Dict) -> List[str]:
        """Handle skill selection."""
        print("   Selecting relevant skills...")
        return ["execute_go", "create_example", "generate_explanation"]
    
    def _handle_execute_skills(self, params: Dict, context: Dict) -> Dict:
        """Handle skill execution sequence."""
        print("   Executing skills sequence...")
        return {"results": "All skills executed successfully"}
    
    def _handle_combine_results(self, params: Dict, context: Dict) -> Dict:
        """Handle result combination."""
        print("   Combining results...")
        return {"combined": True}
    
    def _handle_format_response(self, params: Dict, context: Dict) -> str:
        """Handle response formatting."""
        print("   Formatting final response...")
        return "Response formatted"


# Singleton instance
workflow_engine = WorkflowEngine()
