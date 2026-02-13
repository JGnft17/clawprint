#!/usr/bin/env python3
"""
Clawprint - Blueprint Generator for OpenClaw
Breaks complex tasks into step-by-step build plans using local LLM agents
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


class Clawprint:
    def __init__(self, output_dir=".", model=None, config_path=None):
        self.output_dir = Path(output_dir)
        self.script_dir = Path(__file__).parent
        
        # Load config with validation
        if config_path is None:
            config_path = self.script_dir / "config.json"
        
        try:
            with open(config_path) as f:
                config = json.load(f)
            
            # Validate required keys and set defaults
            self.config = {
                "model_preference": config.get("model_preference", "auto"),
                "planning_timeout": config.get("planning_timeout", 180),
                "output_format": config.get("output_format", "markdown"),
                "plan_detail_level": config.get("plan_detail_level", "comprehensive")
            }
            
        except Exception as e:
            print(f"[WARN] Failed to load config: {e}, using defaults")
            self.config = {
                "model_preference": "auto",
                "planning_timeout": 180,
                "output_format": "markdown",
                "plan_detail_level": "comprehensive"
            }
        
        # Check Ollama
        self.model = model or self._select_model()
        if not self.model:
            print("ERROR: No Ollama models found. Install with: ollama pull glm-4.7-flash")
            sys.exit(1)
        
        print(f"[INFO] Using model: {self.model}")
        
        # Create output directory
        try:
            self.output_dir.mkdir(exist_ok=True, parents=True)
        except Exception as e:
            print(f"ERROR: Cannot create output directory: {e}")
            sys.exit(1)
    
    def _check_ollama(self):
        """Check for Ollama and return available models"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return []
            
            lines = result.stdout.strip().split('\n')[1:]
            if not lines:
                return []
            
            models = []
            for line in lines:
                if line.strip():
                    model_name = line.split()[0]
                    models.append(model_name)
            
            return models
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []
    
    def _select_model(self):
        """Select best available model based on config preference"""
        available = self._check_ollama()
        
        if not available:
            return None
        
        pref = self.config.get("model_preference", "auto")
        
        if pref != "auto":
            # User specified a model
            for model in available:
                if pref in model:
                    return model
            print(f"[WARN] Preferred model '{pref}' not found, using auto-selection")
        
        # Auto-select: priority order
        priority = ["glm-4.7-flash", "qwen2.5-coder", "llama3.1", "mistral"]
        
        for preferred in priority:
            for model in available:
                if preferred in model.lower():
                    return model
        
        # Use first available
        return available[0]
    
    def _validate_blueprint(self, content):
        """Validate blueprint has required sections"""
        required_sections = [
            "Task Overview",
            "Components",
            "Build Sequence"
        ]
        
        for section in required_sections:
            if section.lower() not in content.lower():
                print(f"[WARN] Blueprint missing section: {section}")
                return False
        
        return True
    
    def create_blueprint(self, task_description):
        """Create a build plan from task description"""
        print(f"[INFO] Creating blueprint for: {task_description[:50]}...")
        
        detail_level = self.config.get("plan_detail_level", "comprehensive")
        
        if detail_level == "comprehensive":
            sections = """## 1. Task Overview
Brief summary of what needs to be built.

## 2. Components
List all components/modules needed. For each:
- Name
- Purpose
- Estimated complexity (Simple/Medium/Complex)

## 3. Dependencies
Which components depend on which others? Create a dependency tree.

## 4. Build Sequence
Step-by-step order to build components:
1. Component X (reason: no dependencies)
2. Component Y (reason: depends on X)
etc.

## 5. Test Checkpoints
After each major component, what should be tested?

## 6. Potential Challenges
What could go wrong? What's tricky?

## 7. Success Criteria
How do we know it's complete and working?"""
        else:
            sections = """## 1. Task Overview
## 2. Components
## 3. Build Sequence
## 4. Success Criteria"""
        
        prompt = f"""You are a technical architect breaking down a complex software task into a step-by-step build plan.

Task: {task_description}

Create a BUILD_PLAN.md with these sections:

{sections}

Be specific. Be practical. Think like an engineer building incrementally.

Provide the complete BUILD_PLAN.md in markdown format."""
        
        timeout = self.config.get("planning_timeout", 180)
        
        try:
            print(f"[INFO] Generating blueprint (timeout: {timeout}s)...")
            
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                blueprint = result.stdout.strip()
                
                if not blueprint:
                    print("[ERROR] Model returned empty response")
                    return None
                
                # Validate output
                if not self._validate_blueprint(blueprint):
                    print("[ERROR] Blueprint failed validation - missing required sections")
                    print("[INFO] Saving anyway, but may be incomplete")
                
                return self._create_final_blueprint(task_description, blueprint)
            else:
                print(f"[ERROR] Ollama failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"[ERROR] Blueprint generation timed out after {timeout}s")
            return None
        except Exception as e:
            print(f"[ERROR] {e}")
            return None
    
    def _create_final_blueprint(self, task, content):
        """Create final blueprint with metadata"""
        blueprint = f"""# Build Plan

**Task:** {task}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Tool:** Clawprint (OpenClaw)
**Model:** {self.model} (local/free)

---

{content}

---

*This blueprint was automatically generated by Clawprint.  
Follow steps incrementally, test after each checkpoint.*
"""
        return blueprint
    
    def save_blueprint(self, blueprint, filename="BUILD_PLAN.md"):
        """Save blueprint to file"""
        output_path = self.output_dir / filename
        try:
            output_path.write_text(blueprint)
            print(f"[INFO] Blueprint saved to: {output_path}")
            return output_path
        except Exception as e:
            print(f"[ERROR] Failed to save blueprint: {e}")
            return None
    
    def run(self, task_description):
        """Generate and save blueprint"""
        print("[INFO] Clawprint starting...")
        
        if not task_description:
            print("[ERROR] No task description provided")
            return None
        
        blueprint = self.create_blueprint(task_description)
        
        if blueprint:
            return self.save_blueprint(blueprint)
        else:
            return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 planner.py \"<task description>\" [output_dir]")
        print("Example: python3 planner.py \"Build a Severance-style dashboard\" .")
        print("")
        print("Clawprint uses LOCAL Ollama models (free).")
        sys.exit(1)
    
    task = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "."
    
    planner = Clawprint(output)
    planner.run(task)
