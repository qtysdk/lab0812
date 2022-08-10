import os

from requests_implementation import fetch

if __name__ == '__main__':
    count = 0
    data = [x.strip() for x in os.environ.get('data', '').split('\n') if x.strip()]
    print("len of data", len(data))
    for x in data:
        username = x.strip()
        cached, content = fetch(username)
        if cached:
            continue
        count += 1

        # stop the runner
        if count >= 3:
            break
