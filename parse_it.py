import os
from collections import OrderedDict

from bs4 import BeautifulSoup


def main():
    count = 0
    for x in os.listdir('storage'):
        if count > 25:
            break
        count += 1

        with open(f'storage/{x}') as fh:
            c = fh.read()
            soup = BeautifulSoup(c, 'html5lib')
            result = soup.select('.groupResultRecord')

            output = OrderedDict()
            output['Name'] = None
            output['Found'] = None
            output['Details_Not_Available'] = None

            print(x, len(result), len(soup.select('#searchFormDiv > form > h2 > b')))

            if len(soup.select('#searchFormDiv > form > h2 > b')) == 1:
                output['Found'] = False
                username = soup.select('#searchFormDiv > form > h2 > b')[0].text
                username = username.replace("\"", "").strip()
                output['Name'] = username

            if len(result) == 1:
                output['Found'] = True

                for row in result[0].select('tr'):
                    if len(row.select('td')) != 2:
                        raise ValueError('Found more than 2 columns')

                    field, value = row.select('td')
                    output[field.text] = value.text

                    # edge case for email
                    if field.text == 'Email':
                        output[field.text] = ", ".join([x.text for x in value.contents if x.text])

                    if field.text == 'Office Phone':
                        pass

                    if value.text == 'Details Not Available.':
                        output['Details_Not_Available'] = True
                        del output[field.text]
                    # print(field.text)
                    # print(value.text)

                print(output)

            # break

            # return output


if __name__ == '__main__':
    main()
