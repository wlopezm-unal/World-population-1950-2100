from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import os

def start_browser(downloadpath, mozilla_bin):

    options = Options()
    options.headless = False
    options.set_preference("browser.download.folderList",2)  
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", downloadpath)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/force-download, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet ,\
                                                                        application/octet-stream doc xls pdf txt,\
                                                                        text/csv,application/x-msexcel,\
                                                                        application/excel,application/x-excel,\
                                                                        application/vnd.ms-excel,\
                                                                        image/png,image/jpeg,text/html,text/plain,text/csv,\
                                                                        application/msword,application/xml,\
                                                                        application/x-www-form-urlencoded,\
                                                                        application/csv,\
                                                                        text/tab-separated-values,\
                                                                        application/ms-excel')
    options.set_preference("browser.helperApps.neverAsk.openFile", 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet ,\
                                                                        application/octet-stream doc xls pdf txt,\
                                                                        text/csv,application/x-msexcel,\
                                                                        application/excel,application/x-excel,\
                                                                        application/vnd.ms-excel,\
                                                                        image/png,image/jpeg,text/html,text/plain,text/csv,\
                                                                        application/msword,application/xml,\
                                                                        application/x-www-form-urlencoded,\
                                                                        application/csv,\
                                                                        text/tab-separated-values, \
                                                                        application/ms-excel')
    options.set_preference("browser.helperApps.alwaysAsk.force", False)
    options.set_preference("browser.download.manager.useWindow", False)
    options.set_preference("browser.download.manager.focusWhenStarting", False)
    options.set_preference("browser.download.manager.showAlertOnComplete", False)
    options.set_preference("browser.download.manager.closeWhenDone", True)
    options.set_preference("browser.cache.disk.enable", False)
    options.set_preference("browser.cache.memory.enable", False)
    options.set_preference("browser.cache.offline.enable", False)
    options.set_preference("network.http.use-cache", False)

   
    
    options.set_preference("browser.download.manager.showWhenFinished", False)
    options.set_preference("browser.helperApps.neverAsk.openFile", "image/png")
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.manager.useWindow", False)


    options.binary_location = mozilla_bin
    browser = webdriver.Firefox(executable_path = os.path.join(os.path.dirname(__file__), 'geckodriver.exe'),
                                options=options)
    return browser                                  