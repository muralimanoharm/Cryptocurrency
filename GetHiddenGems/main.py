import json
import requests
from lxml import html
from collections import Counter
import sys
import time
import webbrowser

LikesCount = dict()
rank = 0
j = 0


def WriteDataToFile():
    with open("LikesCount.json", "w+") as file:
        file.seek(0)
        json.dump(LikesCount, file)


def GetLenghtOfTheFile():
    with open('LikesCount.json') as f:
        jsonpath1 = json.load(f)
        return len(jsonpath1)


def CopyTheExistingContentToFile():
    with open('LikesCount.json') as f:
        jsonpath = json.load(f)
        return jsonpath


def GetCoinDetails(name):
    return requests.get(
        'https://api.coingecko.com/api/v3/coins/' + name + '?localization=fasle&tickers=true&market_data=false&community_data=false&developer_data=false&sparkline=false')


def GetDetailsOfACoin(name):
    data1 = GetCoinDetails(name)
    if data1 is None or data1 == '' or data1.status_code is not requests.codes.ok:
        if data1.status_code is not requests.codes.ok:
            # print('Sleeping for 10 sec to reduce load')
            time.sleep(10)
            data1 = GetCoinDetails(name)
            if data1 is None or data1 == '' or data1.status_code is not requests.codes.ok:
                print('I got a null or empty string value :', name)
                return {}
            else:
                return data1.json()
    else:
        return data1.json()

def OpenURL(name):
    webbrowser.open('https://www.coingecko.com/en/coins/' + name)

def GetHiddenGems():
    for each in topCoins:
        #binance = False
        eachCoinDetails = GetDetailsOfACoin(each[0])
        eachrank = eachCoinDetails.get('market_cap_rank', -1)
        if eachrank is not None:
            if eachrank > 900:
                # for eachticker in eachCoinDetails['tickers']:
                #     if eachticker['market']['name'] == 'Binance':
                #         binance = True
                # if binance:
                print('Rank :', eachrank, ': name :', each[0], ': Likes :', each[1])
                OpenURL(each[0])


with open('response.json') as f:
    data = json.load(f)

print("Total :", len(data))
# Getting The Size of the File
size = GetLenghtOfTheFile()
print("Existing Size :", size)

for i in data:
    if size > 0:
        # print(size)
        j += 1
        size -= 1
        if size == 0:
            print("Skipped : ", GetLenghtOfTheFile())
            LikesCount = CopyTheExistingContentToFile()

    else:
        # iterate each website and find the views
        page = requests.get('https://www.coingecko.com/en/coins/' + i['id'])

        # Parsing the page
        tree = html.fromstring(page.content)

        # Get element using XPath
        likes = tree.xpath(
            '//div[@class="container "]/div/div[2]/span/text()')

        j += 1
        if len(likes) > 0:
            eachLikes = likes[0]
            eachLikesNum = eachLikes.split(" ", 1)

            # print(i['id'], (eachLikesNum[0]).replace(',', ''))
            sys.stdout.write("\rCompleted : %d" % j)
            sys.stdout.flush()
            LikesCount[i['id']] = int((eachLikesNum[0]).replace(',', ''))
            WriteDataToFile()
        else:
            print("Error :", i['id'])

c = Counter(LikesCount)
topCoins = c.most_common(275)

with open("OrderedLikesCount.json", "w+") as file:
    file.seek(0)
    json.dump(topCoins, file)
print('\n')
GetHiddenGems()
