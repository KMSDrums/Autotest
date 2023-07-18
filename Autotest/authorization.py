from playwright.sync_api import sync_playwright
import data

email = data.email()
password = data.password()
with sync_playwright() as p:
    # launch browser
    browser = p.chromium.launch()
    page = browser.new_page()
    # go to site
    page.goto("https://account.getblock.io/sign-in-email")
    print(page.title())
    page.get_by_test_id("signInEmailButton").click()
    page.wait_for_timeout(1000)
    # enter data
    page.type("input[name='email']", email)
    page.wait_for_timeout(1000)
    page.type("input[name='password']", password)
    # login
    page.get_by_test_id("signInButton").click()
    page.wait_for_timeout(5000)
    # choice protocol and network
    page.get_by_test_id("protocolDropdown").click()
    page.query_selector("text=Bitcoin").click()
    page.get_by_test_id("networkDropdown").click()
    page.query_selector("text=Mainnet").click()
    page.get_by_test_id("createEndpointButton").click()
    page.wait_for_timeout(5000)
    # check response
    check_visibility = page.get_by_test_id("endpoint").is_visible()
    if check_visibility:
        print("Success")
    page.screenshot(path="screenshot.png", full_page=True)
    browser.close()
