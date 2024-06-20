import requests
from bs4 import BeautifulSoup
from core.config import config
from utils.partial_request import get_req
from core.logger_setting import logger


def get_page_urls(page_no: int, project_page_url: str) -> list:
    try:
        page_url = f"{config.domain_url}{project_page_url}"
        if page_no:
            response = get_req(f"{page_url}?page={page_no}")
        else:
            response = get_req(page_url)
        
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            building_articles = soup.find_all("article")
            
            if len(building_articles):
                page_links = [article.find("a").get("href") for article in building_articles]
                return page_links
            else:
                print("No data found")
                return []
        else:
            print(f"Error: {response.status_code}")
            return []
    except Exception as e:
        logger.error(e)