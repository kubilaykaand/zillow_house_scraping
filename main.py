from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service 

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}

response= requests.get("https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.7439559777441%2C%22east%22%3A-122.20425260860347%2C%22south%22%3A37.52745260885822%2C%22north%22%3A37.91145629713992%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D", headers=headers)

data= response.text
soup=BeautifulSoup(data,"html.parser")

all_link_elements = soup.select("a.property-card-link")

all_links=[]

for link in all_link_elements:
    href = link["href"]
    #print(href)
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

all_address_elements=soup.select("address")
all_addresses=[]
for address in all_address_elements:
    address=address.text
    address= address.split(" | ")[-1]
    all_addresses.append(address)
    print(address)
#print(all_addresses)

all_price_elements= soup.find_all("div",{"class":"StyledPropertyCardDataArea-c11n-8-89-0__sc-yipmu-0 kvldQr"})
#print(f"all price elements{all_price_elements}")
price_tag=[]
for prices in all_price_elements:
    try:
        price = prices.find("div",{"class":"PropertyCardWrapper__StyledPriceGridContainer-srp__sc-16e8gqd-0 kSsByo"})
    except IndexError:
        print('Multiple listings for the card')
        price =prices.select()(".property-card-price li")[0].contents[0]
    finally:
        price_tag.append(price)
#print(f"all prices are{all_prices}")
all_prices=[]
for x in range(0,len(price_tag)):
    try:
        price_text= price_tag[x].find("span",{"class":"PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr"}).text
    except IndexError:
        #print('Multiple listings for the card')
        price_text= price_tag[x].find("div",{"class":"StyledPropertyCardDataArea-c11n-8-89-0__sc-yipmu-0 eLdkcJ"})
        other_enlisted=price_text.find("ul",{"class":"StyledPropertyCardHomeDetailsList-c11n-8-89-0__sc-1xvdaej-0 GlipV"})
        sub_cat1=other_enlisted.find("li")
        sub_cat2=sub_cat1.find("b")
        #print(sub_cat2)
        price_text=sub_cat2.text
    finally:
        all_prices.append(price_text)
print(f"prices:****{all_prices}")


service=Service("C:\Development\chromedriver_win32\chromedriver.exe")

driver= webdriver.Chrome(service=service)

print(f"ADRESSES:{all_addresses}")
print(f"PRICES{all_prices}")
print(f"LINKS{all_links}")
for n in range(len(all_links)):
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSeu9anDqJTQxIniuQIkpJNikrAR_BtUQDsMNk7RfP9j176Diw/viewform?vc=0&c=0&w=1&flr=0")
    time.sleep(2)

    address= driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link= driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button= driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    
    
    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()