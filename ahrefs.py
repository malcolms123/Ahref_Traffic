import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.common.action_chains import ActionChains

def human_type(element, text):
    """Type like a human with random delays between characters"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

def open_ahrefs():
    # Set up Chrome options
    options = uc.ChromeOptions()
    
    # Window size and position
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    
    # Add common browser features
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--enable-javascript')
    options.add_argument('--enable-cookies')
    
    # Initialize undetected Chrome driver
    driver = uc.Chrome(options=options)
    
    # Navigate to ahrefs login page
    driver.get('https://app.ahrefs.com/user/login')
    
    # Wait for user to log in manually and handle Cloudflare
    input("Press any key after logging in...")
    
    # Add a delay after login
    time.sleep(1)
    
    domains = pd.read_csv('sample_sheet.csv')['URL'].tolist()

    first = True
    for domain in domains:
        print(f"Processing {domain}")
        if first:
            driver.get(f'https://app.ahrefs.com/v2-site-explorer/overview?mode=subdomains&target={domain}')
            first = False
        else:
            # Find search input
            search_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((
                By.CSS_SELECTOR, 
                "input.css-j5i1cm-input[placeholder='Domain or URL']"
            ))
            )
        
            # Try multiple methods to clear the input
            # 1. Clear via JavaScript
            driver.execute_script("arguments[0].value = '';", search_input)
            time.sleep(0.5)
            
            # 2. Send backspace keys if there's still text
            current_value = search_input.get_attribute('value')
            if current_value:
                search_input.send_keys(len(current_value) * Keys.BACKSPACE)
                time.sleep(0.5)
            
            # Type like a human
            human_type(search_input, domain)
            
            # Random pause before hitting enter
            time.sleep(random.uniform(0.5, 1.5))
            search_input.send_keys(Keys.RETURN)
        
        try:
            # Look for the traffic value in the specific structure
            traffic_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((
                    By.XPATH, 
                    "//div[contains(@class, 'css-1iy025y-groupOrganicPaidSearchContent')]//div[.//div[contains(text(), 'Traffic')]]//a/span[contains(@class, 'css-1qasr9x')]"
                ))
            )
            
            # Get the traffic value as string
            traffic = traffic_element.text
            print(f"Organic traffic: {traffic}")
        except Exception as e:
            print(f"Error finding traffic element for {domain}")
            traffic = "Not Found"
        
        # Update the traffic value in the DataFrame - specify dtype as string
        domains_df = pd.read_csv('sample_sheet.csv', dtype={'Traffic': str})
        domains_df.loc[domains_df['URL'] == domain, 'Traffic'] = traffic
        domains_df.to_csv('sample_sheet.csv', index=False)

        # Random delay between requests
        time.sleep(random.uniform(0.5, 5.0))

    input("Press any key to close the browser...")
    driver.quit()

if __name__ == "__main__":
    open_ahrefs()