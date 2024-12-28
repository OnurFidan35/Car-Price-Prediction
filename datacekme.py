import pandas as pd
import numpy as np
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



geckodriver_path='C:\\Users\\Onur Fidan\\Documents\\SecondHandCar\\geckodriver.exe'
service = Service(geckodriver_path)
driver = webdriver.Firefox(service=service)

class Cars():
    def __init__(self):
        self.veri_cek()
    
    def veri_cek(self):
        driver.get("https://www.arabam.com/ikinci-el/otomobil?take=50&view=List")
        WebDriverWait(driver,10).until(

            EC.presence_of_element_located((By.CLASS_NAME,'listing-table-wrapper'))
            
        )
     
        
        data={
                "İlan No":[],
                "İlan Tarihi":[],
                "Marka":[],
                "Seri":[],
                "Model":[],
                "Yıl":[],
                "Kilometre":[],
                "Vites Tipi":[],
                "Yakıt Tipi":[],
                "Kasa Tipi":[],
                "Renk":[],
                "Motor Hacmi":[],
                "Motor Gücü":[],
                "Çekiş":[],
                "Araç Durumu":[],
                "Ort. Yakıt Tüketimi":[],
                "Yakıt Deposu":[],
                "Boya-değişen":[],
                "Takasa Uygun":[],
                "Kimden":[],
                "Fiyat":[]
                 }


        for i in range(1,51):
            if i==1:
                driver.get("https://www.arabam.com/ikinci-el/otomobil?take=50&view=List")
                sleep(3)
            else:
                driver.get(f"https://www.arabam.com/ikinci-el/otomobil?take=50&view=List&page={i}")
                sleep(3)

            car_links=driver.find_element(By.CLASS_NAME,'listing-table-wrapper')
            car_links=car_links.find_element(By.ID,'main-listing').find_element(By.TAG_NAME,'tbody')
            car_links=car_links.find_elements(By.TAG_NAME,'tr')
            car_links_list=[]
            for link in car_links:
               try: 
                    link=link.find_element(By.CLASS_NAME,'fade-out-content-wrapper').find_element(By.TAG_NAME,'a')
                    car_links_list.append(link.get_attribute('href'))
               except:
                  continue
            for link in car_links_list:
                driver.get(link)
                sleep(3)
                feautures=driver.find_element(By.CLASS_NAME,'product-detail-wrapper').find_element(By.CLASS_NAME,'product-properties-container').find_element(By.CLASS_NAME,'product-properties')
                price=feautures.find_element(By.CLASS_NAME,'product-properties-details-header').find_element(By.CLASS_NAME,'product-price').text
                others=feautures.find_elements(By.CLASS_NAME,'property-item')
                #Yakıt deposu ve Ort. Yakıt Tüketimi opsiyonel olduğundan her zaman olmuyor bu yüzden kontrol ettim ve olmadığı zaman nan yazdırdım
                fuel_tank_exists=False
                avg_fuel_exists=False
                for feauture in others:
                    try:
                        feauture_value=feauture.find_element(By.CLASS_NAME,'property-value').text
                        feauture_key=feauture.find_element(By.CLASS_NAME,'property-key').text.strip()
                        if feauture_key=="Yakıt Deposu":
                            fuel_tank_exists=True
                        elif feauture_key=="Ort. Yakıt Tüketimi":
                            avg_fuel_exists=True
                        data[feauture_key].append(feauture_value)
                    except:
                        continue
                if fuel_tank_exists==False:
                    data["Yakıt Deposu"].append(np.nan)
                if avg_fuel_exists==False:
                    data["Ort. Yakıt Tüketimi"].append(np.nan)

                data["Fiyat"].append(price)    
                
        
        df=pd.DataFrame(data) 


        df.to_csv("ilanlar.csv", index=False, encoding="utf-8-sig")
        print("bitti")
        driver.quit()
        
a=Cars()
input()