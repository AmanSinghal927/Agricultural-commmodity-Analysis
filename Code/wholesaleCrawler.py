from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import os
from state_map import state_map
from os import path
from selenium.common.exceptions import TimeoutException


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

chrome_location = '/home/gem/Nishant/chromedriver'

def downloadWholesaleData(commodity,centres,start_year,end_year,months):
        rootfolder = 'folders/'+str(commodity)
        if not os.path.exists(rootfolder):
                print(rootfolder,' does not exist')
                os.makedirs(rootfolder)
        else:
                print(rootfolder,' exists')
        for centre in centres:
                folderPath = rootfolder+'/'+str(centre)
                if not os.path.exists(folderPath):
                        print(folderPath,' not exists')
                        os.makedirs(folderPath)
                else:
                        print(folderPath,' exists')
                print(centre, commodity)
                for year in range(start_year,end_year+1):
                        for month in months:
                                print(year,month,centre,commodity)
                                fileName = "mynewdata"+"_"+str(year)+"_"+str(month)+".csv"
                                filePath = folderPath + "/" + fileName
                                print('file to open',filePath)
                                print(path.exists(filePath))
                                if path.exists(filePath):
                                    print(filePath, " Exist")
                                    continue
                                print("After")
                                #print("TRYING TO DOWNLOAD THIS FILE",fileName, end =" ")                                
                                driver = webdriver.Chrome(chrome_options=chrome_options)
                                for t in range(3):
                                        try:
                                                print("inside try, t=", t)
                                                try_left = 3
                                                driver.set_page_load_timeout(10)
                                                while True:
                                                        try:
                                                            print("driver.get")
                                                            driver.get("https://agmarknet.gov.in/PriceAndArrivals/DatewiseCommodityReport.aspx")
                                                            break
                                                        except TimeoutException:
                                                            print("Timeout exveption")
                                                            try_left-=1
                                                            driver.execute_script("window.stop();")
                                                            if try_left<=0:
                                                                print("Timeout loading url")
                                                                break

                                                driver.set_page_load_timeout(600)
                                                #driver.get('http://agmarknet.gov.in/PriceAndArrivals/DatewiseCommodityReport.aspx')
                                                print('YEAR', end=" ")
                                                driver.find_element_by_xpath("//*[@id=\"cphBody_cboYear\"]/option[contains(text(),\""+str(year)+"\")]").click()
                                                driver.implicitly_wait(400)
                                                print('MONTH', end=" ")
                                                flag = False
                                                for k in range(5):
                                                        try:
                                                            driver.find_element_by_xpath("//*[@id=\"cphBody_cboMonth\"]/option[contains(text(),\""+str(month)+"\")]").click()
                                                            driver.implicitly_wait(400)
                                                            flag = True
                                                            break
                                                        except (StaleElementReferenceException) as x:
                                                            k+=1
                                                if(not flag):
                                                        continue
                                                print('STATE', end=" ")
                                                flag = False
                                                for k in range(5):
                                                        try:
                                                                driver.find_element_by_xpath("//*[@id=\"cphBody_cboState\"]/option[contains(text(),\""+str(centre)+"\")]").click()
                                                                driver.implicitly_wait(400)
                                                                flag = True
                                                                break
                                                        except (StaleElementReferenceException) as x:
                                                                k+=1
                                                if(not flag):
                                                        continue
                                                print('COMMODITY', end=" ")
                                                flag = False
                                                for k in range(5):
                                                        try:
                                                            driver.find_element_by_xpath("//*[@id=\"cphBody_cboCommodity\"]/option[contains(text(),\""+str(commodity)+"\")]").click()
                                                            driver.implicitly_wait(400)
                                                            flag = True
                                                            break
                                                        except (StaleElementReferenceException) as x:
                                                            k+=1
                                                if(not flag):
                                                        continue
                                                print('downloading data', end =' ')
                                                driver.find_element_by_xpath("//*[@id=\"cphBody_btnSubmit\"]").click()
                                                table = driver.find_element_by_xpath("//*[@id=\"cphBody_gridRecords\"]")
                                                rows = table.find_elements_by_tag_name("tr")
                                                st = ''
                                                count=0
                                                for row in rows:
                                                        cells = row.find_elements_by_xpath(".//*[local-name(.)='th' or local-name(.)='td']")
                                                        for cell in cells:
                                                            st += cell.text+','
                                                        st+='\n'
                                                myfile= open(filePath,'a')
                                                myfile.write(st)
                                                myfile.close()
                                                print("saved")
                                                print(month+ "completed", end=" ")
                                                driver.close()
                                                break
                                        except(NoSuchElementException,StaleElementReferenceException) as e:
                                                print("Exception")
                                                continue
                                try:
                                        driver.close()
                                except:
                                        print('BROWSER ALREADY CLOSED')

commodity = "Rice"
start_year = 2016
end_year = 2019
centres = state_map[commodity]

