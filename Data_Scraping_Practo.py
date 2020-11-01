#Scraping Data of Dentists from Practo
#By Sangeet Agarwal
import requests
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
import pandas as pd

column=[' Name_of_Dr ',' Dr_Exp', ' Specialisation ' , ' Address ' , ' Fee ' , ' Services ']

Cities = ['Mumbai','Delhi','Rajkot','Jaipur','Chandigarh']
for city in Cities:
    data=[] #creating an empty list for storing the data
    # Web scrapper for infinite scrolling page
    driver = webdriver.Chrome(executable_path=r"C:\Users\sangeet\OneDrive\Desktop\WebScraping_Job\chromedriver.exe")
    driver.get("https://www.practo.com/search?results_type=doctor&q=%5B%7B%22word%22%3A%22Dentist%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=" + city)
    time.sleep(1.5)  # Allowing 1.5 seconds for the web page to open
    scroll_pause_time = 1.5 # setting pause time.
    screen_height = driver.execute_script("return window.screen.height;")   # getting the screen height of the web
    i = 1

    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break

    page_soup = BeautifulSoup(driver.page_source, "html.parser")

    Drs = page_soup.findAll("div",{"class": "info-section"}) #finding the class to get the Doctors link

    for dr in range(len(Drs)):
         link = Drs[dr] #  taking the first Doctor link
         Drs_url = "https://www.practo.com" + link.a['href'] # extracting the actual doctor link
         Dr_page = requests.get(Drs_url) #getting the Doctors page from internet
         Dr_html = BeautifulSoup(Dr_page.text, "html.parser") # parsing the Doctors page as HTML

         try:
            Parsing_Name_of_Dr = Dr_html.find_all('h1', {'data-qa-id': "doctor-name"})
            Name_of_Dr = Parsing_Name_of_Dr[0].text
         except:
             Name_of_Dr = "NA"

         try:
            Parsing_Dr_Exp = Dr_html.find_all('div', {'class': 'c-profile--qualification'})
            Dr_Exp = re.findall('[0-9]+', str(Parsing_Dr_Exp[0].text))[0]
         except:
            Dr_Exp = "Not Mentioned"

         Parsing_Dr_Spec = Dr_html.find_all('div', {'data-qa-id': "specializations-item"})
         Spec = []
         for num in range(len(Parsing_Dr_Spec)):
             Spec.append(Parsing_Dr_Spec[num].span.text)

         Parsing_Addr = Dr_html.find_all('p',{'class': 'c-profile--clinic__address'})
         Addr = []
         for num in range(len(Parsing_Addr)):
             Addr.append(Parsing_Addr[num].text)

         Parsing_Dr_Fee = Dr_html.find_all('span', {'data-qa-id': "consultation_fee"})
         Fee = []
         for num in range(len(Parsing_Dr_Fee)):
             Fee.append(Parsing_Dr_Fee[num].text)

         Parsing_Services = Dr_html.find_all('div', {'data-qa-id': "services-item"})
         Services = []
         for num in range(len(Parsing_Services)):
             Services.append(Parsing_Services[num].span.text)

         data.append((Name_of_Dr, Dr_Exp, Spec, Addr, Fee, Services))

    #storing the data in a dataframe
    df = pd.DataFrame(data, columns=column)
    file_name = "Dentist_List_" + city + ".csv"
    #storing the data in a csv file
    df.to_csv(file_name,index=False)