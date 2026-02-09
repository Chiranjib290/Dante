import requests
from bs4 import BeautifulSoup

def url_is_reachable(url, timeout=5):
    try:
        response = requests.get(url, allow_redirects=False, timeout=timeout)

        # If it's not HTTP 200, it's not reachable
        if response.status_code != 200:
            return False

        # Parse the HTML title
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else ""

        # If the title indicates a 404 page, treat as unreachable
        if title.lower() == "404":
            return False

        return True

    except Exception:
        return False


print(url_is_reachable("https://www.pwc.ie/digital-playbook/templates/archive/EXPIRE__accelerator-template-sample.html"))

