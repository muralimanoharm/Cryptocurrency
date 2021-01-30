import json
import requests
from lxml import html
from collections import Counter
import sys

LikesCount = dict()


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

with open('response.json') as f:
    data = json.load(f)

print("Total :", len(data))
#Getting The Size of the File
size = GetLenghtOfTheFile()
print("Existing Size :", size)
j = 0
for i in data:
    if size > 0:
        #print(size)
        j += 1
        size -=1
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

            #print(i['id'], (eachLikesNum[0]).replace(',', ''))
            sys.stdout.write("\rCompleted : %d" % j)
            sys.stdout.flush()
            LikesCount[i['id']] = int((eachLikesNum[0]).replace(',', ''))
            WriteDataToFile()
        else:
            print("Error :", i['id'])

c = Counter(LikesCount)
topCoins = c.most_common(len(LikesCount))

with open("OrderedLikesCount.json", "w+") as file:
    file.seek(0)
    json.dump(topCoins, file)
