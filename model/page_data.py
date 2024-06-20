from dataclasses import dataclass

@dataclass
class PageData:
    title: str
    bhk_units: str
    launch_date: str
    cost: list
    description: str
    amenities: list
    locality: dict
    geo_location: dict
    seller_details: list
    page_url: str