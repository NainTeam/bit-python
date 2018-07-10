import json

import pandas as pd
pd.set_option('precision', 2)

import requests
import time

intereses = ['bitcoin', 'iota', 'ethereum', 'litecoin', 'ripple']
column_names = ['name','price_eur', 'percent_change_24h', 'percent_change_7d']

def formatData(df, column_names = ['name','price_eur', 'percent_change_24h', 'percent_change_7d']):
    text = ''
    for index, row in df.iterrows():
        for i in column_names:
            print(i)
            text = text+str(row[i])+' '
        text = text + '\n'
    print(text)

def sendSlackData(df):
    webhook_url = 'https://hooks.slack.com/services/hook'
    slack_data = {'text': df.to_string(index  = False, col_space  = 15)+'\n\n'}
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        print("Error sending data")
    else:
        print("Data sent")
        
api = 'https://api.coinmarketcap.com/v1/ticker?convert=EUR&limit=10?'        
def sendPrices():
    import requests
    r = requests.get(api)
    if r.status_code != 200:
        print("No available data")
    df = pd.read_json(r.text)
    df = df[df.id.isin(intereses)]
    df = df[column_names]
    sendSlackData(df)
    
sendPrices()
