from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os


def scrapping():
    url = 'https://www.avito.ru/all/mototsikly_i_mototehnika/mototsikly-ASgBAgICAUQ80k0?cd=1&f=ASgBAgICBEQ80k3wjQ~~mKQQ8o0P6JqkEPSND_KapBA'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(str(os.getcwd) + '/chromedriver')

    driver = webdriver.Chrome(service=service, options=options)
    items = {}
    counter = []

    try:
        print('Open browser')
        driver.get(url)
        driver.implicitly_wait(10)
        open_element = driver.find_elements(By.XPATH, "//div[@data-marker='item']")
        print('Reading content')
        print(f'Find: {len(open_element)} elements in page')

        for element in open_element:
            element.click()
            driver.implicitly_wait(5)
            driver.switch_to.window(driver.window_handles[1])
            url_item = driver.current_url
            driver.implicitly_wait(5)

            try:
                price = driver.find_element(By.XPATH,
                                            '//span[@class="js-item-price style-item-price-text-_w822 text-text-LurtD text-size-xxl-UPhmI"]')
            except Exception:
                price = None

            # description = driver.find_element(By.XPATH, '//div[@itemprop="description"]')
            # title = driver.find_element(By.XPATH, '//span[@class="title-info-title-text"]')
            address = driver.find_element(By.XPATH, '//span[@class="style-item-address__string-wt61A"]')
            date_income = driver.find_element(By.XPATH, '//span[@data-marker="item-view/item-date"]')
            desc1 = driver.find_element(By.XPATH, '//div[@data-marker="item-view/item-params"]')

            if not price:
                price = "Не указана"
            else:
                price = int((price.text).replace(' ', '')) // 75.22

            items['Price'] = price
            items['Url'] = url_item
            items['Published date'] = date_income.text
            items['Description'] = desc1.text
            items['Addess'] = address.text

            counter.append(items)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()
    return counter


if __name__ == '__main__':
    remarks = ['Prise', 'Url', ]
    items = scrapping()
    print(f'Discovered {len(items)} rows')
    for row in items:
        for key in row:
            print(f'{key} : {row[key]}')
        print('\n\n\n')
