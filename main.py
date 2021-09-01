import os
import requests
from typing import Union
from dotenv import load_dotenv


# https://developer.todoist.com/rest/v1/
Projects = list[dict[str, Union[int, str, bool]]]
Tasks = list[dict[str, Union[int, str]]]


def main():
    """Prints all Todoist project names, asks the user to choose one, prints all of its active tasks"""
    load_dotenv()
    api_token: str = get_api_token()
    projects: Projects = fetch_projects(api_token)
    print_project_names(projects)
    chosen_project_name: str = input('Enter a project name: ')
    try:
        project_id: int = get_project_id(chosen_project_name, projects)
        active_tasks: Tasks = fetch_active_tasks(project_id, api_token)
        print(f'Here are the active tasks in the {chosen_project_name} project:')
        for task in active_tasks:
            print(task['content'])
    except ValueError as e:
        print(e)


def get_api_token() -> str:
    """Gets the API token from a .env file or directly from the user
    
    If a .env file is not found, the user is asked for the token. If the user
    provides the token, a .env file with the token is created.
    """
    try:
        api_token = os.environ['my_todoist_api_token']
    except KeyError:
        print('Find your Todoist API token in settings > integrations')
        api_token = input('and enter it here: ')
        with open('.env', 'a') as file:
            file.write(f'my_todoist_api_token={api_token}')
    return api_token


def fetch_projects(api_token: str) -> Projects:
    """Fetches all projects"""
    return requests.get(
        'https://api.todoist.com/rest/v1/projects',
        headers={
            'Authorization': f'Bearer {api_token}'}
    ).json()


def print_project_names(projects: Projects) -> None:
    """Prints the names of Todoist projects"""
    print('Here are all of your current Todoist projects:')
    for project in projects:
        print(project['name'])


def get_project_id(chosen_project_name: str, projects: Projects) -> int:
    """Gets a Todoist project's ID by its name
    
    Raises ValueError if the project does not exist.
    """
    for project in projects:
        if project['name'] == chosen_project_name:
            return project['id']
    raise ValueError('Project not found')


def fetch_active_tasks(project_id: int, api_token: str) -> Tasks:
    """Fetches all active tasks in a project"""
    return requests.get(
        'https://api.todoist.com/rest/v1/tasks',
        params={
            'project_id': project_id
        },
        headers={
            'Authorization': f'Bearer {api_token}'
        }).json()


if __name__ == '__main__':
    main()
