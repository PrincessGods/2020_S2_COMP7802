# 2020_S2_COMP7802
2020_S2_COMP7802

System requirement:
1. Windows or Unix OS
2. Python version 3.8+

Installation:
1. For Windows users using Pycharm, firstly create a new project with Virtualenv as environment and Python version 3.8+ as interpreter
2. Copy all file into the project folder
3. Import all packages
4. For Unix users, just import all packages should work
5. For users would like to use the Splash dynamic content perload function, please visit this website https://splash.readthedocs.io/en/stable/install.html and config Splash correctly with Docker
6. For users would like to use localhost, please doulbe check the actual address of the localhost. For example, if Docker was installed, the actual localhost address should be "kubernetes.docker.internal" instead of 127.0.0.1

Usage:
1. cd path into the crawler folder
2. Run SQLi_Det.py with the 4 options of operations
    -f: run full automatic pen-test with crawler (example: py SQLi_Det.py -f)
	-s: run automatic pen-test on a single page" (example: py SQLi_Det.py -u "http://localhost/dashboard/var/www/sqli-labs-master/Less-1/")
	-i: run half-auto pen-test with the file of the intercepted response to inject (example: py SQLi_Det.py -i post.txt)
	-u: run basic pen-test on a specific GET method URL (example: py SQLi_Det.py -u "http://localhost/dashboard/var/www/sqli-labs-master/Less-1/?id=1&name=admin")
	-h: print the help document (example: py SQLi_Det.py -h)
3. If operation -i is chosen, you must place the intercepted request headers into the post.txt file within the temp folder

Test application:
The test application is PHP MVC based web application which can be launched in any PHP development environment. The database file has been provided in the folder.