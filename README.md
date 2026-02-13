# 🦞 Clawprint

**Blueprint generator for OpenClaw** - Breaks complex tasks into step-by-step build plans using local LLM agents.

Built for small hardware. Runs 100% FREE using Ollama.

## What It Does

Clawprint prevents agents from getting stuck on complex tasks by creating detailed build plans:

- 🎯 **Analyzes complex tasks** and identifies all components
- 🗺️ **Maps dependencies** between components
- 📋 **Creates build sequences** with logical ordering
- ✅ **Adds test checkpoints** for incremental validation
- ⚠️ **Identifies challenges** before you hit them
- 💰 **Completely FREE** - uses local Ollama models

## The Problem It Solves

**Without Clawprint:**
```
User: Build a monitoring dashboard
Agent: [tries to do everything at once]
Agent: [gets overwhelmed, times out, stuck]
```

**With Clawprint:**
```
User: Build a monitoring dashboard
Agent: [generates BUILD_PLAN.md]
Agent: Build skeleton → test ✅
Agent: Build theme → test ✅
Agent: Build layout → test ✅
... continues incrementally until complete
```

## Installation

### Prerequisites

1. **Ollama** - Install from [ollama.ai](https://ollama.ai)

2. **A capable local model** - Clawprint works with many models. Pick one:

**Recommended for planning:**
- `glm-4.7-flash` - Fast, excellent reasoning (4.7B params)
- `qwen2.5-coder:14b` - Strong technical planning (14B params)
- `qwen2.5-coder:32b` - Top-tier planning if you have RAM (32B params)
- `llama3.1:8b` - Solid general-purpose (8B params)
- `llama3.1:70b` - Powerful if hardware allows (70B params)
- `mistral:7b` - Good balance (7B params)
- `mixtral:8x7b` - Excellent reasoning (47B params)
- `deepseek-coder:6.7b` - Code-focused planning (6.7B params)

**Install any with:** `ollama pull <model-name>`

**Minimum recommendation:** Any model 7B+ parameters will work. Smaller models (1-3B) may produce less detailed plans.

3. **Python 3.8+**

### Install Clawprint
```bash
# Clone the repo
git clone https://github.com/JGnft17/clawprint.git
cd clawprint

# Make executable
chmod +x planner.py
```

### Install as OpenClaw Skill (Optional)
```bash
# Copy to OpenClaw skills directory
mkdir -p /mnt/skills/user/clawprint
cp -r . /mnt/skills/user/clawprint/
```

Now OpenClaw agents can use Clawprint automatically!

## Usage

### Basic Usage
```bash
python3 planner.py "Build a Severance-style dashboard with real-time metrics"
```

This creates `BUILD_PLAN.md` in the current directory.

### Specify Output Directory
```bash
python3 planner.py "Your task description" /path/to/output
```

### Real Example
```bash
python3 planner.py "Create a task management app with user authentication, drag-and-drop interface, and real-time collaboration"
```

## Output Example

Clawprint creates a comprehensive build plan:
```markdown
# Build Plan

## 1. Task Overview
Summary of what needs to be built

## 2. Components
- Component A (Simple)
- Component B (Medium) 
- Component C (Complex)

## 3. Dependencies
A → B → C (dependency tree)

## 4. Build Sequence
1. Build A (no dependencies)
2. Test A
3. Build B (depends on A)
4. Test B
...

## 5. Test Checkpoints
What to verify at each step

## 6. Potential Challenges
Known issues and solutions

## 7. Success Criteria
How to know it's done
```

## How It Works

1. **Analyzes** your task description
2. **Identifies** all required components
3. **Maps** dependencies (what needs what)
4. **Creates** logical build order
5. **Adds** test checkpoints
6. **Highlights** potential problems

## Model Support

Clawprint auto-detects and uses the best available local model:

**Recommended models:**
- `glm-4.7-flash` (fast, excellent for planning)
- `qwen2.5-coder:14b` (code-focused)
- `llama3.1:8b` (general purpose)
- `mistral` (balanced)

**Install with:** `ollama pull <model-name>`

## Use Cases

### Dashboard Building
```bash
python3 planner.py "Build monitoring dashboard with live metrics"
```

### Application Development
```bash
python3 planner.py "Create expense tracking app with charts"
```

### API Development
```bash
python3 planner.py "Build REST API for inventory management"
```

### System Integration
```bash
python3 planner.py "Integrate Stripe payments into e-commerce site"
```

## Features

✅ **100% Local** - No API costs, complete privacy  
✅ **Fast** - Generates plans in 1-2 minutes  
✅ **Smart** - Identifies dependencies and ordering  
✅ **Practical** - Creates actionable, testable steps  
✅ **Incremental** - Prevents overwhelming complexity  
✅ **Free Forever** - Uses local Ollama models  

## Troubleshooting

**"No Ollama models found"**
```bash
# Install a model
ollama pull glm-4.7-flash

# Verify it's running
ollama list
```

**"Blueprint seems incomplete"**
- Task description might be too vague
- Try adding more details about requirements
- Re-run with specific features listed

**"Plan doesn't match my expectations"**
- Clawprint makes educated guesses based on description
- Use the plan as a starting framework
- Adjust the sequence to fit your needs

## OpenClaw Integration

When installed as an OpenClaw skill, agents like Smith can use it automatically:
```
User: Build a complex dashboard
Smith: [runs Clawprint to generate BUILD_PLAN.md]
Smith: I've created a build plan. Starting with Component 1...
Smith: [builds incrementally, tests at each checkpoint]
Smith: Dashboard complete!
```

See [SKILL.md](SKILL.md) for details on OpenClaw integration.

## Philosophy

**"Small hardware doing big things"**

Complex projects don't require expensive cloud APIs. With proper planning and incremental execution, local models on small hardware can tackle ambitious builds.

Clawprint breaks overwhelming tasks into manageable pieces, making the impossible possible.

## Companion Tool

**🦞 Clawtographer** - Maps existing codebases  
**🦞 Clawprint** - Plans future builds

Use them together:
1. Clawtographer to understand existing code
2. Clawprint to plan new features
3. Build incrementally with confidence

## Contributing

Issues and PRs welcome! This is an open-source project for the OpenClaw community.

## License

MIT License - see [LICENSE](LICENSE)

---

**Made with 🦞 for the OpenClaw community**# clawprint
Blueprint generator for OpenClaw - breaks complex tasks into step-by-step build plans using local LLM agents
