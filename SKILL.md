---
name: clawprint
description: "Blueprint generator for complex task planning - breaks tasks into step-by-step build plans"
---

# Clawprint Skill

## Overview
Clawprint is a blueprint generator that breaks complex tasks into step-by-step build plans using local LLM agents. It prevents agents from getting stuck on overwhelming tasks by creating clear, incremental execution paths.

## When to Use Clawprint

Use Clawprint whenever:
- User asks you to build something complex (dashboards, applications, multi-file projects)
- A task has multiple components that could be built in different orders
- You're unsure where to start on a large project
- Previous attempts at similar tasks resulted in timeouts or getting stuck
- The task description is vague and needs decomposition

**Common triggers:**
- "Build a [complex thing]"
- "Create a [multi-component system]"
- "Make me a [application/dashboard/tool]"
- "I need a [project that requires planning]"

**DO NOT use for:**
- Simple single-file tasks
- Editing existing code
- Answering questions
- Tasks with clear, single steps

## What Clawprint Does

1. **Analyzes** the task description
2. **Identifies** all required components
3. **Maps** dependencies between components
4. **Orders** build steps logically
5. **Adds** test checkpoints
6. **Highlights** potential challenges
7. **Defines** success criteria

**Output:** `BUILD_PLAN.md` with structured build instructions

## How to Use Clawprint

### Basic Usage
```bash
python3 ~/clawprint/planner.py "Build a Severance-style dashboard"
```

This creates `BUILD_PLAN.md` in the current directory.

### With Custom Output Location
```bash
python3 ~/clawprint/planner.py "Task description" /path/to/output
```

### Example Workflow

1. **User gives complex task:** "Build a real-time monitoring dashboard"
2. **Run Clawprint:** Generate BUILD_PLAN.md
3. **Read the plan:** Understand components and sequence
4. **Execute incrementally:** Build Component 1 → Test → Component 2 → Test...
5. **Follow checkpoints:** Verify each piece works before moving on

## Output Format

Clawprint creates a BUILD_PLAN.md with these sections:

### 1. Task Overview
High-level summary of what needs to be built

### 2. Components
List of all modules/pieces needed with:
- Name
- Purpose  
- Complexity (Simple/Medium/Complex)

### 3. Dependencies
Which components depend on which others (dependency tree)

### 4. Build Sequence
Step-by-step order to build components with reasoning:
1. Component X (reason: no dependencies)
2. Component Y (reason: depends on X)
etc.

### 5. Test Checkpoints
What to verify after each major component

### 6. Potential Challenges
What could go wrong, what's tricky

### 7. Success Criteria
How to know it's complete and working

## Integration with OpenClaw Workflow

**Before Clawprint (Problem):**
```
User: Build complex dashboard
Agent: [tries to do everything at once]
Agent: [gets overwhelmed, times out, gets stuck]
```

**After Clawprint (Solution):**
```
User: Build complex dashboard
Agent: [runs Clawprint to generate plan]
Agent: [reads BUILD_PLAN.md]
Agent: [builds Component 1]
Agent: [tests Component 1]
Agent: [builds Component 2]
Agent: [tests Component 2]
... continues incrementally
```

## Model Support

Clawprint uses local Ollama models (100% free):

**Recommended models:**
- `glm-4.7-flash` (fast, smart planning)
- `qwen2.5-coder:14b` (technical focus)
- `llama3.1:8b` (general purpose)
- `mistral` (balanced)

Auto-detects and uses the best available model.

## Cost

**Always FREE** - uses local models only. No API costs ever.

## Best Practices

### When to Generate a Blueprint
- **At the START** of complex tasks
- **Before coding** anything substantial
- **When stuck** on how to approach something

### How to Use the Blueprint
- **Read it fully** before starting
- **Follow the sequence** - don't skip steps
- **Test at checkpoints** - verify before moving on
- **Refer back** if you get stuck

### When NOT to Use
- Simple edits or fixes
- Single-file scripts
- When you already have a clear plan
- Answering questions (no building involved)

## Example Use Cases

**Dashboard Building:**
```bash
python3 ~/clawprint/planner.py "Build a monitoring dashboard with real-time metrics"
```

**Application Development:**
```bash
python3 ~/clawprint/planner.py "Create a task management app with authentication"
```

**System Integration:**
```bash
python3 ~/clawprint/planner.py "Integrate payment processing into existing web app"
```

**API Development:**
```bash
python3 ~/clawprint/planner.py "Build REST API for user management with auth"
```

## Troubleshooting

**"No Ollama models found"**
- Install Ollama: `brew install ollama`
- Pull a model: `ollama pull glm-4.7-flash`

**"Blueprint seems incomplete"**
- Task description might be too vague
- Try being more specific about requirements
- Re-run with more detail

**"Plan doesn't match my needs"**
- Clawprint makes educated guesses
- Use the plan as a starting point
- Adjust sequence as needed

## Philosophy

Clawprint embodies the "small hardware doing big things" philosophy:
- **Free:** No API costs, runs locally
- **Fast:** Generates plans in 1-2 minutes
- **Practical:** Creates actionable, testable steps
- **Incremental:** Prevents overwhelming complexity

Complex tasks become manageable when broken into small, tested pieces.

---

**Made with 🦞 for OpenClaw agents who tackle big projects**
