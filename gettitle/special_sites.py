def ptt_handler(browser):
    element = browser.find_element_by_xpath(
        "/html/body/div[2]/form/div[1]/button"
    )
    if element:
        element.click()
        title = browser.title
        real_url = browser.current_url
        return title, real_url
    else:
        raise RuntimeError("Cannot find element.")


URL_AND_HANDLER_MAPPING = {
    "www.ptt.cc/ask/over18": ptt_handler,
}
