import asyncio
import json
import os
import shutil
from aiohttp import ClientSession, ClientTimeout
from urllib.parse import urlparse, urlencode
from playwright.async_api import async_playwright
import pandas as pd

# Uses Python 3.7 to avoid conflicts with aiohttp

# Function to extract the domain from a URL
def extract_domain(url):
    """
    Extract the domain from the given URL.
    If the domain starts with 'www.', it removes it.

    Args:
        url (str): The URL to extract the domain from.

    Returns:
        str: The extracted domain.
    """
    domain = urlparse(url).netloc
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

async def download_image(session, img_url, file_path, retries=3):
    """
    Download an image from the given URL and save it to the specified file path.
    If the download fails, it retries the specified number of times.

    Args:
        session (ClientSession): The aiohttp session to use for downloading.
        img_url (str): The URL of the image to download.
        file_path (str): The path to save the downloaded image.
        retries (int, optional): The number of retries for downloading. Defaults to 3.

    Returns:
        None
    """
    attempt = 0
    while attempt < retries:
        try:
            # Attempt to download the image
            async with session.get(img_url) as response:
                if response.status == 200:
                    # Write the image content to the file
                    with open(file_path, "wb") as f:
                        f.write(await response.read())
                    print(f"Downloaded image to: {file_path}")
                    return
                else:
                    print(f"Failed to download image from {img_url}. Status: {response.status}")
        except Exception as e:
            print(f"Error downloading image from {img_url}: {e}")
        attempt += 1
        # Retry if the maximum number of attempts has not been reached
        if attempt < retries:
            print(f"Retrying download for {img_url} (attempt {attempt + 1}/{retries})")
            await asyncio.sleep(2**attempt)  # Exponential backoff for retries
    print(f"Failed to download image from {img_url} after {retries} attempts.")

# Navigates to google images by setting up an asynchronous Playwright instance to control a Chromium browser
# ex. asyncio.run(scrape_google_images(search_query="iphone 16 pro", max_images=1))
async def scrape_google_images(search_query, max_images=None):
    """
    Scrape images from Google Images for a given search query.

    Args:
        search_query (str, optional): The search term to use for Google Images. Defaults to "macbook m3".
        max_images (int, optional): The maximum number of images to download. If None, downloads all available. Defaults to None.
    Returns:
        None
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) 
        page = await browser.new_page()

        query_params = urlencode({"q": search_query, "tbm": "isch"}) # tbm=isch parameter returns image search results
        # example url: https://www.google.com/search?q=iphone+16+pro&tbm=isch
        search_url = f"https://www.google.com/search?{query_params}"

        # print(f"Navigating to search URL: {search_url}")
        await page.goto(search_url)  # Navigate to the search results page

        # Set up directories for image storage
        download_folder = "downloaded_images"
        json_file_path = "google_images_data.json"

        # if os.path.exists(download_folder):
        #    Prompt the user whether to delete or archive the existing folder
        #    user_input = input(f"The folder '{download_folder}' already exists. Do you want to delete it? (yes/no): ")
        #    if user_input.lower() == "yes":
        #        print(f"Removing existing folder: {download_folder}")
        #        shutil.rmtree(download_folder)
        #   else:
        #        archive_folder = f"{download_folder}_archive"
        #        print(f"Archiving existing folder to: {archive_folder}")
        #        shutil.move(download_folder, archive_folder)
        # os.makedirs(download_folder)  # Create a new folder to store the images

        # Initialize the JSON file to store image metadata
        with open(json_file_path, "w") as json_file:
            json.dump([], json_file)

        # Find all image elements on the page
        # Maybe change this later to just query_selector
        image_element = await page.query_selector('div[data-attrid="images universal"]')
        # print(f"Found element on the page.")

        async with ClientSession() as session:
            try:
                # print(f"Processing image...")
                # Click on the image to get a full view
                await image_element.click()
                await page.wait_for_selector("img.sFlh5c.FyHeAf.iPVvYb[jsaction]")

                img_tag = await page.query_selector("img.sFlh5c.FyHeAf.iPVvYb[jsaction]")
                if not img_tag:
                    print(f"Failed to find image tag for element")

                # Get the image URL
                img_url = await img_tag.get_attribute("src")
                file_extension = os.path.splitext(urlparse(img_url).path)[1] or ".png"
                image_name = search_query.replace(" ", "_") # rename image
                file_path = os.path.join(download_folder, f"{image_name}{file_extension}")

                # Download the image
                await download_image(session, img_url, file_path)

                # Extract source URL and image description
                source_url = await page.query_selector('(//div[@jsname="figiqf"]/a[@class="YsLeY"])[2]')
                source_url = await source_url.get_attribute("href") if source_url else "N/A"
                image_description = await img_tag.get_attribute("alt")
                source_name = extract_domain(source_url)

                # Store image metadata
                image_data = {
                    "image_description": image_description,
                    "source_url": source_url,
                    "source_name": source_name,
                    "image_file": file_path,
                }

                # print(f"Image metadata prepared.")
            except Exception as e:
                print(f"Error processing image: {e}")

            # Save image metadata to a JSON file
            with open(json_file_path, "w") as json_file:
                json.dump(image_data, json_file, indent=4)

        # print(f"Finished downloading images.")
        await browser.close()  # Close the browser when done

products_df = pd.DataFrame(pd.read_csv(r'C:\Users\tiffa\Documents\HackUMass25\skincare_products_clean.csv'))

for name in products_df['product_name']:
    # remove any slashes or backslashes from the product name to avoid any download problems
    processed_name = name.replace("/", "")
    print(processed_name)
    asyncio.run(scrape_google_images(search_query=processed_name, max_images=1))