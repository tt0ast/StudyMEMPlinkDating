import os
from pydub import AudioSegment
from pydub import effects


# cut the audio segment and fade it in and out

def processSnippet(audioSegment, plinkLength, fadeTime):
    
    plinkUncut = audioSegment
    plink = plinkUncut[:plinkLength].fade_in(fadeTime).fade_out(fadeTime)

    return plink

# normalize the audio segment

def normalizeSnippet(audioSegemnt, headroom):
    
    return effects.normalize(audioSegemnt, headroom)

## MAIN:

# settings for stimuli

stimuliLength = 300
fadeTime = 2
normalizationHeadroom = 0.5

# paths for data

audioSourcePath = ""
stimuliPath = ""

# go through all files in the audioSourcePath, edit them and store them in the stimuliPath

sourceDirPath = os.fsencode(audioSourcePath)

for file in os.listdir(sourceDirPath):
     
     filename = os.fsdecode(file)

     if filename.endswith(".wav"): 
            
        stim = AudioSegment.from_wav(audioSourcePath + '\\' + filename)

        # Report if a rough cut stimuli is to short

        if len(stim) < stimuliLength:

            print('Error: ' + filename + ' is shorter than specified stimuli length!')   

        stim = processSnippet(stim, stimuliLength, fadeTime)
        stim = normalizeSnippet(stim, normalizationHeadroom)

        stim.export(stimuliPath + '\\' + filename, format="wav")

# Success :) !!

print("All Stimuli Processed")







