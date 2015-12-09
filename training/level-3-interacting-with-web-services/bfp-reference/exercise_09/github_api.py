"""
This module interacts with the Github API to demonstrate
interaction with RESTful web services.
"""

import requests

from configuration_panda import ConfigurationPanda

credentials = ConfigurationPanda(['PROGRAM_CREDENTIALS'])


class Github:
    """
    Provides access to the Github API.

    Class Attributes:
        urls: Github API url templates for accessing various functionality.

    Attributes:
        oauth_token: A valid OAuth oauth_token for access the API.

    Methods:
        user_info: Provide information on a given Github user.
        user_repos: Provide information on a given users repositories.
        repo_issues: Provide information on a given repo's issues.
        create_issue: Create a new issue on a repo.
        update_issue: Update an issue on a repo.
        create_repo: Create a new repo for the authenticated user.
        update_repo: Update a repo for a specified user.
        delete_repo: Delete a repo for a specified user.
    """
    urls = requests.get("https://api.github.com").json()

    def __init__(self, oauth_token: str):
        self.oauth_token = oauth_token
        self.headers = {'Authorization': 'token {}'.format(self.oauth_token)}

    def user_info(self, username: str) -> requests.Response:
        """
        Obtain information about a given user in Github.

        Args
            username: A str specifying a valid Github username.

        Returns
            A requests.Response object.
        """
        url = self.urls['user_url'].format(user=username)
        return requests.get(url)

    def user_repos(self, username: str) -> requests.Response:
        """
        Obtain information about a given user's repositories in Github.

        Args
            username: A str specifying a valid Github username.

        Returns
            A requests.Response object.
        """
        url = self.urls['user_url'].format(user=username) + "/repos"
        return requests.get(url)

    def repo_issues(self, username: str, repo_name: str) -> requests.Response:
        """
        Obtain information about a given repositories issues in Github.

        Args
            username: A str specifying a valid Github username.
            repo_name: A str specifying a Github repo that belongs to the
                specified user.

        Returns
            A requests.Response object.
        """
        url = (self.urls['repository_url'].format(
            owner=username, repo=repo_name) + "/issues")
        return requests.get(url)

    def create_issue(self, username: str, repo_name: str,
                     title: str, body: str=None,
                     assignee: str=None, milestone: str=None,
                     labels: list=None) -> requests.Response:
        """
        Create an issue on a given repo.

        This method requires authentication and will fail if the requesting
        user does not have pull access on the designated repo.

        Args:
            username: A str of a valid Github username designating
                the owner of the repo.
            repo_name: A str designating the repo to create the issue for.
            title: A str designating the title of the issue.
            body: A str designating the body/description of the issue.
            assignee: Github username to assign the issue to.  Will be
                ignored if issue creator does not have push access to
                repository.
            milestone: Project milestone to assign issue to.  Will be
                ignored if issue creator does not have push access to
                repository.
            labels: A list of strs containing labels for the issue. Will be
                ignored if issue creator does not have push access to
                repository.

        Returns:
            A requests.Response object.
        """
        if labels is None:
            labels = []

        url = (self.urls['repository_url'].format(
            owner=username, repo=repo_name) + "/issues")
        payload = dict(title=title, body=body, assignee=assignee,
                       milestone=milestone, labels=labels)

        return requests.post(url, headers=self.headers, json=payload)

    def update_issue(self, username: str, repo_name: str,
                     issue_number: int, title: str, body: str=None,
                     assignee: str=None, state: str=None,
                     milestone: str=None,
                     labels: list=None) -> requests.Response:
        """
        Create an issue on a given repo.

        This method requires authentication and will fail if the requesting
        user does not have pull access on the designated repo.

        Args:
            username: A str of a valid Github username designating
                the owner of the repo.
            repo_name: A str designating the repo to create the issue for.
            issue_number: A int designating the unique issue number.
            title: A str designating the title of the issue.
            body: A str designating the body/description of the issue.
            assignee: Github username to assign the issue to.  Will be
                ignored if issue creator does not have push access to
                repository.
            state: A str of either 'open' or 'closed' indicating the
                status of the issue.
            milestone: Project milestone to assign issue to.  Will be
                ignored if issue creator does not have push access to
                repository.
            labels: A list of strs containing labels for the issue. Will be
                ignored if issue creator does not have push access to
                repository.

        Returns:
            A requests.Response object.
        """
        if labels is None:
            labels = []

        payload = dict(title=title, body=body, assignee=assignee,
                       milestone=milestone, labels=labels)

        if state is not None:
            payload['state'] = state

        url = (self.urls['repository_url'].format(
            owner=username, repo=repo_name) + "/issues/" + str(issue_number))

        return requests.patch(url, headers=self.headers, json=payload)

    def create_repo(self, name: str, description: str, **kwargs):
        """
        Create a new repository for a given user.  You must be able
        to authenticate as the user for this to work.

        Args:
            name (str): The name of the new repo.

            All other parameters are optional members of the JSON
            request payload.  See the API docs for more information:
            https://developer.github.com/v3/repos/#create

        Returns:
            A requests.Response object.
        """
        payload = dict(
            name=name,
            description=description,
            private=private,
            has_issues=has_issues,
            has_wiki=has_wiki,
            has_downloads=has_downloads,
            auto_init=auto_init,
            gitignore_template=gitignore_template,
            license_template=license_template)

        url = (self.urls['current_user_url'] + '/repos')
        return requests.post(url, headers=self.headers, json=payload)

    def update_repo(self, username: str, repo_name: str,
                    name: str=None, description: str=None, homepage: str=None,
                    private: bool=False, has_issues: bool=True,
                    has_wiki: bool=True, has_downloads: bool=True,
                    default_branch: str=None):
        """
        Update a give user's repo.

        Args:
            username (str): Github username repo belongs to.
            repo_name (str): Name of the repo

            All other parameters are optional members of the JSON
            request payload.  See the API docs for more information:
            https://developer.github.com/v3/repos/#edit


        Returns:
            A requests.Response object.
        """
        if name is None:
            name = repo_name

        payload = dict(
            name=name,
            description=description,
            homepage=homepage,
            private=private,
            has_issues=has_issues,
            has_wiki=has_wiki,
            has_downloads=has_downloads,
            default_branch=default_branch)

        url = (self.urls['repository_url'].format(
            owner=username, repo=repo_name))

        return requests.patch(url, headers=self.headers, json=payload)

    def delete_repo(self, username: str, repo_name: str):
        """
        Delete a repo from a given user's account.

        Args:
            username (str): The user to whom the repo belongs.
            repo_name (str): The repo to delete.

        Returns:
            A requests.Response object.
        """
        url = (self.urls['repository_url'].format(
            owner=username, repo=repo_name))
        return requests.delete(url, headers=self.headers)


if __name__ == "__main__":
    github = Github(oauth_token=credentials.tokens['github'])
    new_repo = github.create_repo(
        name='Test Repo 45',
        description='This is my test repo.',
        gitignore_template='Python',
        license_template='mit')

    updated_repo = github.update_repo(
        username='eikonomega',  # Replace with your Github username.
        repo_name=new_repo.json()['name'],
        description="This is my UPDATED description.",
        homepage="BFPisSoooooooCool.com")


    # Uncomment to delete repo.
    # deleted_repo = github.delete_repo(
        # username='bigfatpanda-training',  # Replace with your Github username.
        # repo_name=new_repo.json()['name'])


