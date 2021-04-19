# 2020_S2_COMP7802
2020_S2_COMP7802

Usage:
1. cd path into the crawler folder
2. Run SQLi_4.py with the 4 options of operations
    -f: run full automatic pen-test with crawler (example: py SQLi_4.py -f)
	-s: run automatic pen-test on a single page" (example: py SQLi_4.py -u "http://localhost/dashboard/var/www/sqli-labs-master/Less-1/")
	-i: run half-auto pen-test with the file of the intercepted response to inject (example: py SQLi_4.py -i post.txt)
	-u: run basic pen-test on a specific GET method URL (example: py SQLi_4.py -u "http://localhost/dashboard/var/www/sqli-labs-master/Less-1/?id=1&name=admin")
	-h: print the help document (example: py SQLi_4.py -h)