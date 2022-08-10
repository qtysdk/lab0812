import os

from requests_implementation import fetch

if __name__ == '__main__':
    skip_count = 0
    count = 0
    data = [x.strip() for x in os.environ.get('data', '').split('\n') if x.strip()]
    print("len of data", len(data))
    for x in data:
        username = x.strip()
        cached, content = fetch(username)
        if cached:
            skip_count += 1
            continue
        count += 1

        # stop the runner
        if count >= 6:
            break

    print("skip", skip_count)
