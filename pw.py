from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://en.abiyefon.com/sale/evening-dresses")
    page.get_by_role("link", name="View Next 51 Products").click()
    page.goto("https://en.abiyefon.com/long-green-mermaid-prom-dress-abu2744")
    page.locator("span").filter(has_text=re.compile(r"^37\.00$")).dblclick()
    page.get_by_role("deletion").filter(has_text="87.00").dblclick()
    page.locator("#product-options").get_by_text("44").click()
    page.locator("#product-options").get_by_text("42").click()
    page.locator("#product-options").get_by_text("40").click()
    page.locator("#product-options").get_by_text("38").click()
    page.locator("#product-options").get_by_text("36").click()
    page.get_by_text("3638404244").click()
    page.get_by_text("Revealing: Off Shoulder, Slit Fabric: Lycra Sleeve Type: Sleeveless Brassiere Li").click()
    page.get_by_text("Revealing: Off Shoulder, Slit Fabric: Lycra Sleeve Type: Sleeveless Brassiere Li").click()
    page.get_by_role("link", name="Long Emerald Green Satin Engagement Dress ABU3088 Long Emerald Green Satin Engagement Dress ABU3088 €129.00 €101.00 36 38 40 42").click()
    page.locator("html").click()
    page.get_by_role("link", name="Long Emerald Green Velvet Evening Dress ABU2605 Long Emerald Green Velvet Evening Dress ABU2605 €73.00 €58.00 36 38 40 42").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
