import csv
import json
import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options


##########################
# ФУНКЦИИ ДЛЯ СSV

def writeToCSV(data, path):
    """
    Запись в файл csv
    """
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for line in data:
            writer.writerow(line)
            
##########################
# ФУНКЦИИ ДЛЯ JSON
def convertTableToJson(rezult):
    """
    Перевод результата в json
    """
    rezult_dict = {}
    # Идем по списку организаций
    for num, item in enumerate(rezult):
        # Справочник организации
        table_dict = {}
        
        # Заполнение 
        table_dict["name"] = item[0][0]
        table_dict["data"] = {}
        
        mini_dict = {}
        # Заполнение по строкам
        for col_num, row in enumerate(item[1:]):
            mini_dict[str(col_num)] = {}
            # Заполнение по колонкам
            for row_num, item in enumerate(row):
                mini_dict[str(col_num)][str(row_num)] = item
        # Добавляем данные
        table_dict["data"] = mini_dict
        rezult_dict[str(num)] = table_dict
    
    return rezult_dict

def writeToJson(data, path):
    """
    Запись json в файл
    """
    with open(path, "w") as file:
        json.dump(data, file, ensure_ascii=False)
    
##########################
# Функции для парсинга           


def parseItem(browser, xpath):
    """
    Парсинг нужного поля с текстом на сайте
    """
    return browser.find_element_by_xpath(xpath)

def parseTable(browser, xpath):
    """
    Парсинг таблицы на странице
    """
    # Список с результатом
    rezult = []
    # Строка с результатом
    row_rezult = []
        
    # Счетчики
    col = 1
    row = 1
    bugs_limit = 3

    # Парсинг сайта
    while bugs_limit > 0:
        
        try:
            # Получаем инфу из нужного блока
            block_cell = parseItem(browser, xpath % (col, row))
            # Записываем результат
            row_rezult.append(block_cell.text)
            
            # Сдвигаемся по строке
            row += 1
            
            # Возвращаем счетчик багов
            bugs_limit = 3
        except NoSuchElementException:
            # Ловим ошибку о том, что колонки кончились и переходим на новую строку
            col += 1
            row = 1
            
            # Добавляем строку в таблицу
            rezult.append(row_rezult)
            row_rezult = []
            
            # Счетчик багов
            bugs_limit -= 1
        except Exception as exc:
            # Косяк другого типа
            print("!!!Что то не так!!!")
            print(exc)
            break

    return rezult

def removeWrongRows(rezult):
    """
    Удаление лишних строк
    """
    # Список для удаления
    remove_list = []
    # Убираем лишние строки
    for i, row in enumerate(rezult):
        if len(row) == 0:
            remove_list.append(i)
        elif len(row) == 1 and row[0] == "":
            remove_list.append(i)
    
    remove_list.reverse()
    # Удаление лишних строк
    for i in remove_list:
        _ = rezult.pop(i)
    
    return rezult
 
##########################
# КОД

def saveRezult(rezult, rezult_type, save_path):
    
    if rezult_type == "json":
        # Приводим к нужному виду
        rezult_dict = convertTableToJson(rezult)
        # Делаем json типом 
        #rezult_json = json.dumps(rezult_dict, ensure_ascii=False)   
        # Запись в файл
        writeToJson(rezult_dict, save_path + ".json")
    else:
        # Формируем из вложенности один список
        rezult = [el for item in rezult for el in item]
        # Запись в файл
        writeToCSV(rezult, save_path + ".csv")    
    
def takeDataElibrary(page_id = []):
    
    ##########################
    # ВВОД ДАННЫХ
    # Путь к драйверу (https://selenium-python.com/install-geckodriver)
    driver = os.getcwd()
    # Путь к нужной странице
    page_url = "https://elibrary.ru/org_profile.asp?id=%s"
    # xPath путь к нужному блоку с названием организации
    header_xpath = "/html/body/div[2]/table/tbody/tr/td/table[1]/tbody/tr/td[2]/form/table/tbody/tr[2]/td[1]/table[1]/tbody/tr/td/div/font[1]/b"
    # xPath путь к нужному блоку таблицы
    table_xpath = "/html/body/div[2]/table/tbody/tr/td/table[1]/tbody/tr/td[2]/form/table/tbody/tr[2]/td[1]/table[5]/tbody"
    table_row = "/tr[%s]/td[%s]"



    # Опция чтобы не открывать окно
    options = Options()
    options.add_argument('--headless')
    # Запускаем локальную сессию firefox
    browser = webdriver.Firefox(driver, options=options) 
    
    full_rezult = []
    
    for item in page_id:
        try:
            # Создаем адрес строки
            url = page_url % str(item)
            # Загружаем страницу
            browser.get(url)
            # Ждем подгрузку
            time.sleep(5)
            
            # Парсим нужную таблицу
            rezult = parseTable(browser, table_xpath + table_row)
            # Корректируем
            rezult = removeWrongRows(rezult)
            # Название организации
            header = parseItem(browser, header_xpath)
            # Добавляем наз. организации в начале списка
            rezult = [[header.text]] + rezult
            # Добавляем в результат
            full_rezult.append(rezult)
        except:
            print("!!!С %s не вышло!!!" % item)
    
    # Закрываем браузер
    browser.close()

    print("Закрытие браузера")
    # На всякий ждем пока закроется
    time.sleep(2)
    print("Усе")
    
    return full_rezult
