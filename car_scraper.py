import cloudscraper
from bs4 import BeautifulSoup
import time
import random
import re
import csv


scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
)


def clean_text(text):
    """Remove extra whitespace and clean text"""
    if text:
        return re.sub(r'\s+', ' ', text.strip())
    return None


def scrape_first_reg(soup):
    """Scrape Esmane reg (First registration) - extract only year"""
    try:
        row = soup.find('tr', class_='field-month_and_year')
        if row:
            value = row.find('td', class_='field').find('span', class_='value')
            if value:
                text = clean_text(value.text)
                # Extract year from formats like "07/2006" or "01/2008"
                if '/' in text:
                    # Split by '/' and get the year part (after the slash)
                    year = text.split('/')[-1]
                    return year
                # If format is different, try to extract 4-digit year
                elif text and len(text) >= 4:
                    # Look for 4 consecutive digits
                    import re
                    year_match = re.search(r'\d{4}', text)
                    if year_match:
                        return year_match.group()
                return text  # Return as-is if format is unexpected
    except Exception as e:
        print(f"Error scraping Esmane reg: {e}")
    return None


def scrape_type(soup):
    """Scrape Liik (Type)"""
    try:
        row = soup.find('tr', class_='field-liik')
        if row:
            value = row.find('td', class_='field').find('span', class_='value')
            return clean_text(value.text) if value else None
    except Exception as e:
        print(f"Error scraping Liik: {e}")
    return None


def scrape_body_type(soup):
    """Scrape Keretüüp (Body type)"""
    try:
        row = soup.find('tr', class_='field-keretyyp')
        if row:
            value = row.find('td', class_='field').find('span', class_='value')
            return clean_text(value.text) if value else None
    except Exception as e:
        print(f"Error scraping Keretüüp: {e}")
    return None


def scrape_engine(soup):
    """Scrape Mootor (Engine) - return entire field as-is"""
    try:
        row = soup.find('tr', class_='field-mootorvoimsus')
        if row:
            value = row.find('td', class_='field').find('span', class_='value')
            if value:
                return clean_text(value.text)
    except Exception as e:
        print(f"Error scraping Mootor: {e}")
    return None


def scrape_fuel(soup):
    """Scrape Kütus (Fuel)"""
    try:
        row = soup.find('tr', class_='field-kytus')
        if row:
            value = row.find('td', class_='field').find('span', class_='value')
            return clean_text(value.text) if value else None
    except Exception as e:
        print(f"Error scraping Kütus: {e}")
    return None


def scrape_mileage(soup):
    """Scrape Läbisõidumõõdiku näit (Mileage) - extract only number"""
    try:
        row = soup.find('tr', class_='field-labisoit')
        if row:
            value = row.find('td', class_='field').find('span', class_='value')
            if value:
                text = clean_text(value.text)
                # Remove 'km' and spaces, keep only numbers
                mileage = text.replace('km', '').replace(' ', '').replace('\xa0', '').strip()
                return mileage
    except Exception as e:
        print(f"Error scraping Läbisõidumõõdiku näit: {e}")
    return None


def scrape_drive_type(soup):
    """Scrape Vedav sild (Drive type)"""
    try:
        row = soup.find('tr', class_='field-vedavsild')
        if row:
            value = row.find('td', class_='field').find('span', class_='value')
            return clean_text(value.text) if value else None
    except Exception as e:
        print(f"Error scraping Vedav sild: {e}")
    return None


def scrape_gearbox(soup):
    """Scrape Käigukast (Gearbox)"""
    try:
        row = soup.find('tr', class_='field-kaigukast_kaikudega')
        if row:
            value = row.find('td', class_='field').find('span', class_='value')
            return clean_text(value.text) if value else None
    except Exception as e:
        print(f"Error scraping Käigukast: {e}")
    return None


def scrape_color(soup):
    """Scrape Värvus (Color)"""
    try:
        row = soup.find('tr', class_='field-varvus')
        if row:
            value = row.find('td', class_='field').find('span', class_='value')
            return clean_text(value.text) if value else None
    except Exception as e:
        print(f"Error scraping Värvus: {e}")
    return None


def scrape_brand_model(soup):
    """Scrape car brand and model from vHistoryReport section"""
    try:
        # Find the vHistoryReport section
        history_report = soup.find('div', class_='vHistoryReport__vehicle')
        if history_report:
            # Find the make (brand)
            make_span = history_report.find('span', class_='-make')
            brand = clean_text(make_span.text) if make_span else None

            return brand
            # # Extract model from brand string
            # # The text is typically "Brand Model" (e.g., "Mazda 6" or "Ford Mondeo Turnier Facelift ATM")
            # if brand and ' ' in brand:
            #     parts = brand.split(' ', 1)  # Split into max 2 parts
            #     brand_name = parts[0]  # First part is the brand (e.g., "Ford", "Mazda")
            #
            #     if len(parts) > 1:
            #         model_full = parts[1]  # Everything after brand (e.g., "Mondeo Turnier Facelift ATM", "6")
            #         # Extract only the first word of the model
            #         model = model_full.split()[0] if model_full else None
            #         return brand_name, model  # Return (brand, first_word_of_model)
            #
            #     return brand_name, None
            #
            # return brand, None
    except Exception as e:
        print(f"Error scraping brand and model: {e}")
    return None, None


def scrape_price(soup):
    """Scrape price - returns discount price if available, otherwise regular price"""
    try:
        # First, check if there's a discount price
        discount_row = soup.find('tr', class_='field-soodushind')
        if discount_row:
            value_span = discount_row.find('span', class_='value')
            if value_span:
                price_text = clean_text(value_span.text)
                # Remove EUR and whitespace, keep only numbers
                price = price_text.replace('EUR', '').replace('\xa0', '').replace(' ', '').strip()
                return price

        # If no discount price, get regular price
        price_row = soup.find('tr', class_='field-hind')
        if price_row:
            value_span = price_row.find('span', class_='value')
            if value_span:
                price_text = clean_text(value_span.text)
                # Remove EUR and whitespace, keep only numbers
                price = price_text.replace('EUR', '').replace('\xa0', '').replace(' ', '').strip()
                return price
    except Exception as e:
        print(f"Error scraping price: {e}")
    return None

def scrape_car_details(url):
    """Scrape details from individual car page"""
    try:
        response = scraper.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        print(f"\n=== Scraping: {url} ===")
        brand = scrape_brand_model(soup)

        # Scrape all fields
        car_data = {
            'url': url,
            'brand': brand,
            'first_reg': scrape_first_reg(soup),
            'type': scrape_type(soup),
            'body_type': scrape_body_type(soup),
            'engine': scrape_engine(soup),
            'fuel': scrape_fuel(soup),
            'mileage': scrape_mileage(soup),
            'drive_type': scrape_drive_type(soup),
            'gearbox': scrape_gearbox(soup),
            'color': scrape_color(soup),
            'price': scrape_price(soup)
        }

        # Print scraped data
        for key, value in car_data.items():
            if key != 'url':
                print(f"{key}: {value}")

        return car_data
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


def get_car_links(listing_url):
    """Extract all car listing links from the search results page"""
    try:
        response = scraper.get(listing_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all car listing links
        car_links = []
        title_divs = soup.find_all('div', class_='title')

        for div in title_divs:
            link = div.find('a', class_='main')
            if link and link.get('href'):
                href = link['href']
                # Construct full URL
                full_url = f"https://www.auto24.ee{href}"
                car_links.append(full_url)

        return car_links
    except Exception as e:
        print(f"Error getting car links: {e}")
        return []


def save_to_csv(data, filename=None, mode='w'):
    """
    Save scraped data to CSV file

    Args:
        data: List of car data dictionaries
        filename: CSV filename
        mode: 'w' for write (new file), 'a' for append
    """
    if not data:
        print("No data to save!")
        return

    # Generate filename with timestamp if not provided
    if filename is None:
        filename = f'auto24_cars_v2.csv'

    # Define CSV columns - updated to use single 'engine' column
    fieldnames = ['url', 'brand', 'first_reg', 'type', 'body_type',
                  'engine', 'fuel', 'mileage', 'drive_type', 'gearbox',
                  'color', 'price']

    try:
        # Check if file exists when appending
        file_exists = False
        if mode == 'a':
            try:
                with open(filename, 'r'):
                    file_exists = True
            except FileNotFoundError:
                file_exists = False

        with open(filename, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header only if creating new file or file doesn't exist
            if mode == 'w' or not file_exists:
                writer.writeheader()

            # Write data rows
            for car in data:
                writer.writerow(car)

        if mode == 'w':
            print(f"\n✓ Data successfully saved to: {filename}")
        else:
            print(f"\n✓ Data successfully appended to: {filename}")
        print(f"✓ Records in this batch: {len(data)}")

    except Exception as e:
        print(f"Error saving to CSV: {e}")

    return filename


def main(base_url, max_pages=None, start_page=0):
    """
    Main function to scrape multiple pages

    Args:
        base_url: The initial URL (with ak=0 or without ak parameter)
        max_pages: Maximum number of pages to scrape (None = scrape until no results)
        :param start_page:
    """
    print(f"Starting scrape from: {base_url}")

    # Parse the base URL to extract parameters
    from urllib.parse import urlparse, parse_qs, urlencode

    parsed_url = urlparse(base_url)
    query_params = parse_qs(parsed_url.query)

    # Convert query params back to single values (parse_qs returns lists)
    query_dict = {k: v[0] for k, v in query_params.items()}

    # Start from ak=0 if not specified
    if 'ak' not in query_dict:
        query_dict['ak'] = '0'

    if start_page > 0:
        query_dict['ak'] = str(start_page * 100)

    page_num = 0
    csv_filename = None
    total_cars_scraped = 0

    while True:
        # Check if we've reached max_pages
        if max_pages is not None and page_num >= max_pages:
            print(f"\nReached maximum page limit ({max_pages})")
            break

        # Construct the URL for current page
        current_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{urlencode(query_dict)}"

        print(f"\n{'=' * 60}")
        print(f"PAGE {page_num + 1} - ak={query_dict['ak']}")
        print(f"{'=' * 60}")
        print(f"Fetching listings from: {current_url}")

        # Get all car links from the listing page
        car_links = get_car_links(current_url)

        if not car_links:
            print(f"\nNo car listings found on page {page_num + 1}. Stopping.")
            break

        print(f"\nFound {len(car_links)} car listings on this page")

        # Store data for current page
        page_car_data = []

        # Loop through each car listing
        for idx, car_url in enumerate(car_links, 1):
            print(f"\n[Page {page_num + 1} - {idx}/{len(car_links)}] Processing: {car_url}")
            car_data = scrape_car_details(car_url)

            if car_data:
                page_car_data.append(car_data)

            # Random delay between 2 to 10 seconds
            delay = random.uniform(1, 2.5)
            print(f"Waiting {delay:.1f} seconds before next request...")
            time.sleep(delay)

        # Save current page data to CSV
        if page_car_data:
            if page_num == 0:
                # First page - create new file
                csv_filename = save_to_csv(page_car_data, mode='w')
            else:
                # Subsequent pages - append to existing file
                save_to_csv(page_car_data, filename=csv_filename, mode='a')

            total_cars_scraped += len(page_car_data)
            print(f"✓ Total cars scraped so far: {total_cars_scraped}")

        # Increment ak by 100 for next page
        current_ak = int(query_dict['ak'])
        query_dict['ak'] = str(current_ak + 100)
        page_num += 1

        # Delay before fetching next page
        delay = random.uniform(3, 8)
        print(f"\nWaiting {delay:.1f} seconds before fetching next page...")
        time.sleep(delay)

    print(f"\n\n{'=' * 60}")
    print(f"SCRAPING COMPLETE")
    print(f"{'=' * 60}")
    print(f"Total pages scraped: {page_num}")
    print(f"Total cars scraped: {total_cars_scraped}")
    if csv_filename:
        print(f"Data saved to: {csv_filename}")

    return total_cars_scraped


if __name__ == "__main__":
    url = 'https://www.auto24.ee/kasutatud/nimekiri.php?bn=2&a=101102&ae=2&af=100&by=2&ssid=247797544&ak=0'

    # Option 1: Scrape all pages until no results (set max_pages=None)
    results = main(url, max_pages=None, start_page=0)

    # Option 2: Scrape only first 5 pages (uncomment below)
    # results = main(url, max_pages=5)