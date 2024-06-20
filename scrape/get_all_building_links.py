from core.config import config
from scrape.get_page_urls import get_page_urls

def get_all_building_links() -> list:
    page_no = 0
    building_page_links = []
    
    
    while len(building_page_links) <= 100:
        project_page_url = config.project_page_url
        building_page_links.extend(get_page_urls(page_no, project_page_url))
        page_no += 1

    
    # with open("links.txt", "w") as f:
    #     for link in building_page_links:
    #         f.write(f"{link}\n")
            
    return building_page_links