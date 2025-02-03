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

        def ensure_all_columns(data):
            max_length = max(len(v) for v in data.values())
            for key in data:
                if len(data[key]) < max_length:
                    data[key].append(np.nan)
     
        
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
            print("Sayfa",i,"\n")
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
                sleep(1)
                feautures=driver.find_element(By.CLASS_NAME,'product-detail-wrapper').find_element(By.CLASS_NAME,'product-properties-container').find_element(By.CLASS_NAME,'product-properties')
                price=feautures.find_element(By.CLASS_NAME,'product-properties-details-header').find_element(By.CLASS_NAME,'product-price').text
                others=feautures.find_elements(By.CLASS_NAME,'property-item')
                
                for feauture in others:
                    try:
                        feauture_value=feauture.find_element(By.CLASS_NAME,'property-value').text
                        feauture_key=feauture.find_element(By.CLASS_NAME,'property-key').text.strip()
                        data[feauture_key].append(feauture_value)
                    except:
                        continue
                    
                

                data["Fiyat"].append(price)   
                ensure_all_columns(data)
                
                
             
                
        
        df=pd.DataFrame(data) 


        df.to_csv("ilanlar.csv",mode='a', index=False, header=False)
        print("bitti")
        driver.quit()
        
a=Cars()
input()