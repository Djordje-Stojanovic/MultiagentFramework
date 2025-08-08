# MultiAgent Framework - Cline Project Brief

## Project Overview
MultiAgent Framework is a comprehensive platform for building and managing multi-agent systems. This document serves as a reference for Cline about the project capabilities and available tools.

## Available MCP Servers

### 1. Git Server (Local Repository Management)
**Server Name:** `github.com/modelcontextprotocol/servers/tree/main/src/git`
**Purpose:** Local git repository operations and version control
**Repository:** `d:/bkp/DEV/Stojanovic-One`

**Capabilities:**
- View git commit history and logs
- Check repository status and file changes
- Browse file contents at different commits
- Analyze git diffs and code changes
- Track file modifications and staging
- Repository insights and statistics

### 2. GitHub MCP Server (Remote GitHub Operations)
**Server Name:** `github.com/github/github-mcp-server`
**Purpose:** Complete GitHub API integration for remote repository management
**Authentication:** Personal Access Token with full repository permissions

**Available Tool Categories:**
- **Repository Management**: Browse code, search files, analyze commits, manage branches
- **Issues & Pull Requests**: Create, update, manage issues and PRs, handle reviews
- **GitHub Actions**: Monitor workflows, analyze build failures, manage CI/CD
- **Code Security**: Review security alerts, Dependabot findings, secret scanning
- **Notifications**: Manage GitHub notifications and subscriptions
- **Gists**: Create and manage code snippets
- **Organizations**: Search and manage GitHub organizations
- **Users**: Search GitHub users and profiles

**Key Tools Include:**
- `get_me` - Get authenticated user profile
- `search_repositories` - Search GitHub repositories
- `create_repository` - Create new repositories
- `list_issues` - List repository issues
- `create_issue` - Create new issues
- `get_file_contents` - Read repository files
- `create_or_update_file` - Modify repository files
- `create_pull_request` - Create pull requests
- `list_notifications` - Check GitHub notifications
- `search_code` - Search code across GitHub
- And 100+ more tools for comprehensive GitHub management

## Project Structure
```
MultiagentFramework/
├── README.md           # Project documentation
├── Cline.md           # This file - Cline's project reference
└── .git/              # Git repository data
```

## Instructions for Cline
When working on this project:
1. **Read this file first** to understand available capabilities
2. **Use git server** for local repository operations and version control
3. **Use GitHub server** for remote repository management and collaboration
4. **Create issues** on GitHub for tracking project tasks and features
5. **Commit changes** regularly with meaningful commit messages
6. **Push to GitHub** to maintain remote backup and collaboration

## Development Guidelines
- Follow semantic versioning for releases
- Use descriptive commit messages
- Create feature branches for new development
- Use GitHub Issues for task tracking
- Document all major features and APIs
- Test thoroughly before merging to main

---
*This document will be expanded as the project grows and new capabilities are added.*
