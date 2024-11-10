import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def get_ingredients(url):
    # Set up WebDriver (e.g., using Chrome)
    print(f"Load URL in Scraping: {url}")
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for better performance
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    # if ulta url
    if "ulta.com" in url:
    # After clicking, find the ingredients section
        try:
            try:
                popup_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'I Understand')]"))
                )
                popup_button.click()  # Close the pop-up
                print("Pop-up closed.")
            except:
                print("No pop-up detected.")
            
            # Wait for the button to load (you can also use WebDriverWait for better stability)
            scroll_attempts = 0
            button = None
            while scroll_attempts < 10:  # limit scroll attempts to avoid infinite loop
                try:
                    button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[.//h3[text()='Ingredients']]"))
                    )
                    break  # Exit loop if button is found and clickable
                except:
                    driver.execute_script("window.scrollBy(0, 600);")  # Scroll down incrementally
                    scroll_attempts += 1
                    time.sleep(0.5)  # Short delay to allow page loading

            if button:
                # Directly click the button using JavaScript for reliability
                button.click()
                print("Ingredients section expanded.")
                
                time.sleep(1)

                ingredients_section = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div/div/main/div[4]/div/div[9]/div/div/div[3]/section"))
                )
                #print("Ingredients section: ", ingredients_section)
                ingredients_text = ingredients_section.find_element(By.TAG_NAME, "p").text
                #print("Ingredients text: ", ingredients_text)
                ingredients_text = ingredients_text.rstrip(".")
                # Now find the div containing the ingredients list inside the expanded section
                ingredients_list = [ingredient.strip() for ingredient in ingredients_text.split(",")]
                print(ingredients_list)
                return ingredients_list
                
            else:
                print("Ingredients button not found.")
                return "Unable to find ingredients :("
        except Exception as e:
            print("Error extracting ingredients:", e)
            driver.quit()
        finally:
            driver.quit()
    
    #insidecoder website
    elif "incidecoder.com" in url:
        print()
        try:
            # Wait for the ingredients list section to load
            ingredients_section = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ingredlist-short-like-section"))
            )
            # Now get all the ingredient links inside the section
            ingredient_links = ingredients_section.find_elements(By.CSS_SELECTOR, "a.ingred-link")
            
            # Extract text for each ingredient
            ingredients_list = [link.text for link in ingredient_links]
            
            #print("Ingredients List:", ingredients_list)
            return ingredients_list
        except Exception as e:
            print("Error extracting ingredients from Incidecoder:", e)
            driver.quit()
        finally:
            driver.quit()
        
        
    else:
        print("Unsupported website. Please provide a URL from the Ulta or Insidecoder websites!")

if __name__ == '__main__':
    get_ingredients("https://incidecoder.com/products/glossier-futuredew")