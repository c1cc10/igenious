# -*- coding: utf-8 -*-
import urllib3 as url
import json

def connect(amount, src_currency,dest_currency,reference_date):
    url_to = "http://127.0.0.1:8888/convert?amount=%s&src_currency=%s&dest_currency=%s&reference_date=%s" % (amount, src_currency,dest_currency,reference_date)
    try:
        r = http.request("GET", url_to)
    except url.exceptions.NewConnectionError:
        print("Can't Connect. Exiting ...")
        exit
    else:
        return r

if __name__ == "__main__":
    http = url.PoolManager()
    result = ""
    print("Test 1 Starting: regular change")
    r = connect("23","EUR","USD", "2018-10-26")
    #check_test(r)
    if r.status == 200:
        result = json.loads(r.data.decode('utf-8'))
        if result['amount'] == 26.093500000000002 and result['currency'] == "USD":
            print("Test one Passed")
        else:
            print("Test one Failed")
    else:
        print("Test one Failed")
    print(result)
    print("Test 2 Starting: negative amount value")
    r = connect("-23","EUR","USD", "2018-10-26")
    if r.status == 200:
        print("Test two Failed")
    else:
        print("Test two Passed")
    print("Test 3 Starting: non existent src currency")
    r = connect("23","TFG","USD", "2018-10-26")
    if r.status == 200:
        print("Test three Failed")
    else:
        print("Test three Passed")
    print("Test 4 Starting: non existent dest currency")
    r = connect("23","EUR","TFG", "2018-10-26")
    if r.status == 200:
        print("Test four Failed")
    else:
        print("Test four Passed")
    print("Test 5 Starting: non existent date")
    r = connect("23","EUR","USD", "2015-10-26")
    if r.status == 200:
        print("Test five Failed")
    else:
        print("Test five Passed")

