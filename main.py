from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import re

driver = webdriver.Firefox()
driver.get("https://orteil.dashnet.org/cookieclicker/")

buildings_cps = {}

# Wait for the page to load
driver.implicitly_wait(10)

assert "Cookie" in driver.title
# Click the "Got it!" button
driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/button[1]").click()

# Select English as the language
driver.find_element(By.ID, "langSelect-EN").click()

# Wait for cookie to be clickable
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "bigCookie"))
)

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
    # Click the cookie a specified number of times
    print(f"Clicking cookie {clicks} times...")
    for _ in range(clicks):
        bigCookie.click()

def get_available_upgrades():
    # Get the available upgrades
    print("Getting available upgrades...")
    upgrades_container = driver.find_element(By.ID, "upgrades")
    upgrades = upgrades_container.find_elements(By.CSS_SELECTOR, ".crate.upgrade.enabled")
    return upgrades

def get_available_buildings():
    # Get the available buildings
    print("Getting available buildings...")
    buildings_container = driver.find_element(By.ID, "products")
    buildings = buildings_container.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")
    return buildings

def buy_upgrade(upgrade):
    upgrade.click()

def buy_building(building):
    try:
        previous_cps = current_cps()
        building.click()
        new_cps = current_cps()
        buildings_cps[building] = new_cps - previous_cps
    except StaleElementReferenceException:
        print("StaleElementReferenceException encountered in buy_building. Retrying...")
        buildings = get_available_buildings()
        if building in buildings:
            buy_building(building)

def best_purchase(upgrades, buildings):
    # Determine the best purchase option
    best_purchase = (None, -1)
    if upgrades:
        return upgrades[0]  # Buy the first available upgrade

    for building in buildings:
        # Unlock new available buildings
        if building not in buildings_cps:
            return building
            
        price = int(building.find_element(By.CLASS_NAME, "price").text.replace(",", ""))
        cps = buildings_cps.get(building, 0)  # Use 0 if building is not in the dictionary
        cps_per_price = cps / price if price > 0 else 0
        if cps_per_price > best_purchase[1]:
            best_purchase = (building, cps_per_price)

    return best_purchase[0]
        
def quit():
    # Close the browser
    driver.quit()

def main():
    print("Starting Cookie Clicker bot...")
    print("Press control + c to stop.\n")

    try:
        while True:
            # Click the cookie a few times
            click_cookie(50)

            # Get available upgrades and buildings
            upgrades = get_available_upgrades()
            print(f"Available upgrades: {len(upgrades)}")
            buildings = get_available_buildings()
            print(f"Available buildings: {len(buildings)}")

            # Determine the best purchase
            best_item = best_purchase(upgrades, buildings)
            print(f"Best item to buy: {best_item}")

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
        quit()

if __name__ == "__main__":
    main()
