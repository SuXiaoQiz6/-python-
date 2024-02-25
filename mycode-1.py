# -*- encoding=utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import sys

class ExchangeRate:
    '''外汇汇率条目对象'''
    def __init__(self,name:str,price:float,stime:str) -> None:
        self.name = name
        self.price = price
        self.stime = stime

def main():
    #货币名称转换字典创建
    currency_dict = {}#key为英文缩写，value为对应的中文字符串
    driver = webdriver.Chrome()
    driver.get("https://www.11meigui.com/tools/currency")
    try:
        elements = driver.find_elements(By.CSS_SELECTOR,"#desc > table")
    except:
        print("货币名称转换元素爬取失败")
        return 0
    for element in elements:
        e = element.find_elements(By.CSS_SELECTOR,"tbody > tr")
        for i in range(2,len(e)):
            td = e[i].find_elements(By.TAG_NAME,"td")
            
            if td[4].text.strip() == "INR":
                currency_dict[td[4].text.strip()] = "印度卢比"
            else:
                currency_dict[td[4].text.strip()] = td[1].text.strip()
    driver.close()

    #转换输入参数查询格式
    input = sys.argv
    input_time = input[1]
    input_currency = input[2]
    currency_name = currency_dict[input_currency]
    search_time = input_time[:4]+"-"+input_time[4:6]+"-"+input_time[6:]
    
    #爬取对应汇率信息
    result = []#存储汇率信息
    f = open("result.txt","a")
    driver = webdriver.Chrome()
    driver.get("https://www.boc.cn/sourcedb/whpj/")

    try:
        paijia_selector = driver.find_element(By.CSS_SELECTOR,"#pjname")
        paijia_selector.click()
    except:
        print("货币类型选择错误")
        return 0
    select = Select(paijia_selector)
    select.select_by_value(currency_name)
    

    try:
        start_time_input = driver.find_element(By.CSS_SELECTOR,"#historysearchform > div > table > tbody > tr > td:nth-child(2) > div > input")
        start_time_input.clear()
        start_time_input.send_keys(search_time)
        start_time_input.click()
    except:
        print("开始时间设置失败")

    try:
        end_time_input = driver.find_element(By.CSS_SELECTOR,"#historysearchform > div > table > tbody > tr > td:nth-child(4) > div > input")
        end_time_input.clear()
        end_time_input.send_keys(search_time)
        end_time_input.click()
    except:
        print("结束时间设置失败")

    try:
        driver.find_element(By.CSS_SELECTOR,"#historysearchform > div > table > tbody > tr > td:nth-child(7) > input").click()
    except:
        print("汇率搜索失败")
    
    driver.implicitly_wait(10)

    #搜集根据时间货币搜索出的页面元素
    try:
        elements = driver.find_elements(By.CSS_SELECTOR,"body > div > div.BOC_main.publish > table > tbody > tr")
    except:
        print("查询搜索框搜索出来了，但元素未找到，或输入时间没有汇率条目，爬取失败")
        
    for i in range(0,len(elements)):
        f.write(elements[i].text)
        f.write("\n")
        if i > 0: 
            element = elements[i].find_elements(By.CSS_SELECTOR,"td")
            if len(element) >= 4: #防止空行
                e = ExchangeRate(element[0].text,element[3].text,input_time)
                result.append(e)
                
    #点击换页
    try:
        time_string = driver.find_element(By.CSS_SELECTOR,"#list_navigator > ol > li:nth-child(1)").text
        time_string = time_string.lstrip("共")
        time_string = time_string.rstrip("页")
        click_times = int(time_string)-1
    except:
        for r in result:
            if r.price != "":
                print(r.price)
                break
        else:
            print("该时间段该货币没有现汇卖出价")
        return 0
    
    for i in range(click_times):
        driver.find_element(By.CLASS_NAME,"turn_next").click()
        driver.implicitly_wait(10)
        try:
            elements = driver.find_elements(By.CSS_SELECTOR,"body > div > div.BOC_main.publish > table > tbody > tr")
        except:
            print("元素未找到，爬取失败")
        for i in range(1,len(elements)):
            f.write(elements[i].text)
            f.write("\n")
            element = elements[i].find_elements(By.CSS_SELECTOR,"td")
            if len(element) >= 4:
                e = ExchangeRate(element[0].text,element[3].text,input_time)
                result.append(e)
    f.close()
    driver.close()

    for r in result:
        if r.price != "":
            print(r.price)
            break
    else:
        print("该时间段该货币没有现汇卖出价")
    
if __name__ == '__main__':
    main()  
      


