from bs4 import BeautifulSoup
import seaborn as sns
import requests
import pandas as pd
import matplotlib.pyplot as plt

with open('request.htm', 'w') as file:
	page = requests.get("https://www.pro-football-reference.com/players/P/PeteAd01.htm")
	file.write(page.text)

with open('request.htm') as file:
    page = file.read()

    soup = BeautifulSoup(page, 'html.parser')
    # print(soup.find_all(id="switcher_rushing_and_receiving"))

    table_container = soup.find(id="switcher_rushing_and_receiving")
    table = table_container.find('table')

    header = table.find('thead').contents[3].find_all('th')
    rows = table.find('tbody').find_all('tr')

    labels = []
    for label in header:
        if label.text in ['Yds', 'TD', 'Lng', 'Y/G', '1D']:
            if 'rush_{}'.format(label.text) not in labels:
                labels.append('rush_{}'.format(label.text))
                continue
            else:
                labels.append('rec_{}'.format(label.text))
                continue
        else:
            labels.append(label.text)

    data = {}
    for label in labels:
        data[label] = []

    for i, row in enumerate(rows):
        for j, item in enumerate(row.contents):
            data[labels[j]].append(item.text)

    # for key in data:
    #     print(len(data[key]))
    #     if len(data[key]) == 8:
    #         print(data[key])
    df = pd.DataFrame(data).convert_dtypes()
    df['rush_Yds'] = pd.to_numeric(df['rush_Yds'])
    print(df['rush_Yds'])
    sns.barplot(data=df, x='Year', y='rush_Yds')
    plt.savefig('test.png')
