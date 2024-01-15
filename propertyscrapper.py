import csv   
from typing import IO               
import requests
from bs4 import BeautifulSoup


def scrape(area: str, area_code: int, filepath:str) -> IO[str]:
    """
    Function to scrape Property24 data.

    Parameters:
    - area (str): The name of the suburb or area, found on the link after searching for a suburb on property24.com.
    - area_code (int): The area code is found on the link after searching for a suburb.
    - filename (str): filepath with filename to save the scarpped data. The filename should be csv. 

    Returns:
    A csv file with the scrapped data at the path specified.
    """
    count = 1  
    base_url = f"https://www.property24.com/for-sale/{area}/pretoria/gauteng/{area_code}"

    with open(filepath, mode='a', newline='',encoding= 'utf-8') as csv_file:
        variables = ['location','bedrooms','bathrooms','parking','size','price']
        writer = csv.DictWriter(csv_file, fieldnames=variables)

        if csv_file.tell()==0:
            writer.writeheader()
       
        while True:
            if count == 1:
                full_url = base_url
            else:
                full_url = f"{base_url}/p{count}"

            response = requests.get(full_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                tile_containers = soup.find_all('div', class_='p24_tileContainer')

                if not tile_containers:
                    break

                for tile in tile_containers:
                    p24_regular = tile.find('div', class_='p24_regularTile')

                    if p24_regular:
                        link = p24_regular.find("a")

                        if link:
                            p24_content = link.find('span', class_='p24_content')

                            if p24_content:
                                price = p24_content.find('span', class_='p24_price').text.strip()
                                location = p24_content.find('span', class_='p24_location').text.strip()

                                bedrooms = p24_content.find('span', {'class': 'p24_featureDetails', 'title': 'Bedrooms'})
                                bed = bedrooms.find('span').text.strip() if bedrooms else None

                                bathrooms = p24_content.find('span', {'class': 'p24_featureDetails', 'title': 'Bathrooms'})
                                bath = bathrooms.find('span').text.strip() if bathrooms else None

                                park = p24_content.find('span', {'class': 'p24_featureDetails', 'title': 'Parking Spaces'})
                                parking = park.find('span').text.strip() if park else None

                                p24_size = p24_content.find('span', class_='p24_size')
                                size = p24_size.find('span').text.strip() if p24_size else None

                                writer.writerow({'location':location, 
                                                 'bedrooms':bed,
                                                 'bathrooms':bath,
                                                 'parking':parking, 
                                                 'size':size,
                                                 'price':price})
                                
                                
                count += 1  


scrape('mooikloof-ridge',10834,'pretoria_east_property_data.csv')
scrape('mooikloof',10,'pretoria_east_property_data.csv')
scrape('the-wilds',10444,'pretoria_east_property_data.csv')
scrape('pretoriuspark',162,'pretoria_east_property_data.csv')
scrape('olympus-ah',12201,'pretoria_east_property_data.csv')