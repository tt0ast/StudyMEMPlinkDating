# Parse CSV data of plink study

import os
import csv

# paths

csvSourcePath = ''
parsedDataSavePath = ''

# Functions

# Find the start of the main listening task and return it's index
def findMainTaskIndex(csvPath):

    index = 0

    with open(csvPath, newline='') as csvfile:
    
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')

            for row in reader:   
                if (row['trial_type'] == 'call-function'):
                    index += 1
                    if index == 2:
                        return row['trial_index']

# Format the GoldsmithMSI data to be analyzed by the online scoring tool
def sanitizeGoldsmithMSI(data, keys):

    dataDict = dict.fromkeys(keys)

    for key in keys:

        keyIndex = data.find(key)
        answerNumberPosition = data.find(':', keyIndex)

        dataDict[key] = data[answerNumberPosition + 2]

    return dataDict        
                               
# Main

parsedDataKeys = ['runID', 'yearOfBirth', 'countryGrewUp', 'goldsmithMSI', 'stimuliOrder', 'BlueOrchid', 'BORecognition', 
                  'GoldOnTheCeiling', 'GOTCRecognition', 'GoodTimesBadTimes', 'GTBTRecognition', 'Bitch', 'BRecognition', 
                  'SaveYourTears', 'SYTRecognition', '87Stingray', '87SRecognition', 'ThatWasYesterday', 'TWYRecognition', 
                  'CryWolf', 'CWRecognition', 'Touch', 'TRecognition', 'TakeBackTheNight', 'TBTNRecognition',
                  'YouShouldBeDancing', 'YSBDRecognition', 'Fantasy', 'FRecognition','TearsDryOnTheirOwn', 'TDOTORecognition',
                  'TroubleSleeping', 'TSRecognition', 'HoneyLove', 'HLRecognition', 'ICantSeeMyselfLeavingYou', 'ICSMLYRecognition']

songNameKeys = ['BlueOrchid', 'GoldOnTheCeiling', 'GoodTimesBadTimes', 'Bitch', 'SaveYourTears', '87Stingray', 'ThatWasYesterday', 
                'CryWolf', 'Touch', 'TakeBackTheNight', 'YouShouldBeDancing', 'Fantasy', 'TearsDryOnTheirOwn', 'TroubleSleeping', 
                'HoneyLove', 'ICantSeeMyselfLeavingYou']

goldsmithKeys = ['AE_01', 'AE_02', 'MT_03', 'MT_06', 'PA_04', 'PA_08', 'SA_01', 'SA_02', 'SA_03', 'SA_04', 'SA_05', 'SA_06']

outputDict = []

goldsmithDict = []

# Open all CSV files from the given folder
for file in os.listdir(csvSourcePath):
     
    filename = os.fsdecode(file)

    if filename.endswith(".csv"): 

        # Open the specific CSV file
        with open(csvSourcePath + filename, newline='') as csvfile:

            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            dictParsedRow = dict.fromkeys(parsedDataKeys)

            ofset = int(findMainTaskIndex(csvSourcePath + filename))

            wasLastRowMusic = False
            songNameIndex = 0

            # Parse each row
            for row in reader:

                # Parse the personal data
                if row['trial_index'] == '2':
                    dictParsedRow['runID'] = row['run_id']
                    answerString = row['response']
                    dictParsedRow['yearOfBirth'] = answerString[answerString.find('h":') + 3:answerString.find(',"P')]
                    dictParsedRow['countryGrewUp'] = answerString[answerString.find('Q1":"') + 5:answerString.find('"}')]

                # Get and parse the GoldsmithMSI data
                elif row['trial_index'] == '3':
                    goldsmithData = (sanitizeGoldsmithMSI(row['response'], goldsmithKeys))
                    goldsmithData['uid'] = row['run_id']
                    goldsmithDict.append(goldsmithData)
                
                # Parse the listening task answers
                elif (int(row['trial_index']) >= ofset):

                    # Get the dating answers
                    if row['trial_type'] == 'audio-slider-response':   
                        for index, songName in enumerate(songNameKeys):
                            if row['stimulus'].find(songName) > -1:
                                dictParsedRow[songName] = row['response']
                                wasLastRowMusic = True
                                songNameIndex = (index * 2) + 5
                    
                    # Get the recognition answers
                    elif row['trial_type'] == 'html-button-response':
                        if wasLastRowMusic:
                            dictParsedRow[parsedDataKeys[songNameIndex + 1]] = row['response']
                            wasLastRowMusic = False

            outputDict.append(dictParsedRow)

goldsmithParsedKeys = ['uid', 'AE_01', 'AE_02', 'MT_03', 'MT_06', 'PA_04', 'PA_08', 'SA_01', 'SA_02', 'SA_03', 'SA_04', 'SA_05', 'SA_06']            

# Save the GoldsmithMSI answers for online analysis
with open(parsedDataSavePath + 'GoldsmithMSIAnswers.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=goldsmithParsedKeys, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(goldsmithDict)

# Save the parsed data as a CSV file
with open(parsedDataSavePath + 'PlinkStudyParsedData.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=parsedDataKeys, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(outputDict)