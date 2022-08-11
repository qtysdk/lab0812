import os
from collections import OrderedDict

from bs4 import BeautifulSoup
from pandas import DataFrame


def main():
    pass


def parse_file(file: str):
    # print(file)
    with open(file) as fh:
        html_content = fh.read()
        soup = BeautifulSoup(html_content, 'html5lib')
        result = soup.select('.groupResultRecord')
        not_found_message = soup.select("#searchFormDiv > form > h2")

        output = OrderedDict()
        output['Name'] = None
        output['Found'] = None
        output['Details Not Available'] = None

        if len(not_found_message) == 1:
            output['Name'] = not_found_message[0].select('b')[0].text.replace("\"", '').strip()
            output['Found'] = False
            # print(f'{username} not found')
            # print(username)
            # pass

        if len(result) == 1:
            output['Found'] = True
            for row in result[0].select('tr'):
                columns = row.select('td')
                if len(columns) != 2:
                    raise ValueError(f'found not paired columns => {result}')

                field, value = columns
                if len(list(value.children)) == 1:
                    if value.text != 'Details Not Available.':
                        output[field.text] = value.text
                    else:
                        output['Details Not Available'] = True
                else:
                    v = [x.text for x in value.children if x.text]
                    output[field.text] = ",".join(v)
            pass

        # print(file, len(soup.select('.groupResultRecord')), len(soup.select("#searchFormDiv > form > h2")))
        # print(file, output)
        return output


if __name__ == '__main__':

    data = []
    for file in os.listdir('storage'):
        if file.endswith(".html"):
            output = parse_file(os.path.join('storage', file))
            if output['Name'] is not None:
                data.append(output)

    headers = []
    for d in data:
        for h in d.keys():
            if h not in headers:
                headers.append(h)

    df = DataFrame(data, columns=headers)
    df = df.sort_values(by=['Name'])
    df.to_excel('data.xlsx', index=False)
