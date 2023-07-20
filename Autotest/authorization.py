from playwright.sync_api import sync_playwright
import data
import pyperclip
import json

email = data.email()
password = data.password()
with sync_playwright() as p:
    # launch browser
    browser = p.chromium.launch(headless=False)
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
    # copy apikey
    page.get_by_test_id("apikeyButton").click()
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Copy", exact=True).click()
    apikey = pyperclip.paste()
    print(apikey)
    # send request
    context = browser.new_context(base_url="https://btc.getblock.io")
    api_request_context = context.request
    page = context.new_page()
    to_send = """
          {
            "jsonrpc": "2.0",
            "id": "healthcheck",
            "method": "getmininginfo",
            "params": []
            }
        """
    response = api_request_context.post(
        "/mainnet/",
        headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "x-api-key": apikey
        },
        data=to_send,
    )
    try:
        print(response)
        data = json.loads(response)
    except:
        # Still might fail sometimes
        data = None
    print(data)
    browser.close()
