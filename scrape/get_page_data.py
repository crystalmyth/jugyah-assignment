from core.config import config
from bs4 import BeautifulSoup
import json
import random
from model.page_data import PageData
from core.logger_setting import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.partial_request import get_req


def get_page_data(page_url: str) -> PageData | None:
    logger.info(page_url)
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        user_agent = random.choice(config.user_agents)
        chrome_options.add_argument(f"user-agent={user_agent}")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f"{config.domain_url}{page_url}")
        
        initial_state_script = "return window.__INITIAL_STATE__;"
        initial_state_json = driver.execute_script(initial_state_script)
        
        driver.quit()    
        
        headers = {'User-Agent': user_agent}
        response = get_req(url=f"{config.domain_url}{page_url}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Get title
            title = soup.find("h1").get_text()
            
            # Get Cost
            # cost = soup.find("span", {"class": "rupee-icon"}).parent.get_text() if soup.find("span", {"class": "rupee-icon"}).parent else None
            cost = []
            if initial_state_json["propertyDetails"]["details"]["details"]["config"]["propertyConfig"]:
                for item in initial_state_json["propertyDetails"]["details"]["details"]["config"]["propertyConfig"]:
                    cost.append({
                        "label": item["label"],
                        "range": item["range"],
                    })      
            
            # Get Launch date and BHK units
            launch_date = ''
            bhk_units = ''
            overview = soup.find("div", {"data-q": "more-about-project"})
            if overview:
                for td in overview.find_all("td"):
                    if "launch date" in td.get_text().lower():
                        launch_date = td.find_all("div")[1].get_text()
                    
                    if "configuration" in td.get_text().lower():
                        bhk_units = td.find_all("div")[1].get_text()
            
            # Get description
            about_section = soup.find("section", {"id": "aboutProject"})
            description = ''
            if about_section:
                description = about_section.find("div", {"data-q": "desc"}).get_text()
            
            
            # Get Aminities
            amenities = []
            amenities_section = soup.find("section", {"id": "amenities"})
            if amenities_section:
                amenities_container = amenities_section.find("div", {"class": "item-container"})

                if amenities_container and amenities_container.children:
                    for amenity in amenities_container.children:
                        if "less" not in amenity.get_text().lower():
                            amenities.append(amenity.get_text())
            
            
            # Get Locality
            locality = {
                "content": '',
                "know_more": '',
            }
            locality_section = soup.find("section", {"id": "locality"})
            if locality_section:
                if locality_section.find("div", {"data-q": "desc"}).find_all("span"):
                    locality_content = locality_section.find("div", {"data-q": "desc"}).find_all("span")[1].get_text()
                know_more_locality = locality_section.find("a").get("href") if locality_section.find("a") else None
                locality = {
                    "content": locality_content,
                    "know_more": know_more_locality,
                }
            
            # Get Geo Location
            latitude = ''
            longitude = ''
            
            if soup.find_all("script", {"type": "application/ld+json"}):
                for script in soup.find_all("script", {"type": "application/ld+json"}):
                    script_json = json.loads(script.string)
                    if len(script_json) and isinstance(script_json, list):
                        latitude = script_json[0]['geo']['latitude']
                        longitude = script_json[0]['geo']['longitude']
            
            # Sellers Details
            seller_details = []
            if initial_state_json['propertyDetails']['details']['sellers']:
                for seller in initial_state_json['propertyDetails']['details']['sellers']:
                    seller_details.append({
                        "name": seller['name'],
                        "designation": seller['designation'],
                        "phone": seller['phone']['partialValue']
                    })

            page_data =  PageData(
                title=title,
                bhk_units=bhk_units,
                launch_date=launch_date,
                cost=cost,
                description=description,
                amenities=amenities,
                locality=locality,
                geo_location={
                    "latitude": latitude,
                    "longitude": longitude
                },
                seller_details=seller_details,
                page_url=page_url
            )
            
            # logger.info(f"{ page_data = }")
            return page_data
        else:
            logger.error(f"{response.status_code = }")
            return None
    
    except Exception as e:
        logger.error(e)