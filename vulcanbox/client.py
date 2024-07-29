import logging
from typing import Final, List, Optional

import requests

from .constants import Environment
from .models import GithubRepository

logger = logging.getLogger(__name__)


class GithubClient:
    """A class to interact with the GitHub API."""

    BASE_URL: Final[str] = "https://api.github.com"

    def __init__(self) -> None:
        """
        Initialize the GitHubAPI instance.
        """
        Environment.GITHUB_USERNAME.validate()
        Environment.GITHUB_API_TOKEN.validate()

        self.__username = Environment.GITHUB_USERNAME.value
        self.headers = {
            "Authorization": f"Bearer {Environment.GITHUB_API_TOKEN.value}",
            "Accept": "application/vnd.github.v3+json",
        }

    @property
    def username(self) -> str:
        return self.__username

    def create_repo(self, name: str, private: Optional[bool] = False) -> str:
        """
        Create a new GitHub repository.

        Args:
            name (str): The name of the repository
            private (bool): If True, creates a private repository; otherwise, creates a public repository

        Returns:
            str: A message indicating the result of the repository creation.
        """
        url = f"{self.BASE_URL}/user/repos"
        data = {"name": name, "private": private}
        response = requests.post(url, json=data, headers=self.headers)
        if response.status_code == 201:
            return f"Repository {name} created successfully."
        return f"Error: {response.json().get('message', 'Unknown error')}"

    def list_repos(self) -> List[GithubRepository]:
        """
        List all repositories of a user.

        Args:
            username (str): The GitHub username whose repositories are to be listed.

        Returns:
            Union[List[str], str]: A list of repository full names if successful, otherwise an error message.
        """
        url: str = f"{self.BASE_URL}/users/{self.__username}/repos"
        response: requests.Response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            repos_found = [
                GithubRepository.from_json(repo_data) for repo_data in response.json()
            ]
            logger.debug(
                f"Found {len(repos_found)} repositories for user {self.__username}"
            )
            return repos_found
        return []

    def add_collaborator(self, repo: str, username: str, permission: str) -> str:
        """
        Add a collaborator to a repository.

        Args:
            repo (str): The full name of the repository (e.g., "owner/repo").
            username (str): The GitHub username of the collaborator to add.
            permission (str): The permission level to grant to the collaborator (e.g., "pull", "push", "admin").

        Returns:
            str: A message indicating the result of adding the collaborator.
        """
        url = f"{self.BASE_URL}/repos/{repo}/collaborators/{username}"
        data = {"permission": permission}
        response: requests.Response = requests.put(url, json=data, headers=self.headers)
        if response.status_code in [201, 204]:
            return f"Collaborator {username} added to repository {repo}."
        return f"Error: {response.json().get('message', 'Unknown error')}"

    def remove_collaborator(self, repo: str, username: str) -> str:
        """
        Remove a collaborator from a repository.

        Args:
            repo (str): The full name of the repository (e.g., "owner/repo").
            username (str): The GitHub username of the collaborator to remove.

        Returns:
            str: A message indicating the result of removing the collaborator.
        """
        url: str = f"{self.BASE_URL}/repos/{repo}/collaborators/{username}"
        response: requests.Response = requests.delete(url, headers=self.headers)
        if response.status_code == 204:
            return f"Collaborator {username} removed from repository {repo}."
        return f"Error: {response.json().get('message', 'Unknown error')}"
