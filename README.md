# API TESTER

## API.PI
        This api python code runs the same CRUD operation that is run in javascript, or even in Node.js code. 
    The reason it is created in this python code, is to be able to test it and to also test my api that it is all 
    set up correctly and can be able to test if there is any errors with how the code is running.
    The api is connected to the database so that it can be able to create tasks, read all the tasks, read only, update, 
    or even delete tasks. This runs a Create, Read, Update, and Delete (CRUD) operation which will update the datbase it 
    is connected to. This code is also connected to the website, so as it updates the database, it can update the user's 
    website so they can be able to have those changes on an front-end app.
### How to Test
    * At the bottom there is base_url. In there you need to put the site address, like your localhost or even server 
    address that can connect to your website and database. 
    * Under it, there is a cookie spot. When you open your front-end site, sign in and right click, then click inspect. 
    You will get a side window, click on application. You will need to get the cookie session that was created when you 
    signed in to your site. Some people it may be like todo-session, others may be connect.sid. Copy and paste the id and 
    paste into the cookie on your python code.
    * To be able to test each of the different apis, need to change the response code at the bootom. Keep api. 
    but change the rest to what ever api you are wanting to test. 
    * The print statements will run and make sure each of the codes are code properly and connected to the database 
    properly. The first two prints will print true or a 200 error if the code worked properly. The last two will 
    print out the task that was created, read, updated, or will delete the task and print the other tasks.

## TEST_API.PI
    The test python code is the testing portion of the python code. It is to test that the code in the api are implemented
    properly 