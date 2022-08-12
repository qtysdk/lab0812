import datetime
import hashlib
import os
import re
import requests

# In this example, we don't put the Cookie
_REQUEST_EXAMPLE = r"""
curl 'https://www.hawaii.edu/directory/index.php' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'Accept-Language: en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6' \
  -H 'Cache-Control: max-age=0' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Origin: https://www.hawaii.edu' \
  -H 'Referer: https://www.hawaii.edu/directory/index.php' \
  -H 'Sec-Fetch-Dest: document' \
  -H 'Sec-Fetch-Mode: navigate' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-Fetch-User: ?1' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  --data-raw 'q=person&campus=all&qtype=person&mykey=uid&query=Lyman&search=++++Search++++' \
  --compressed
"""


def hash_value(s: str):
    m = hashlib.md5()
    m.update(s.encode())
    return m.hexdigest()


def curl_to_headers(curl_example: str) -> dict:
    header_lines = [x.strip() for x in curl_example.split('\n') if '-H ' in x]

    def to_key_value(header_line):
        # newline \ for unix-like
        v1 = re.findall(r'^-H .(.*). \\$', header_line)
        # newline ^ for windows
        v2 = re.findall(r'^-H .(.*). \^$', header_line)

        # find each header
        header = v1 if v1 else v2
        v = re.findall(r'(^[^:]+): (.+$)', header[0])
        if v:
            return v[0]
        return None

    result = dict()
    for line in header_lines:
        kv = to_key_value(line.strip())
        if kv:
            k, v = kv
            result[k] = v
    return result


def do_fetch(username: str):
    # use the Session to keep cookies
    with requests.Session() as s:
        # Get the index page to initial the cookie
        url = 'https://www.hawaii.edu/directory/index.php'
        response = s.get(url, timeout=30)
        print(response.status_code)
        print(response.cookies.items())

        # Search for username
        headers = curl_to_headers(_REQUEST_EXAMPLE)
        payload = f'q=person&campus=all&qtype=person&mykey=uid&query={username}&search=++++Search++++'
        r = s.post(url, headers=headers, data=payload, timeout=30)
        return r.text


def cache_path(username):
    storage_path = os.path.join(os.path.dirname(__file__), 'storage')
    os.makedirs(storage_path, exist_ok=True)
    filename = os.path.join(storage_path, f"{hash_value(username)}.html")
    return filename


def fetch(username: str):
    filename = cache_path(username)
    if os.path.exists(filename):
        with open(filename) as fh:
            return True, fh.read()

    content = do_fetch(username)
    with open(filename, "w") as fh:
        fh.write(content)
    return False, content


if __name__ == '__main__':
    username = 'yz6'
    # cached, content = fetch(username)
    print(hash_value(username))
