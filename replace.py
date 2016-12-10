#!/usr/bin/python
#
# company_code - лицевой счет по которому обрабатывается выписка
company_code = "295380282427"
# year - год выписки
year = "2016"
# month - месяц выписки
month = "09"
# FileNameInput имя входного файла
FileNameInput = "invoice_" + company_code + "_" + year + "_" + month + ".txt"
FileNameInput = "input.txt"
# FileNameOutput имя результирующего файла
FileNameOutput = "output.txt"

replace_string1= '"Hello World"'
replace_string2= 'Hello World'


with open(FileNameInput) as f:
    newText = f.read().replace(replace_string1, replace_string2)

with open(FileNameOutput, "w") as f:
    f.write(newText)
f.close()