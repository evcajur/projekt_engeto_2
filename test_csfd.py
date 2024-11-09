import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = False)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

def test_title(page):
    page.goto("https://www.csfd.cz/")
    assert page.title() == "ČSFD.cz", "The page title does not match the expected title"

@pytest.mark.parametrize("movie", ["Joker", "Star Wars", "Pán prstenů"])
def test_search_movie(page, movie):
    page.goto("https://www.csfd.cz/")
    search = page.locator("#main-search-form input[name='q']")
    search.fill(movie)
    search.press("Enter")
    page.wait_for_load_state("networkidle", timeout=60000)
    first_result =  page.locator(".film-title-nooverflow").first
    assert first_result.is_visible(), f"The first result for movie '{movie}' is not visible on the page"
    assert movie in first_result.inner_text(), f"The first result does not match the searched movie {movie}"

def test_televize_page_navigation(page):
    page.goto("https://www.csfd.cz/")
    page.locator("nav ul.tab-nav-list li.tab-nav-item a[href='/televize/']").click()
    page.wait_for_load_state("networkidle", timeout=60000)
    assert "/televize/" in page.url, "Navigation to the 'televize' page has failed"