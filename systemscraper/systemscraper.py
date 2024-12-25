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


def pollImageDownload(_imageSrc, imgPath):

    if not os.path.exists(imgPath):
        os.makedirs(imgPath)

    if not _imageSrc:
        print("[LOG]: No image source found")

    response = requests.get(_imageSrc)
    if response.status_code != 200:
        print(f"[WARNING]: Failed to download image from {_imageSrc}")
    
    # Extract filename from the URL
    pathname = os.path.join(imgPath, "campaign_picture.jpg")
    
    # Save the image
    with open(pathname, "wb") as file:
        file.write(response.content)
    print(f"[LOG]: Image downloaded: campaign_picture.jpg")


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

campaign = soup.find("div", {"class":"css-1rynq56 r-dnmrzs r-1udh08x r-1udbk01 r-3s2u2q r-1iln25a"}).text



def addJSONObject(sheetStr, key, value):
    return sheetStr + "{ \"" + key + "\": " + value + " }"

def findOptionValue(option, j):
    optionValue = ""
    for i in range(5):
        try:
            if i == 0:
                optionValue = option.find_element(By.CSS_SELECTOR, ".css-11aywtz.r-6taxm2.r-1mlwlqe.r-16y2uox.r-1wbh5a2.r-10paoce.r-lnhwgy").get_attribute("value")
                if optionValue == "":
                    optionValue = option.find_element(By.CSS_SELECTOR, ".css-11aywtz.r-6taxm2.r-1mlwlqe.r-16y2uox.r-1wbh5a2.r-10paoce.r-lnhwgy").get_attribute("placeholder")
            if i == 1:
                optionValue = option.find_element(By.CSS_SELECTOR, ".css-1rynq56.r-dnmrzs.r-1udh08x.r-1udbk01.r-3s2u2q.r-1iln25a.r-13awgt0.r-fdjqy7").text
            if i == 2:
                optionValue = option.find_element(By.CSS_SELECTOR, ".css-11aywtz.r-6taxm2.r-1mlwlqe.r-16y2uox.r-1wbh5a2.r-10paoce.r-lnhwgy").text
            if i == 3:
                optionValue = option.find_element(By.CSS_SELECTOR, ".css-175oi2r.r-1awozwy.r-1777fci[style]").get_attribute("style")
                if optionValue == "width: 20px; height: 20px; border-radius: 3px; border-width: 1px; border-color: rgb(87, 74, 226); background-color: rgb(87, 74, 226);":
                    optionValue = "true"
                elif optionValue == "width: 20px; height: 20px; border-radius: 3px; border-width: 1px; border-color: rgb(153, 153, 153); background-color: rgba(143, 155, 179, 0.08);":
                    optionValue = "false"
                else:
                    continue
            if i == 4:
                optionValue = option.find_element(By.CSS_SELECTOR, '.css-175oi2r[style*="border-color"]').get_attribute("style")
                if optionValue == "border-color: rgb(87, 74, 226); background-color: rgb(87, 74, 226); width: 52px; height: 32px; border-radius: 16px; border-width: 1px; justify-content: center; align-self: center; overflow: hidden;":
                    optionValue = "true"
                elif optionValue == "border-color: rgb(153, 153, 153); background-color: rgba(143, 155, 179, 0.08); width: 52px; height: 32px; border-radius: 16px; border-width: 1px; justify-content: center; align-self: center; overflow: hidden;":
                    optionValue = "false"

            return optionValue
        except:
            continue

def appendSectionFieldJSONObject(sheetStr, fieldInfoDict, isLastField):
    sheetStr = sheetStr + "{"+newlineWithIndent(5)
    for key in fieldInfoDict:
        if fieldInfoDict[key] == "" or fieldInfoDict[key] is None:
            fieldInfoDict[key] = "\"\""
        if key != "defaultModifier":
            sheetStr = sheetStr + f"\"{key}\": {fieldInfoDict[key]}," + newlineWithIndent(5)
        else:
            sheetStr = sheetStr + f"\"{key}\": {fieldInfoDict[key]}" + newlineWithIndent(4)
    if not isLastField:
        sheetStr = sheetStr + "}," + newlineWithIndent(4)
    else:
        sheetStr = sheetStr + "}" + newlineWithIndent(3) + "]" + newlineWithIndent(2) + "}" + newlineWithIndent(1)
    return sheetStr

def newlineWithIndent(level):
    return "\n" + level*"  "



# COPY SHEET TEMPLATE
driver.find_element(By.XPATH, "//*[@id=\"app\"]/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div[2]").click()
sleep(1)
sheetStr = "{" + newlineWithIndent(1)

i = 0
elementlist = driver.find_element(By.XPATH, "//*[@id=\"app\"]/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div/div/div[2]/div")
elementlist = elementlist.find_elements(By.XPATH, "./*")
elementlist.pop()

for element in elementlist:
    curElement = element.find_element(By.CLASS_NAME, "css-1rynq56")
    isNextElementASection = False
    if i <= len(elementlist) - 2:
        isNextElementASection = elementlist[i+1].find_element(By.CLASS_NAME, "css-1rynq56").get_attribute("style") == "color: rgb(255, 255, 255); font-size: 18px; font-weight: 800; font-family: AvenirNext-Bold;"
    if i == len(elementlist) - 1:
        isNextElementASection = True
    curHeaderDesc = None


    # Section
    if curElement.get_attribute("style") == "color: rgb(255, 255, 255); font-size: 18px; font-weight: 800; font-family: AvenirNext-Bold;":
        try:
            curHeaderDesc = curElement.find_element(By.CLASS_NAME, "css-1rynq56 r-dnmrzs r-1udh08x r-1udbk01 r-3s2u2q r-1iln25a").text if curHeaderDesc is not None else ""
        except:
            pass
        if i != 0:
            sheetStr = sheetStr + "],"  + newlineWithIndent(1)

        sheetStr = sheetStr + f"{json.dumps(curElement.text)}: [" + newlineWithIndent(2)
        sheetStr = addJSONObject(sheetStr, "Section Description" , json.dumps(curHeaderDesc)) + "," + newlineWithIndent(2)
        sheetStr = sheetStr + "{ \"Section Fields\": ["+newlineWithIndent(4)

    # Field
    else:
        dictKeys = ["Name", "Type", "Reference", "Description", "usesModifiers", "isLocked", "isHidden", "usesDefaultValue", "usesMathExpression", "defaultValue", "defaultModifier"]
        fieldInfoDict = {
            "Name":"",
            "Type":"",
            "Reference":"",
            "Description":"",
            "usesModifiers":"",
            "isLocked":"",
            "isHidden":"",
            "usesDefaultValue":"",
            "usesMathExpression":"",
            "defaultValue":"",
            "defaultModifier":""
          }
        curElement.click()
        curElement = driver.find_element(By.XPATH, "//*[@id=\"app\"]/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div/div/div/div")
        fieldOptions = curElement.find_elements(By.CSS_SELECTOR, ".css-175oi2r.r-1c45kls.r-4k9ar7.r-1niwhzg.r-jw8lkh")
        fieldType = driver.find_element(By.XPATH, "//*[@id=\"app\"]/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div[1]").text

        j = 0
        for option in fieldOptions:
            if fieldType == "Text Area":
                dictKeys = ["Name", "Type", "Reference", "Description", "usesModifiers", "isLocked", "isHidden", "usesDefaultValue", "defaultValue", "defaultModifier"]
            try:
                optionStr = findOptionValue(option, j)
                fieldInfoDict[dictKeys[j]] = json.dumps(optionStr)
            except Exception:
                pass
            j = j + 1
        driver.find_element(By.XPATH, "//*[@id=\"app\"]/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/div").click()
        sheetStr = appendSectionFieldJSONObject(sheetStr, fieldInfoDict, isNextElementASection)

    if i == len(elementlist) - 1:
        sheetStr = sheetStr + "]\n}"
    i = i + 1
    campaign_foldername = f"{campaign}_({campaign_url[0:5]})"

# SAVE CAMPAIGN PICTURE
imgSource = soup.find("div", {"class":"css-175oi2r r-1c45kls r-4k9ar7 r-1niwhzg r-1h0z5md r-1awozwy r-18u37iz", "style":"flex: 1 1 0%;"}).find("img", {"class":"css-9pa8cd"}).get("src")
pollImageDownload(imgSource, "mRPG_Archive\\"+campaign_foldername)

# SAVE SHEET JSON
try:
    filename = "mRPG_Archive\\"+campaign_foldername+"\\system_sheet.json"
    with open(filename, 'w', encoding='utf-16') as file:
        file.write(sheetStr)
    print(f"File '{filename}' has been created and written successfully.")
except Exception as e:
    print(f"[ERROR]: An error occurred while writing to the file: {e}")

    

def isEmpty(charactersheet, type, index):
    return charactersheet[type][index] == "" or charactersheet[type][index] is None or charactersheet[type][index] == "\"\""
    
def isSheetSection(charactersheet, index):
    return not isEmpty(charactersheet, "title", index) and isEmpty(charactersheet, "value", index) and isEmpty(charactersheet, "mod", index)