


from selenium import webdriver

browser = webdriver.Chrome('./bin/chromedriver')
browser.get('http://localhost:8000')

assert 'worked' in browser.title

browser.quit()
