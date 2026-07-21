import csv
import json

import pandas as pd
import matplotlib.pyplot as plt




# Зчитування даних
sales = []

with open("global_sales.csv", "r", encoding="utf-8") as file:
    reader= csv.DictReader(file)

    for row in reader:
        sales.append(row)




with open("regional_tariffs.json", "r", encoding="utf-8") as file:
    tariffs =json.load(file)



# Clean
for sale in sales:

    if sale["quantity"] == "N/A":
        sale["quantity"]= 0
    else:
        sale["quantity"]=int(sale["quantity"])

    if sale["revenue"]== "N/A":
        sale["revenue"]=0
    else:
        sale["revenue"]=float(sale["revenue"])


for region in tariffs:

    if tariffs[region] == "N/A":
        tariffs[region] =0
    else:
        tariffs[region] =float(tariffs[region])





for sale in sales:
    region=sale["region"]
    tariff=tariffs[region]

    sale["net_profit"] = sale["revenue"]-(sale["revenue"] *(tariff / 100))



# Запис у ссв
with open("cleaned_sales_updated.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames =sales[0].keys()
    writer =csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(sales)


# Прибуток категорії
category_profit = {}
for sale in sales:

    category=sale["product_category"]
    profit = sale["net_profit"]

    if category not in category_profit:
        category_profit[category] = 0

    category_profit[category] += profit




average_profit = sum(category_profit.values()) / len(category_profit)




# Словник топ категорій
top_categories = {
    category: profit
    for category, profit in category_profit.items()
    if profit > average_profit
}



# Фільтрація
top_categories = dict(sorted(top_categories.items(),key=lambda item: item[1],reverse=True))




with open("top_categories.json", "w", encoding="utf-8") as file:
    json.dump(top_categories, file,)



# Створюємо датафрейм
df = pd.DataFrame(
    list(top_categories.items()),
    columns=["Category", "Net Profit"]
)

print(df)


plt.figure(figsize=(6, 5))

plt.bar(df["Category"], df["Net Profit"])

plt.title("Top Product Categories")
plt.xlabel("Category")
plt.ylabel("Net Profit")

plt.show()