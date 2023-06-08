import requests
import json
import pandas as pd
import boto3
import matplotlib.pyplot as plt


url_usd = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=usd&sort=exchangedate&order=desc&json"
url_eur = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=eur&sort=exchangedate&order=desc&json"
usd = requests.get(url_usd)
eu = requests.get(url_eur)
data_us = usd.json()
data_eu = eu.json()

usd = []
eur = []
for i in data_us:
    usd.append({'exchangedate': i[ 'exchangedate'], 'rate_usd':i['rate']})
for i in data_eu:
    eur.append({'exchangedate': i[ 'exchangedate'], 'rate_eur':i['rate']})

usd_df = pd.DataFrame(usd).set_index('exchangedate')
eur_df = pd.DataFrame(eur).set_index('exchangedate')
data = pd.concat([usd_df, eur_df], axis=1)
data.to_csv('rates_2021.csv')

s3 = boto3.client('s3')
s3.upload_file('rates_uah_2021.csv', 'cloudlab-bucket', 'rates_uah_2021.csv')

s3.download_file('art-bucket', 'rates_2021.csv', 'rates_2021.csv')
df = pd.read_csv('rates_2021.csv')
df.plot(x='exchangedate', y=['rate_usd', 'rate_eur'], rot=45, title='rates 2021')
plt.savefig('graph.png')
s3.upload_file('graph.png', 'art-bucket', 'grahp.png')
