import json
import os
import re
from time import sleep, time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


benchmarkStats = {"sheet_size":"0", "sheet_quantity":"0"}

def find_element_with_multiple_xpaths(driver, xpaths, isNumberField):
    # Try multiple XPaths until one works.
    if(isNumberField):
        xpaths.pop(0)
    for xpath in xpaths:
        try:
            element = driver.find_element(By.XPATH, xpath)
            return element.text  # Return the text of the found element
        except Exception as e:
            continue  # Try the next XPath
    return None  # Return None if no element was found

def pollImageDownload(_imageSrc, name: str, campaign: str):
    replacements = {
        '.': 'dot',
        ':': 'colon',
        '<': 'lt', 
        '>': 'gt',
        '"': 'quote',
        '/': 'slash', 
        '\\': 'backslash',
        '|': 'pipe',
        '?': 'qm',
        '*': 'asterisk'
    }

    def replace(match):
        return replacements[match.group(0)]
    
    invalid_characters = r'[\.<>:"/\\|?*]'
    name = re.sub(invalid_characters, replace, name).strip()
    
    newpath = "mRPG_Archive\\" + campaign + "\Characters\\" + name
    filename = name + ".jpg"

    if not os.path.exists(newpath):
        os.makedirs(newpath)

    if os.path.isfile(newpath + "\\" + filename):
        print("[LOG]: The image for " + newpath + " already exists.")
        return newpath

    if not _imageSrc:
        print("[LOG]: No image source found")
        return newpath
    response = requests.get(_imageSrc)
    if response.status_code != 200:
        print(f"[WARNING]: Failed to download image from {_imageSrc}")
    
    # Extract filename from the URL
    pathname = os.path.join(newpath, filename)
    
    # Save the image
    with open(pathname, "wb") as file:
        file.write(response.content)
    print(f"[LOG]: Image downloaded: {filename}")
    return newpath

# Set up Selenium
service = Service()  # Path to ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36")
options.add_argument("user-data-dir=C:/Users/PC/AppData/Local/Google/Chrome/User Data")  # Path to your Chrome profile
options.add_argument("profile-directory=Default")
driver = webdriver.Chrome(service=service, options=options)

loginUrl = "https://web.mrpg.app/auth/login"
driver.get(loginUrl)
sleep(0.5)
if (driver.current_url == loginUrl):
    sleep(3)
    email = input("[PROMPT]: Input your email in the terminal or the website and press enter:\n")
    if(email != ""):
        driver.find_element(By.XPATH, "//*[@id=\"app\"]/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div/input").send_keys(email)
    password = input("[PROMPT]: Input your password in the terminal or the website and press enter:\n")
    if(password != ""):
        driver.find_element(By.XPATH, "//*[@id=\"app\"]/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/input").send_keys(password)
    driver.find_element(By.XPATH, "//*[@id=\"app\"]/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div/div/div[1]/div/div[2]/div/div/div[4]/div").click()
    sleep(1)
sleep(0.5)

# Navigate to the target page
mrpg_url = input("[PROMPT]: Please select the campaign in the opened browser or type in the corresponding URL and press enter:\n")
start_time = time()
if mrpg_url is None or mrpg_url == "":
    mrpg_url = driver.current_url
else:
    driver.get(mrpg_url)
campaign_url = mrpg_url.split("/")[-1]
sleep(1)
# Wait for specific content to load
page_to_scrape = driver.page_source
soup = BeautifulSoup(page_to_scrape, "html.parser")

last_height = driver.execute_script("return document.body.scrollHeight")


characterlist = soup.find_all("div", {"class":"css-175oi2r", "style":"background-color: rgba(0, 0, 0, 0); margin-top: 0px; margin-bottom: 0px;"})
campaign = soup.find("div", {"class":"css-1rynq56 r-dnmrzs r-1udh08x r-1udbk01 r-3s2u2q r-1iln25a"}).text
benchmarkStats.update({"sheet_quantity":str(len(characterlist))})

characterpaths = []

for character in characterlist:
    name = character.find("div", {"class":"css-1rynq56", "style":"color: rgb(255, 255, 255); font-size: 15px; font-weight: 600; font-family: AvenirNext-DemiBold;"}).text
    image = character.find("img", {"class":"css-9pa8cd"})
    imageSrc = None
    try:
        imageSrc = image.get("src")
    except Exception as e:
        pass
    characterpaths.append(pollImageDownload(imageSrc, name, (f"{campaign}_({campaign_url[0:5]})")))


for character in characterlist:
    i = characterlist.index(character)

    # select the character from the list
    element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id=\"app\"]/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div/div["+ str(i+1) +"]/div/div[1]")))
    element.click()   
    sleep(0.5)

    page_to_scrape = driver.page_source
    soup = BeautifulSoup(page_to_scrape, "html.parser")

    sheet = soup.find("div", class_=re.compile(r"css-175oi2r.*r-1sv84sj.*r-1j3t67a"))
    sheetitems = sheet.find_all("div", recursive=False)

    charactersheet = {"title": [], "value": [], "mod": []}
    for item in sheetitems:
        j = sheetitems.index(item)+1
        try:
            commonXPath = "//*[@id=\"app\"]/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div["+str(j)+"]/div/div"
            isNumberField = False 
            try:
                isNumberField = (driver.find_element(By.XPATH, commonXPath+"/div/div").get_attribute("class")) == "css-175oi2r r-1c45kls r-4k9ar7 r-1niwhzg r-1wtj0ep r-obd0qt r-18u37iz r-15d164r"
            except Exception:
                pass

            titleOptions = [
            commonXPath + "/div/div[1]/div/div[1]",
            commonXPath + "/div/div[1]/div/div/div[1]",
            commonXPath + "/div[1]"
            
            ]

            valueOptions = [
            commonXPath+"/div/div[1]/div/div[2]/div/div/div[1]", 
            commonXPath+"/div/div[1]/div/div[2]/div/div", 
            commonXPath+"/div/div[1]/div/div/div[2]/div"
            ]
            modOptions = [commonXPath+"/div/div[1]/div/div/div[2]/div[1]/div"]

    	    
            title = json.dumps(re.sub(r"\n.*", "", find_element_with_multiple_xpaths(driver, titleOptions, isNumberField)))
            value = json.dumps(find_element_with_multiple_xpaths(driver, valueOptions, False) or '')
            mod = find_element_with_multiple_xpaths(driver, modOptions, False)

            if title == "null":
                continue

            title = title if title is not None else ""
            value = value if value is not None else ""
            mod = mod if title is not None else ""

            charactersheet["title"].extend([title])
            charactersheet["value"].extend([value])
            charactersheet["mod"].extend([mod])
        except Exception as e:
            pass

    def isEmpty(charactersheet, type, index):
        return charactersheet[type][index] == "" or charactersheet[type][index] is None or charactersheet[type][index] == "\"\""
    
    def isSheetSection(charactersheet, index):
        return not isEmpty(charactersheet, "title", index) and isEmpty(charactersheet, "value", index) and isEmpty(charactersheet, "mod", index)

    fileStr = "{\n  "
    sheetLength = len(charactersheet["title"])
    benchmarkStats.update({"sheet_size":str(sheetLength)})
    for k in range(sheetLength):
        if isSheetSection(charactersheet, k):
            if k>=1:
                fileStr = fileStr + "],\n  "
            fileStr = fileStr + f"{charactersheet['title'][k]}: [\n"

        elif not isEmpty(charactersheet, "title", k) and not isEmpty(charactersheet, "value", k):
            jsonTitle = charactersheet["title"][k]
            jsonValue = charactersheet["value"][k]
            if not isEmpty(charactersheet, "mod", k):
                jsonValue = jsonValue[0:len(jsonValue)-1] + f" (Mod: {charactersheet['mod'][k]})\""
            # This procedure just prevents trailing commas at the end of a list section because JSON Parsers can get all whiny over it
            comma = ","
            if k+1 == len(charactersheet["title"]) or (k + 1 <= len(charactersheet["title"]) and isSheetSection(charactersheet, k+1)):
                comma = ""
            fileStr = fileStr + f"  {{ {jsonTitle}:{jsonValue}  }}{comma}\n"
    fileStr = fileStr + "]\n}\n"

    try:
        filename = characterpaths[i]+"\\character_sheet.json"
        with open(filename, 'w', encoding='utf-16') as file:
            file.write(fileStr)
        print(f"File '{filename}' has been created and written successfully.")
    except Exception as e:
        print(f"[ERROR]: An error occurred while writing to the file: {e}")

        element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id=\"app\"]/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/div")))
        element.click()
    sleep(0.2)
    driver.find_element(By.XPATH,"//*[@id=\"app\"]/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/div").click()

print(f"Finished! - ({round(time()-start_time, 2)} seconds) for {benchmarkStats['sheet_quantity']} sheets with {benchmarkStats['sheet_size']} elements. ({int(benchmarkStats['sheet_quantity'])*int(benchmarkStats['sheet_size'])} Elements in total.)")