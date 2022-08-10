import os

from requests_implementation import fetch

if __name__ == '__main__':
    count = 0
    for x in os.environ.get('data', '').split('\n'):
        username = x.strip()
        cached, content = fetch(username)
        if cached:
            continue
        count += 1

        # stop the runner
        if count > 5:
            break
