#!/usr/bin/env python3

from urllib.parse import urljoin

import requests

class API(object):

    def __init__(self, base_url):
        """ Creates the API client.
        Paramaters:
            base_url (str): The base url for the API.
        Returns:
            New API class for testing an API.
        """
        self.base_url = base_url

    def create_task(self, cookie, Text, Date):
        """ Create a new task
        Parameters:
            cookie (str): Pre-authorized cookie
            Text (str): Text/description of the task.
            Date (str): Due date of the task
        Returns:
            Response from the server
        """
        url = urljoin(self.base_url, "api/v1/items")
        data = '{ "Text": "%s", "Date": "%s" }' % (Text, Date)

        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'connect.sid=' + cookie
        }
        response = requests.request("POST", url, headers=headers, data=data)
        return response

    def read_all_tasks(self, cookie):
        """ Read all tasks
        Parameters:
            cookie (str): Pre-authorized cookie
        Returns:
            Response from the server
        """

        url = urljoin(self.base_url, "/api/v1/items")
        
        headers = {
            'Cookie': 'connect.sid=' + cookie
        }

        response = requests.request("GET", url, headers=headers)

        return response

    def read_task(self, cookie, task_id):
        """ Read a specific task
        Parameter:
            cookie (str): Pre-authorized cookie
            task_id (str): Specified task id
        Returns:
            Response from the server
        """

        url = urljoin(self.base_url, "/api/v1/items/" + task_id)
        
        headers = {
            'Cookie': 'connect.sid=' + cookie
        }

        response = requests.request("GET", url, headers=headers)

        return response

    def update_task(self, cookie, task_id, Done):
        """ Updates a task
        Parameter:
            cookie (str): Pre-authorized cookie
            task_id (str): Specidied task id
            Done (Boolean): Stated true or false
        Returns:
            Response from the server
        """

        url = urljoin(self.base_url, "/api/v1/items/" + task_id)
        payload = '{ "task_id": "%s", "Done": "%i" }' % (task_id, Done)
        #payload = f'{"task_id\": {task_id}, \"Done\": {Done}}' 

        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'connect.sid=' + cookie
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        return response

    def delete_task(self, cookie, task_id):
        """ Deletes task
        Parameters:
            cookie (str): Pre-authorized cookie
            task_id (str): Specidied task id
        Returns:
            Response from the server
        """

        url = urljoin(self.base_url, "/api/v1/items/" + task_id)
        payload = '{ "task_id": "%s"}' % (task_id)
        #payload = f'{"task_id\": {task_id}}'

        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'connect.sid=' + cookie
        }

        response = requests.request("DELETE", url, headers=headers, data = payload)

        return response

    def read_current_user(self, cookie):
        """ Reads current user
        Parameters:
            cookie (str): Pre-authorzied cookie
        Returns:
            Response from the server
        """

        url = urljoin(self.base_url, "/api/v1/user")
        
        headers = {
            'Cookie': 'connect.sid=' + cookie
        }

        response = requests.request("GET", url, headers=headers)

        return response

if __name__ == "__main__":
    base_url = "http://localhost:1337"
    cookie = "s%3A8wXkaBZxzy6jz8UrFN2l8Be5jEI75LNB.Wq4%2FzOMfo3Ioab8XQu2jbzyAxDVkVbmK9Qh4rdjCGa8"
    api = API(base_url)
    response = api.create_task(cookie, "Test the API", "2020-02-20")
    print(response.ok) # true if status code is 200-299 or 300-399
    print(response.status_code) # i.e. 201, 401, 500 (internal server)
    print(response.text) # unauthorized 
    print(response.json()) # only works if text is of the form '{"key": "values"}'