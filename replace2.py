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
# FileNameInput = "input.txt"
# FileNameOutput имя результирующего файла
FileNameOutput = "output.txt"
replacements = {'"Hello World"' : 'Hello World', 'world' : 'World',  'hello' : 'Hello'}

f =open(FileNameInput).read()
newText = f
for i in replacements.keys():
    newText = newText.replace(i, replacements[i])
    print(i, replacements[i])


with open(FileNameOutput, "w") as f:
    f.write(newText)
f.close()