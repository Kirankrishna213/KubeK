
# Natural Language to Kubernetes/GitHub Commands

This tool converts natural language instructions into Kubernetes and GitHub management commands.

## Features

- Convert natural language to `kubectl` commands
- Convert natural language to GitHub CLI commands
- Manage multiple Kubernetes contexts
- Execute commands directly or show the generated command

## Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
