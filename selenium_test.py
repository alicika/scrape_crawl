from selenium.webdriver import Firefox, FirefoxOptions, Remote
from selenium.webdriver.common.keys import Keys

options = FirefoxOptions()
options.headless = True
driver = Firefox(options=options)
# when runs on remote env, uncomment:
# driver = Remote("http://10.0.2.2:4444", options=options)

driver.get("https:/google.co.jp")
assert "Google" in driver.title

input_element = driver.find_element_by_name("q")
input_element.clear()
input_element.send_keys("whatever")
input_element.send_keys(Keys.RETURN)

driver.save_screenshot("search_result.png")

for h3 in driver.find_element_by_css_selector("a > h3"):
    a = h3.find_element_by_xpath("..")
    print(h3.text)
    print(a.get_attribute("href"))

driver.quit()