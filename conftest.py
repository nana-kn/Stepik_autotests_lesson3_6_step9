import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


supported_browsers = {
    'chrome': webdriver.Chrome,
    'firefox': webdriver.Firefox
}


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default='en-gb',
                     help="Interface language: Russian or English")


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    language_name = request.config.getoption("language")

    if browser_name in supported_browsers:
        browser = supported_browsers.get(browser_name)()
        print(f"\nstart {browser_name} browser for test..")
        if browser_name == 'chrome':
            print('\n\nChrome browser')
        
            options = Options()
            options.add_experimental_option('prefs', {'intl.accept_languages': language_name})
            browser = webdriver.Chrome(options=options)
        elif browser_name == 'firefox':
            print('\n\nFirefox browser')
        
            fp = webdriver.FirefoxProfile()
            fp.set_preference("intl.accept_languages", language_name)
            browser = webdriver.Firefox(firefox_profile=fp)
        else: print("Browser is not implemented")      
    else:
        joined_browsers = ', '.join(supported_browsers.keys())
        raise pytest.UsageError(f"--browser_name is invalid, supported browsers: {joined_browsers}")

    yield browser
    print("\nquit browser..")
    browser.quit()
    
    



