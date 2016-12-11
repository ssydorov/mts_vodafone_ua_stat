#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 22:35:34 2016

@author: Sergiy Sydorov
"""
import re

#
# company_code - лицевой счет по которому обрабатывается выписка
company_code = "295380282427"
# month - месяц выписки
month = 12
if month == 1:
    month_real = 12
else:
    month_real = month - 1
# year - год выписки
year = 2016
if month == 1:
    year_real = year - 1
else:
    year_real = year

# FileNameInput имя входного файла
FileNameInput = "invoice_" + company_code + "_" + str(year) + "_" + str(month) + ".csv"
# FileNameInput = "input.txt"
# FileNameOutput имя результирующего файла
FileNameOutput = "invoice_" + company_code + "_" + str(year_real) + "_" + str(month_real) + ".txt"
# FileNameOutput = "output.txt"
# словарь словосочетаний нуждающихся в замене для коррекной работы парсера
replacements = {'"Вихідні дзвінки, SMS, передача даних"': 'Вихідні дзвінки, SMS, передача даних',
                '"ПОСЛУГИ, НАДАНІ ЗА МЕЖАМИ ПАКЕТА:"': 'ПОСЛУГИ, НАДАНІ ЗА МЕЖАМИ ПАКЕТА:',
                '"КОНТЕНТ-ПОСЛУГИ:"': 'КОНТЕНТ-ПОСЛУГИ:', '"НАДАНІ КОНТЕНТ-ПОСЛУГИ:"': 'НАДАНІ КОНТЕНТ-ПОСЛУГИ:',
                'GSM Просто Супер': '"GSM Просто Супер"'}
# чтение исходного файла
f = open(FileNameInput).read()
newText = f
# замена словосочетаний
for i in replacements.keys():
    newText = newText.replace(i, replacements[i])

# запись файла
with open(FileNameOutput, "w") as f:
    f.write(newText)
f.close()

# открытие файла для парсинга
file_input = FileNameOutput
file_output = "invoice_" + company_code + "_" + str(year) + "_" + str(month_real) + "_out.txt"
file_detail = "invoice_" + company_code + "_" + str(year_real) + "_" + str(month_real) + "_detail.txt"
fi = open(file_input, 'r')
fo = open(file_output, 'w')
fd = open(file_detail, 'w')

# запись шапки
fo.write(
    "год;месяц;контракт;тарифный план;стоимость пакета;сверх пакета;контент;заказ услуг;роуминг;спец "
    "услуги;скидки;итого" + '\n')
fd.write('год,месяц,контракт,,,,,услуга,оператор,номер,дата,время,длительность/объём,,стоимость' + '\n')
# парсинг файла
kontrakt = ''
tarif = ''
paket = ''
over_paket = ''
skidki = ''
itogo = ''
contract = 0
i = 0
j = 0
line2 = []
line = fi.readline()
while line:
    result = re.findall(r'^\w+', line)
    i = 0
    kontrakt = ''
    tarif = ''
    paket = ''
    over_paket = ''
    content = ''
    zakaz = ''
    rouming = ''
    spicial = ''
    skidki = ''
    itogo = ''
    if len(result) > 0 and result[0] == 'Контракт':
        contract = 1
        result2 = re.findall(r'(?:\d*\.)?\d+', line)
        kontrakt = result2[0]
        line = fi.readline()
        result = re.findall(r'^\w+', line)
        if len(result) > 0 and result[0] == 'Тарифний':
            result5 = re.findall(r'([^"]+)', line)
            tarif = str(result5[1])
        line = fi.readline()
        result = re.findall(r'^\w+', line)
        if len(result) > 0 and result[0] == 'ВАРТІСТЬ':
            result5 = re.findall(r'(?:\d*\.)?\d+', line)
            paket = str(result5[2])
        while len(result) > 0 and result[0] != 'ЗАГАЛОМ':
            line = fi.readline()
            result = re.findall(r'^\w+', line)
            if len(result) > 0 and result[0] == 'ПОСЛУГИ':
                result2 = re.findall(r'\S+', line)
                if result2[1] == 'НАДАНІ':
                    result4 = re.findall(r'(?:\d*\.)?\d+', line)
                    over_paket = str(result4[0])
                if result2[1] == 'МІЖНАРОДНОГО':
                    result4 = re.findall(r'(?:\d*\.)?\d+', line)
                    rouming = str(result4[0])
            elif len(result) > 0 and result[0] == 'ЗНИЖКИ':
                result4 = re.findall(r'\-?\d+\.?\d*', line)
                skidki = str(result4[0])
            elif len(result) > 0 and result[0] == 'КОНТЕНТ':
                result4 = re.findall(r'\-?\d+\.?\d*', line)
                content = str(result4[0])
            elif len(result) > 0 and result[0] == 'ЗАМОВЛЕНІ':
                result4 = re.findall(r'(?:\d*\.)?\d+', line)
                zakaz = str(result4[2])
            elif len(result) > 0 and result[0] == 'СПЕЦІАЛЬНІ':
                result4 = re.findall(r'(?:\d*\.)?\d+', line)
                spicial = str(result4[0])
            i += 1
        if len(result) > 0 and result[0] == 'ЗАГАЛОМ' and contract == 1:
            result4 = re.findall(r'(?:\d*\.)?\d+', line)
            itogo = str(result4[0])
            contract = 0
            line2.append(line)
            line = fi.readline()
    if i != 0:
        # запись общей статистики (с заменой . на , для экселя)
        fo.write(
            '{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11}\n'.format(year_real, month_real, kontrakt, tarif,
                                                                         paket.replace('.', ','),
                                                                         over_paket.replace('.', ','),
                                                                         content.replace('.', ','),
                                                                         zakaz.replace('.', ','),
                                                                         rouming.replace('.', ','),
                                                                         spicial.replace('.', ','),
                                                                         skidki.replace('.', ','),
                                                                         itogo).replace('.', ','))
        kontrakt2 = kontrakt
    line = fi.readline()
    if len(line) > 2:
        if line[0] == ',' and line[1] == ',':
            # запись детализации
            fd.write(str(year_real) + ',' + str(month_real) + ',' + kontrakt2 + ',')
            fd.write(line)
fi.close()
fo.close()
fd.close()
