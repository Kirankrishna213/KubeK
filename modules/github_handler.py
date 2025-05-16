
from github import Github
from github.GithubException import GithubException
from typing import Dict, Optional, List
import yaml
from pathlib import Path

class GitHubHandler:
    def __init__(self, access_token: str):
        self.g = Github(access_token)
        self.user = self.g.get_user()
    
    def execute_command(self, operation: str, params: Dict[str, str]) -> str:
        try:
            if operation == "list_repos":
                return self._list_repos(params)
            elif operation == "create_repo":
                return self._create_repo(params)
            elif operation == "delete_repo":
                return self._delete_repo(params)
            elif operation == "list_issues":
                return self._list_issues(params)
            elif operation == "create_issue":
                return self._create_issue(params)
            elif operation == "list_pull_requests":
                return self._list_pull_requests(params)
            else:
                return f"Unsupported GitHub operation: {operation}"
        except GithubException as e:
            return f"GitHub error: {str(e)}"
    
    def _list_repos(self, params: Dict[str, str]) -> str:
        repos = self.user.get_repos()
        return "\n".join([repo.name for repo in repos])
    
    def _create_repo(self, params: Dict[str, str]) -> str:
        name = params.get("name")
        if not name:
            return "Error: Repository name required"
            
        private = params.get("private", "false").lower() == "true"
        repo = self.user.create_repo(name, private=private)
        return f"Created repository: {repo.html_url}"
    
    def _delete_repo(self, params: Dict[str, str]) -> str:
        name = params.get("name")
        if not name:
            return "Error: Repository name required"
            
        repo = self.user.get_repo(name)
        repo.delete()
        return f"Deleted repository: {name}"
    
    def _list_issues(self, params: Dict[str, str]) -> str:
        repo_name = params.get("repo")
        if not repo_name:
            return "Error: Repository name required"
            
        repo = self.user.get_repo(repo_name)
        issues = repo.get_issues()
        return "\n".join([f"#{issue.number}: {issue.title}" for issue in issues])
    
    # Implement other operations similarly...
    
    def generate_gh_command(self, operation: str, params: Dict[str, str]) -> str:
        if operation == "list_repos":
            return "gh repo list"
        elif operation == "create_repo":
            private = "--private" if params.get("private", "false") == "true" else "--public"
            return f"gh repo create {params.get('name')} {private}"
        # Add more command generations as needed
