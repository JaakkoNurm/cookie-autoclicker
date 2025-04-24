from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import re
import time

driver = webdriver.Chrome()
driver.get("https://orteil.dashnet.org/cookieclicker/")

buildings_cps = {}

# Wait for the page to load
driver.implicitly_wait(10)

assert "Cookie" in driver.title
# Click the "Got it!" button
driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/button[1]").click()

# Select English as the language
driver.find_element(By.ID, "langSelect-EN").click()

# Wait for the page to load completely
time.sleep(3)  # Add a short delay to ensure the page is fully loaded

try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "bigCookie"))
    )
except Exception as e:
    print(f"Error: Unable to locate or interact with 'bigCookie'. Details: {e}")
    driver.quit()
    exit(1)  # Exit the script if the element cannot be found

button = driver.find_element(By.XPATH, "/html/body/div[1]/div/a[1]")
driver.execute_script("arguments[0].click();", button)

bigCookie = driver.find_element(By.ID, "bigCookie")

def current_cookies():
    # Get the current number of cookies
    cookies = driver.find_element(By.ID, "cookies").text
    print(f"Current cookies: {cookies}")

def current_cps():
    # Get the current cookies per second (CPS)
    try:
        cps = driver.find_element(By.ID, "cookiesPerSecond").text
        # Extract the numeric value from the text
        cps = float(re.findall(r"\d+(?:\.\d+)?", cps)[0])
        print(f"Current CPS: {cps}")
        return cps
    except StaleElementReferenceException:
        print("StaleElementReferenceException encountered in current_cps. Retrying...")
        return current_cps()

def click_cookie(clicks = 10):
    time.sleep(0.1)
    # Click the cookie a specified number of times
    print(f"Clicking cookie {clicks} times...")
    for _ in range(clicks):
        bigCookie.click()

def get_available_upgrades():
    # Get first available upgrade
    print("Getting available upgrades...")
    try:
        # Use JavaScript to check for enabled upgrades
        has_upgrades = driver.execute_script("return document.querySelectorAll('.crate.upgrade.enabled').length > 0")
        
        if has_upgrades:
            # Only now try to get the element with Selenium
            upgrade = driver.find_element(By.CSS_SELECTOR, ".crate.upgrade.enabled")
            print("Found available upgrade")
            return upgrade
        else:
            print("No available upgrades found")
            return None
    except Exception as e:
        print(f"Error finding upgrades: {e}")
        return None

def get_available_buildings():
    # Get the available buildings
    print("Getting available buildings...")
    buildings = driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")
    return buildings

def buy_upgrade(upgrade):
    upgrade.click()

def buy_building(building):
    try:
        building_name = building.find_element(By.CLASS_NAME, "title").text

        previous_cps = current_cps()
        building.click()
        time.sleep(0.5)
        new_cps = current_cps()

        cps_difference = new_cps - previous_cps
    
        if building_name not in buildings_cps or cps_difference > 0:
            buildings_cps[building_name] = cps_difference
            print(f"Updated CPS for {building_name}: +{cps_difference:.2f}")
    
    except StaleElementReferenceException:
        print("StaleElementReferenceException encountered in buy_building. Retrying...")
        buildings = get_available_buildings()
        if building in buildings:
            buy_building(building)

def best_purchase(upgrade, buildings):
    """Determine the best purchase option based on ROI (Return on Investment)."""
    
    # Always prioritize upgrades as they typically provide significant multipliers
    if upgrade:
        print("Prioritizing available upgrade!")
        return upgrade
    
    # Track the best building to buy
    best_option = None
    best_roi = -1
    
    for building in buildings:
        # Get building name for better logging
        try:
            building_name = building.find_element(By.CLASS_NAME, "title").text
        except:
            building_name = "Unknown Building"
            
        # Unlock new building types as a priority to expand options
        if building_name not in buildings_cps:
            return building
            
        # Calculate ROI (Return on Investment)
        try:
            price = int(building.find_element(By.CLASS_NAME, "price").text.replace(",", ""))
            cps = buildings_cps[building_name] if building_name in buildings_cps else 0
            
            # Calculate payback period (seconds to recoup investment)
            payback_period = price / cps if cps > 0 else float('inf')
            
            # ROI is inverse of payback period - higher is better
            roi = 1 / payback_period if payback_period > 0 else 0
            
            if roi > best_roi:
                best_roi = roi
                best_option = building
        except Exception as e:
            print(f"Error calculating ROI for {building_name}: {e}")
    
    if best_option:
        try:
            best_name = best_option.find_element(By.CLASS_NAME, "title").text
            print(f"Best purchase: {best_name} with ROI: {best_roi:.6f}")
        except:
            print(f"Selected best building with ROI: {best_roi:.6f}")
    else:
        print("No viable buildings to purchase")
        
    return best_option
        
def quit():
    # Close the browser
    driver.quit()

def main():
    print("Starting Cookie Clicker bot...")
    print("Press control + c to stop.\n")

    try:
        while True:
            # Click the cookie a few times
            click_cookie(150)

            # Get available upgrades and buildings
            upgrade = get_available_upgrades()
            buildings = get_available_buildings()
            print(f"Available buildings: {len(buildings)}")

            # Determine the best purchase
            best_item = best_purchase(upgrade, buildings)
            print(buildings_cps)
            # Buy the best item if available
            if best_item:
                if "upgrade" in best_item.get_attribute("class"):
                    print(f"Buying upgrade: {best_item}")
                    buy_upgrade(best_item)
                elif "product" in best_item.get_attribute("class"):
                    print(f"Buying building: {best_item}")
                    buy_building(best_item)

    except KeyboardInterrupt:
        print("Exiting script...")

if __name__ == "__main__":
    main()
