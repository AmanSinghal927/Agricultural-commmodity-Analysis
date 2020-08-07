from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import os
from state_map import state_map
from os import path

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
                            for t in range(3):
                                fileName = "mynewdata"+"_"+str(year)+"_"+str(month)+".csv"
                                filePath = folderPath + "/" + fileName
                                print('file to open',filePath)
                                if path.exists(filePath):
                                    print(filePath + " Exist")
                                    break
                                print(fileName,end =" ")
                                try:
                                    driver = webdriver.Chrome(chrome_location, chrome_options=chrome_options)
                                    driver.get('http://agmarknet.gov.in/PriceAndArrivals/DatewiseCommodityReport.aspx')
                                    print('0',end=" ")

                                    driver.find_element_by_xpath("//*[@id=\"cphBody_cboYear\"]/option[contains(text(),\""+str(year)+"\")]").click()
                                    driver.implicitly_wait(400)
                                    print('1',end=" ")
                                    for k in range(5):
                                        try:
                                            driver.find_element_by_xpath("//*[@id=\"cphBody_cboMonth\"]/option[contains(text(),\""+str(month)+"\")]").click()
                                            driver.implicitly_wait(400)
                                            break
                                        except (StaleElementReferenceException) as x:
                                            k+=1
                                    print('2',end=" ")
                                    for k in range(5):
                                        try:
                                            driver.find_element_by_xpath("//*[@id=\"cphBody_cboState\"]/option[contains(text(),\""+str(centre)+"\")]").click()
                                            driver.implicitly_wait(400)
                                            break
                                        except (StaleElementReferenceException) as x:
                                            k+=1
                                    print('3',end=" ")
                                    for k in range(5):
                                        try:
                                            driver.find_element_by_xpath("//*[@id=\"cphBody_cboCommodity\"]/option[contains(text(),\""+str(commodity)+"\")]").click()
                                            driver.implicitly_wait(400)
                                            break
                                        except (StaleElementReferenceException) as x:
                                            k+=1
                                    print('downloading data',end =' ')

                                    driver.find_element_by_xpath("//*[@id=\"cphBody_btnSubmit\"]").click()
                                    table = driver.find_element_by_xpath("//*[@id=\"cphBody_gridRecords\"]")
                                    rows = table.find_elements_by_tag_name("tr")
                                    st = ''
                                    count=0
                                    for row in rows:
                                        cells = row.find_elements_by_xpath(".//*[local-name(.)='th' or local-name(.)='td']")
                                        #print(cells)
                                        for cell in cells:
                                            #print(cell.text)
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
                                    driver.close()
                                    print("Exception")
                                    continue


commodity = "Cauliflower"
start_year = 2016
end_year = 2020
centres = state_map[commodity]
months =['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

downloadWholesaleData(commodity,centres,start_year,end_year,months)
