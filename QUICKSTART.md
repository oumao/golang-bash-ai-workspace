# Quick Start Guide

## Prerequisites

- Python 3.9 or higher
- Go 1.21 or higher
- Bash 4.0 or higher
- Anthropic API key (get one at https://console.anthropic.com)

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/oumao/golang-bash-ai-workspace.git
cd golang-bash-ai-workspace
```

### 2. Create environment file
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running Examples

### Run Go Hello World
```bash
make go-hello
```

### Run Bash Hello World
```bash
make bash-hello
```

### Run the Claude Agent
```bash
python src/agent.py
# or
make run-agent
```

## Interactive Agent Usage

When you run the agent, you can:

1. **Ask for Go examples**
   ```
   You: Show me a Go example for working with variables
   ```

2. **Ask for Bash tutorials**
   ```
   You: Teach me about Bash functions
   ```

3. **Execute code**
   ```
   You: Execute this Go code: package main; import "fmt"; func main() { fmt.Println("Hello") }
   ```

4. **Get learning workflows**
   ```
   You: Start the Go basics learning workflow
   ```

5. **Type `help`** for available commands

## Configuration Files

- `agents/config.yaml` - Define agents and their behavior
- `skills/config.yaml` - Define available tools and skills
- `steering/config.yaml` - System prompts and directives
- `workflows/config.yaml` - Multi-step workflows
- `hooks/config.yaml` - Event handlers and callbacks

## Project Structure

```
golang-bash-ai-workspace/
├── golang/              # Go examples and exercises
├── bash/                # Bash examples and exercises
├── src/                 # Python agentic AI implementation
│   ├── agent.py        # Main agent
│   ├── skills.py       # Skill executors
│   └── workflows.py    # Workflow engine
├── agents/             # Agent configurations
├── skills/             # Skill definitions
├── steering/           # System prompts
├── workflows/          # Workflow definitions
├── hooks/              # Event hooks
└── README.md          # Full documentation
```

## Next Steps

1. **Learn Go**: Modify `golang/hello.go` and explore Go features
2. **Learn Bash**: Modify `bash/hello.bash` and try different commands
3. **Build Agents**: Create custom agents in `agents/config.yaml`
4. **Define Skills**: Add new skills in `skills/config.yaml`
5. **Create Workflows**: Build multi-step workflows in `workflows/config.yaml`

## Troubleshooting

### "ANTHROPIC_API_KEY environment variable not set"
```bash
# Make sure you've set the API key in .env
cat .env
export ANTHROPIC_API_KEY=your_key_here
```

### "Go not found"
```bash
# Install Go from https://golang.org/dl
go version  # Verify installation
```

### "Bash not found"
```bash
# Bash should be pre-installed on most systems
bash --version  # Verify installation
```

## Additional Resources

- [Anthropic Claude API Docs](https://docs.anthropic.com)
- [Go Documentation](https://golang.org/doc)
- [Bash Manual](https://www.gnu.org/software/bash/manual/)
- [Project README](README.md)
