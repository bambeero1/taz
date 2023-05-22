import asyncio 
import sqlite3
from playwright.async_api import async_playwright
from datetime import datetime

async def get_dress_info(dress_element): 
    try:
        # Get the dress price
        price_element = await dress_element.query_selector('div > div:nth-child(2) > div > span')
        price = await price_element.text_content() if price_element else None

        # Get the original dress price
        oprice_element = await dress_element.query_selector('div > div:nth-child(2) > div > del')
        oprice = await oprice_element.text_content() if oprice_element else None

        # Get the dress URL
        urlc = await dress_element.get_attribute('href')
        urld = "https://en.abiyefon.com" + urlc

        # Get the list of sizes for this dress
        sizes_element = await dress_element.query_selector('div.product-sizes.pimghover')
        if sizes_element:
            size_elements = await sizes_element.query_selector_all('div')
            sizes = [await size_element.text_content() for size_element in size_elements if await size_element.get_attribute('class') != 'out_of_stock']
        else:
            sizes = []

        if price and oprice:
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y %H:%M:%S")
            
            percentage1 = (float(price.strip('$')) / float(oprice.strip('$'))) * 100
            percentage = 100 - percentage1
            print(f"Scraped dress: price={price}, original price={oprice}, sizes={', '.join(sizes)}, url={urld}, percentage={percentage}, date/time={date_time}") 
            return (price, oprice, ', '.join(sizes), urld, percentage, date_time)
        else:
            return None

    except Exception as e:
        print(f"There was an error processing a dress element: {e}")
        return None

async def main(): 
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            conn = sqlite3.connect('dresses.db')
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS dresses 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            new_price TEXT, original_price TEXT, sizes TEXT, url TEXT UNIQUE, percentage REAL, date_time TEXT)''')  

            page_number = 1
            insert_count = 0
            update_count = 0

            while True:
                url = f'https://en.abiyefon.com/plus-size-evening-dresses?sort=c2e&page={page_number}'
                print(f"Scraping page {page_number}: {url}")

                await page.goto(url)

                # Get the list of dress elements
                dress_elements = await page.query_selector_all('xpath=/html/body/div[1]/div/div[2]/section/div/div[4]/div/ul/li[*]/a')

                if not dress_elements:
                    # No more pages to check, break out of loop
                    print("No more pages to scrape. Exiting.")
                    break

                dress_info = await asyncio.gather(*[get_dress_info(dress_element) for dress_element in dress_elements])
                for info in dress_info:
                    if info:
                        try:
                            cur.execute("INSERT OR IGNORE INTO dresses (new_price, original_price, sizes, url, percentage, date_time) VALUES (?, ?, ?, ?, ?, ?)", info)
                            if cur.rowcount == 1:
                                insert_count += 1
                                print(f"Inserted dress data into the database: {info}")
                            else:
                                cur.execute("UPDATE dresses SET new_price=?, original_price=?, sizes=?, percentage=?, date_time=? WHERE url=?", (info[0], info[1], info[2], info[4], info[5], info[3]))
                                update_count += 1
                                print(f"Updated dress data in the database: {info}")
                        except sqlite3.Error as db_error:
                            print(f"An error occurred while inserting/updating dress data into the database: {db_error}")

                conn.commit()
                page_number += 1

        except Exception as e:
            print(f"There was an error during the scraping process: {e}")

        finally:
            await browser.close()
            conn.close()
            print(f"Total inserts: {insert_count}, total updates: {update_count}")

asyncio.run(main())