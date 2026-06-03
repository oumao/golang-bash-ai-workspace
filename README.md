# Golang & Bash AI Workspace

A unified workspace for learning Go, Bash, and building agentic AI systems with Claude.

## Directory Structure

```
golang-bash-ai-workspace/
├── golang/
│   └── hello.go              # Go hello world example
├── bash/
│   └── hello.bash            # Bash hello world example
├── agents/                   # Agent definitions
│   └── config.yaml
├── skills/                   # Skills and tool definitions
│   └── config.yaml
├── steering/                 # Steering and system prompts
│   └── config.yaml
├── workflows/                # Workflow definitions
│   └── config.yaml
├── hooks/                    # Event hooks and callbacks
│   └── config.yaml
├── src/                      # Python agentic AI implementation
│   ├── agent.py
│   ├── skills.py
│   └── workflows.py
├── requirements.txt
└── README.md
```

## Features

- **Go Examples**: Learn Go basics with simple programs
- **Bash Scripts**: Learn shell scripting fundamentals
- **Claude Integration**: Agentic AI system powered by Claude
- **Skills Framework**: Extensible skills system for AI agents
- **Workflow Management**: Define and execute complex workflows
- **Steering System**: Control agent behavior with steering configs

## Getting Started

### Prerequisites

- Python 3.9+
- Go 1.21+
- Bash 4.0+
- Claude API key (from Anthropic)

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run Go hello world
cd golang
go run hello.go

# Run Bash hello world
cd ../bash
bash hello.bash
```

### Running the Agent

```bash
python src/agent.py
```

## Configuration

All components use YAML for configuration:

- `agents/config.yaml` - Agent definitions and parameters
- `skills/config.yaml` - Available skills and tools
- `steering/config.yaml` - System prompts and steering directives
- `workflows/config.yaml` - Workflow definitions
- `hooks/config.yaml` - Event hooks and callbacks

## Learning Path

1. Start with `golang/hello.go` and `bash/hello.bash`
2. Explore the `steering/` directory to understand prompt engineering
3. Review `skills/` to learn how to define agent capabilities
4. Study `agents/` to understand agent configuration
5. Check `workflows/` for orchestrating multi-step tasks
6. Implement custom hooks in `hooks/`

## Contributing

This is a personal learning workspace. Feel free to extend and modify!
