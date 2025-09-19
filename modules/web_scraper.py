import requests
from bs4 import BeautifulSoup

def scrape_text_from_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Remove scripts/styles
            for script in soup(["script", "style", "noscript"]):
                script.extract()

            text = soup.get_text(separator="\n")
            clean_text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])

            return clean_text[:30000]  # Limit to 30,000 characters
        else:
            return f"Failed to fetch URL (status code: {response.status_code})"
    except Exception as e:
        return f"Error fetching or parsing the website: {str(e)}"
