#!/usr/bin/env python3
import random
import string
import unittest

from api import API


def generate_random_text(l=10):
    """ Helper to generate random text for creating new tasks.
    This is helpful and will ensure that when you run your tests,
    a new text string is created. It is also good for determining
    that two tasks are unique.
    Keyword arguments:
        l (int): How long the generated text should be (default 10)
    Returns:
        A randomly-generated string of length `l`
    """
    chars = string.hexdigits
    return "".join(random.choice(chars) for i in range(l)).lower()


def generate_random_date(year=None, month=None, date=None):
    """ Helper to generate random date for creating new tasks.
    This is helpful as another way of generating random tasks
    Keyword arguments:
        year: Specify a year (default None)
        month: Specify a month (default None)
        date: Specify a date (default None)
    Returns:
        A randomly-generated string representation of a date
    """
    if not year:
        year = str(random.randint(2000, 2025))
    if not month:
        month = str(random.randint(1, 12))
    if not date:
        date = str(random.randint(1, 28))
    return str(year) + "-" + str(month) + "-" + str(date)



class TestAPI(unittest.TestCase):

    # TODO: update these two values with your own.
    base_url = "http://localhost:1337"
    cookie = "s%3A8wXkaBZxzy6jz8UrFN2l8Be5jEI75LNB.Wq4%2FzOMfo3Ioab8XQu2jbzyAxDVkVbmK9Qh4rdjCGa8"

    # This will be ran once, when you start your tests.
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.api = API(self.base_url)

    def test_create_task(self):
        """ Tests creating a task is successful.
        This is an example test:
            - Create the task w/dummy data
            - Verify that the task was created
            - Delete the task we created
        You will be required to implement the other tests
        that are defined in BaseTestCase. They will be marked
        with @abc.abstractmethod.
        """
        Text = generate_random_text()
        Date = generate_random_date()

        response = self.api.create_task(self.cookie, Text, Date)
        self.assertTrue(response.ok, msg=f"The Create Task failed: {response.reason}.")
        # assumes 201
        task = response.json() 

        self.assertEqual(task["Text"], Text, msg="The task's Text did not match the expected Text.")
        self.assertEqual(task["Date"], Date, msg="The task's Date did not match the expected Date.")
        self.assertFalse(task["Done"], msg="The task's Done returned True, expected False.")

        # cleanup - we don't want to conflict with other tests
        # or have a test task in our database.
        self.api.delete_task(self.cookie, task["_id"])

    def test_read_one_task(self):
        #create task
        Text = generate_random_text()
        Date = generate_random_date()

        response = self.api.create_task(self.cookie, Text, Date)
        self.assertTrue(response.ok, msg=f"The Create Task failed: {response.reason}.")
        # assumes 201
        task = response.json() 
        #read one task
        response = self.api.read_task(self.cookie, task["_id"])
        self.assertTrue(response.ok, msg=f"The Read Task failed: {response.reason}.")
        # assumes 201
        taskId = response.json()

        self.assertEqual(task["_id"], taskId["_id"], msg="The task's id did not the match the expected id.")

        # cleanup - we don't want to conflict with other tests
        # or have a test task in our database.
        self.api.delete_task(self.cookie, task["_id"])

    def test_read_all_task(self):
        response = self.api.read_all_tasks(self.cookie)
        self.assertTrue(response.ok, msg=f"The Read all task failed: {response.reason}.")
        # assumes 201
        tasks = response.json() 

        response = self.api.read_current_user(self.cookie)
        self.assertTrue(response.ok, msg=f"The User Task failed: {response.reason}.")
        user = response.json()

        for task in tasks:
            
            self.assertEqual(task["UserId"], user["Id"], msg="The users are not the same for all tasks.")
            # check to make sure all tasks have the same userid

    def test_update_task(self):
        #create task
        Text = generate_random_text()
        Date = generate_random_date()
        Done = True

        response = self.api.create_task(self.cookie, Text, Date)
        self.assertTrue(response.ok, msg=f"The Create Task failed: {response.reason}.")
        # assumes 201
        task = response.json() 

        #update task
        response = self.api.update_task(self.cookie, task["_id"], Done)
        self.assertTrue(response.ok, msg=f"The Update Task failed: {response.reason}.")
        # assumes 201
        task = response.json() 

        self.assertTrue(task["Done"], msg="The task's Done returned False, expected True.")

        # cleanup - we don't want to conflict with other tests
        # or have a test task in our database.
        self.api.delete_task(self.cookie, task["_id"])
        


    def test_delete_task(self):
        #create a task
        Text = generate_random_text()
        Date = generate_random_date()

        response = self.api.create_task(self.cookie, Text, Date)
        self.assertTrue(response.ok, msg=f"The Create Task failed: {response.reason}.")
        # assumes 201 
        task = response.json()

        #delete task
        response = self.api.delete_task(self.cookie, task["_id"])
        self.assertTrue(response.ok, msg=f"The Delete Task failed: {response.reason}.")
        # assumes 201

        #read task
        response = self.api.read_task(self.cookie, task["_id"])
        self.assertFalse(response.ok, msg=f"The Read Task failed: {response.reason}.")
        # assumes 201 
        #task = response.json()


    def test_read_current_user(self):
        response = self.api.read_current_user(self.cookie)
        self.assertTrue(response.ok, msg=f"The User Task failed: {response.reason}.")
        # assumes 201
        user = response.json()

        self.assertIn("Id", user) # make sure has {"Id":"..."}
        self.assertIn("Email", user)
        self.assertNotIn("I'm not an Id", user)
    
    def test_read_one_not_exist(self):
        # make fake _id
        _id = generate_random_text(l=24)
        response = self.api.read_task(self.cookie, _id)
        self.assertFalse(response.ok, msg=f"The task is there.") # 404--not ok, not found

    def test_delete_not_exitst(self):
        _id = generate_random_text(l=24)
        response = self.api.delete_task(self.cookie, _id)
        self.assertFalse(response.ok, msg=f"The task id is there.")

    def test_update_not_exist(self):
        _id = generate_random_text(l=24)
        Done = True
        response = self.api.update_task(self.cookie, _id, Done)
        self.assertFalse(response.ok, msg=f"The task is there and updated.")

    def test_delete_invalid_id(self):
        _id = generate_random_text(l=12)
        response = self.api.delete_task(self.cookie, _id)
        self.assertFalse(response.ok, msg=f"The id is valid.")

    def test_read_all_not_exist(self):
        self.cookie = generate_random_text(l=24)
        response = self.api.read_all_tasks(self.cookie)
        self.assertFalse(response.ok, msg=f"Able to read all tasks")

    def test_create_no_info(self):
        Text = ""
        Date = "" 
        response = self.api.create_task(self.cookie, Text, Date)
        self.assertFalse(response.ok, msg=f"Created a task.")




# Inside this `if` statement will only run if we call the program as
# the top-level module, i.e. when we run this file, not when we import
# this file
if __name__ == "__main__":
    unittest.main()