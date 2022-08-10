from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.select import Select


def create_driver():
    from selenium import webdriver
    from selenium.webdriver import ChromeOptions
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager

    # pip install webdriver-manager to get the ChromeDriverManager
    service = ChromeService(ChromeDriverManager().install())
    options = ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def login(driver: WebDriver):
    # implementation login here
    return driver


def search(driver: WebDriver, user: str):
    data = {'Username': None, 'Name': None, 'Name of Record': None, 'Email': None,
            'Office Phone': None, 'Office Fax': None, 'Office Location': None, 'Job Title': None,
            'Department Name': None, 'Campus Affiliation': None, 'Home Page': None}
    dropdown = Select(driver.find_element(By.CSS_SELECTOR, "#mykey"))  # locate the place of "username"
    dropdown.select_by_visible_text("username")
    element = driver.find_element(By.CSS_SELECTOR, "#query")  # Locate the place to enter username

    # The keyword is "send_keys" (ref: https://www.geeksforgeeks.org/send_keys-element-method-selenium-python/)
    element.send_keys(user)  # enter the username
    search_button = driver.find_element(By.XPATH,
                                        '//*[@id="searchFormDiv"]/form/strong/span[6]/input[2]')  # locate the place of "search button" with selenium
    search_button.click()

    # print(driver.page_source)

    # WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '#btn_Search1')))
    # html_content = driver.page_source # use beautifulsoup
    data['Username'] = user

    # find out all the rows of the table in each username webpage
    rows = driver.find_elements(By.XPATH, '//*[@id="searchFormDiv"]/div/table/tbody/tr')

    # create 2 lists: keys and values.
    keys = []
    values = []
    for i in range(1, len(rows) + 1):
        if driver.find_element(By.XPATH,
                               f'//*[@id="searchFormDiv"]/div/table/tbody/tr[{i}]/td[2]').text != "Details Not Available.":
            key = driver.find_element(By.XPATH, f'//*[@id="searchFormDiv"]/div/table/tbody/tr[{i}]/td[1]/b').text
            value = driver.find_element(By.XPATH, f'//*[@id="searchFormDiv"]/div/table/tbody/tr[{i}]/td[2]').text
            keys.append(key)
            values.append(value)
        else:
            continue

    # insert keys and values into the data dictionary.
    for j in range(len(keys)):
        data[keys[j]] = values[j]
    return data


def main():
    driver = create_driver()
    login(driver)

    driver.get('https://www.hawaii.edu/directory/index.php')
    username = 'yz6'

    username = 'chismar'

    # loop the users into search function
    data = search(driver, username)
    print(data)

    # time.sleep(15)
    driver.close()


if __name__ == '__main__':
    main()
