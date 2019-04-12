import random
import urllib.request
import json

def nearbyUrl(lat, long):
    return "https://mps-stg.mxdata.co.uk/request/execute?cid=bustimesuk:1&rid=nearby&p=lat:" + str(lat) + ";long:" + str(long) + ';radius:500.000000'

def checkStopJson(url, stopJson):
    stopsArray = stopJson['msptl_response']['server_response']['search_results']
    for stop in stopsArray:
        
        indicator = stop['payload'].get('indicator', "15")
        if indicator not in indicatorDict and not indicator.split(' ')[-1].isdigit():
            indicatorDict[indicator] = url

def getRidOfRedundantIndicators(indicatorDict):
    notSavedIndicators = ''
    newIndicatorDict = {}
    for indicator in indicatorDict:
        url = indicatorDict[indicator]
        if len(indicator.split(' ')) == 2 and len(indicator.split(' ')[-1]) <= 2:
            newIndicatorDict[indicator.split(' ')[1]] = url
            notSavedIndicators += indicator + ', '
            notSavedIndicatorDict[indicator] = url
        else:
            newIndicatorDict[indicator] = url
    indicatorDict = newIndicatorDict
    return notSavedIndicators

notSavedIndicators = ''
indicatorDict = {}
notSavedIndicatorDict = {}
for i in range(0, 10):
    randomLong = random.uniform(-10.8544921875, 2.021484375)
    randomLat = random.uniform(49.82380908513249, 59.478568831926395)
    url = nearbyUrl(randomLat, randomLong)
    content = urllib.request.urlopen(url).read()
    stopJson = json.loads(content)
    checkStopJson(url, stopJson)
    notSavedIndicators = getRidOfRedundantIndicators(indicatorDict)
    print(i)

reversedIndicatorDict = {}
for key in indicatorDict:
    if indicatorDict[key] not in reversedIndicatorDict:
        reversedIndicatorDict[indicatorDict[key]] = key
    else:
        reversedIndicatorDict[indicatorDict[key]] += ', ' + key

stringToSave = ''
for key in reversedIndicatorDict:
    stringToSave += '[' + reversedIndicatorDict[key] + '|' + key + '], '
print("SAVED:\n" + stringToSave)
print('\n\n\n\nNOT SAVED:' + notSavedIndicators)


notSavedIndicatorsDict = ''
for key in notSavedIndicatorDict:
    notSavedIndicatorsDict += notSavedIndicatorDict[key] + ' : ' + key + '\n'

with open('correct.txt', 'w') as file:
    file.write(stringToSave)

with open('notSaved.txt', 'w') as file:
    file.write(notSavedIndicators)

with open('notSavedDict.txt', 'w') as file:
    file.write(notSavedIndicatorsDict)