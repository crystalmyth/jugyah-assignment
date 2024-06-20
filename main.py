from core.config import config
from scrape.get_all_building_links import get_all_building_links
from scrape.get_page_data import get_page_data
import pandas as pd


def main() -> None:
    df = pd.DataFrame(columns=['title', 'bhk_units', 'launch_date', 'cost', 'description', 'amenities', 'locality', 'geo_location', 'seller_details', 'page_url'])
    links = get_all_building_links()
    
    for link in links:
        page_data = get_page_data(link)
        if page_data:
            df.loc[len(df)] = vars(page_data)
            
    
    df.to_csv('page_data.csv', index=False)
    
    
        
    
    


if __name__ == "__main__":
    main()