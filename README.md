# ACP Replay Agent

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python tool for testing and validating [Agent Client Protocol (ACP)](https://agentclientprotocol.com/) implementations by replaying recorded communication sessions.

## Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/acp-replay.git
cd acp-replay
chmod +x replay_agent.py

# Run with example
./replay_agent.py examples/example.log /path/to/your/project
```

## Installation

### Prerequisites

- Python 3.6 or higher

### Clone the Repository

```bash
git clone https://github.com/yourusername/acp-replay.git
cd acp-replay
```

### Make Executable

```bash
chmod +x replay_agent.py
```

## Usage

### Basic Usage

```json
{
  "agent_servers": {
    "replay": {
      "command": "/path/to/acp-replay/replay_agent.py",
      "args": [
        "/path/to/acp-replay/examples/example.log",
        "/path/to/dev/spring-petclinic"
      ]
    }
  }
}
```

**Arguments:**
- `replay_file_path`: Path to the replay log file containing OUT:/IN: markers
- `project_root`: Project root path to replace `cwd` fields during comparison

## Replay File Format

Replay files are basically acp-transport.log files that start with the initialization of your session:

- **OUT:** Expected JSON from the client
- **IN:** JSON output of the agent

### Example Format

```
2025-12-17 11:26:25,895 [  12469]   FINE - AcpTransport - OUT: {"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}
2025-12-17 11:26:27,535 [  14109]   FINE - AcpTransport - IN: {"jsonrpc":"2.0","id":1,"result":{...}}
```

The timestamps, log levels, and prefixes before the markers are ignored during processing.
