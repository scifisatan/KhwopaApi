import requests
from bs4 import BeautifulSoup

# Named constants
BASE_URL = "https://www.khwopa.edu.np/mis.php"
LOGIN_URL = f"{BASE_URL}/site/login"
PAGE_URLS = {
    "internalMarks": f"{BASE_URL}/myrecord/intmark",
    "firstAssessment": f"{BASE_URL}/myrecord/ut",
    "finalAssessment": f"{BASE_URL}/myrecord/assessment",
}

session = requests.Session()


def login(data):
    response = session.post(LOGIN_URL, data=data)
    return not response.content.__contains__(b"Incorrect")


def fetch_page(url):
    page = session.get(url)
    if page.status_code == 200:
        return BeautifulSoup(page.content, "html.parser")
    return None


def parse_page(html_block, semester):
    parsed_html = (
        html_block.find_all("div", class_="panel-body")[0]
        .find_all("div")[0]
        .find_all("div")[int(semester) - 1]
    )
    return parsed_html


def scrape_all_site(username, password, semester):
    data = {
        "LoginForm[username]": username,
        "LoginForm[password]": password,
        "LoginForm[rememberMe]": "0",
        "yt0": "Login",
    }

    if login(data):
        return "Login failed"

    parsed_data = {}
    for key, url in PAGE_URLS.items():
        page = fetch_page(url)
        if not page:
            return f"Failed to fetch {key} page"
        parsed_data[key] = parse_page(page, semester)

    return parsed_data

def scrape_one_site(username, password, semester,exam):
    data = {
        "LoginForm[username]": username,
        "LoginForm[password]": password,
        "LoginForm[rememberMe]": "0",
        "yt0": "Login",
    }

    if not login(data):
        return "Login failed"

    parsed_data = {}
    url = PAGE_URLS[exam]
    page = fetch_page(url)
    parsed_data = parse_page(page, semester)

    return parsed_data

def scrape_dueAmount(username, password):
    data = {
        "LoginForm[username]": username,
        "LoginForm[password]": password,
        "LoginForm[rememberMe]": "0",
        "yt0": "Login",
    }

    if not login(data):
        return "Login failed"
    
    parsed_data = {}
    url = f"{BASE_URL}/myrecord/due"
    page = fetch_page(url)
    data = page.findAll('td')[1].text[6:] #type:ignore #[6:] it removes NRs. 
    return {"Due Amount" : int(data[:len(data)-1])} # :len(Str)-1 it removes last \n character