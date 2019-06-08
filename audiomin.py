#!/usr/bin/python3

from pydub import AudioSegment
import sys
import wave as wav
import math
import struct
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import os
import csvLogger


def getFileInfo(filename):

    audiofile = wav.open(filename, 'rb')
    channels = audiofile.getnchannels()
    width = audiofile.getsampwidth()
    rate = audiofile.getframerate()
    frames = audiofile.getnframes()
    frame_width = width * channels
    audiofile.close()

    info = [channels, width, rate, frames, frame_width]
    return info

def getAudioSamples(filename):

    wavfile = wav.open(filename, 'rb')
    channels = wavfile.getnchannels()
    width = wavfile.getsampwidth()
    rate = wavfile.getframerate()
    frames = wavfile.getnframes()
    frame_width = width * channels
    

    wave_bytes = wavfile.readframes(frames)
    samples = []
    # Iterate over frames.
    for f in range(0, len(wave_bytes), frame_width):
        frame = wave_bytes[f : f + frame_width]
        # Iterate over channels.
        for c in range(0, len(frame), width):
            sample_bytes = frame[c : c + width]
            sample = int.from_bytes(sample_bytes,
                                    byteorder='little',
                                    signed=(width>1))
            samples.append(sample)

    wavfile.close()
    return samples

def amplify(filename, amount):
    
    folder = filename[:len(filename)-4]
    #print(folder)
    if os.path.isdir(folder) == False:
        print('Error: cannot amplify the file without having a directory for the new samples.')
        return
    samples = getAudioSamples(filename)
    rate = getFileInfo(filename)
    rate = rate[2]
    '''
    plt.figure(1)
    plt.title('OG Signal Wave...')
    #plt.plot(Time,signal)
    plt.plot(samples)
    plt.show()
    plt.close()
    #print(samples[0:160])
    '''
    number = csvLogger.getNum(filename)
    if number == None:
        number = 0
    newFN = filename[:len(filename)-4]+'/'+filename[:len(filename)-4]+'-version'+str(number)+'.wav'
    obj = wav.open(newFN, 'w')
    obj.setnchannels(1)
    obj.setsampwidth(2)
    obj.setframerate(rate)
    for i in range(len(samples)):
        #print(samples[i])
        #if (samples[i] < 0):
        #    value = samples[i]
        #else:
        #    value = samples[i] * -1
        #value = value + samples[i] + 100 # This needs adjusments 
        value = samples[i] * amount
        if value > 32766:
            value = 32767
        elif value < -32766:
            value = -32766
        #print(value)
        data = struct.pack('<h', value)
        obj.writeframesraw(data)

    obj.close()
   

    
    spf = wav.open(newFN,'rb')

    signal = spf.readframes(-1)
    signal = np.fromstring(signal, 'Int16')
    #fs = spf.getframerate()

    if spf.getnchannels() == 2:
         sys.exit(0)
     
     
    #Time=np.linspace(0, len(signal)/fs, num=len(signal))
    '''     
    plt.figure(num=2)
    plt.title('After Editing Signal Wave...')
    #plt.plot(Time,signal)
    plt.plot(signal)
    plt.show()
    plt.close()
    '''

def filterNoise(filename, low, high):
    
    audiofile = wav.open(filename, 'r')
    info = list(audiofile.getparams())

    number = csvLogger.getNum(filename)
    if number == None:
        number = 0
    newFN = filename[:len(filename)-4]+'/'+filename[:len(filename)-4]+'-version'+str(number)+'.wav'
    output = wav.open(newFN, 'w')
    output.setparams(tuple(info))
    LP = low
    HP = high

    cframe = audiofile.getframerate()
    wholeFileFrames = int(audiofile.getnframes()/cframe)
    #print(audiofile.getnframes())
    #print(wholeFileFrames)
    for frame in range(0, wholeFileFrames):
        no = np.fromstring(audiofile.readframes(cframe), dtype = np.int16)
        LC = no[0::2]
        RC = no[1::2]
        lf = np.fft.rfft(LC)
        rf = np.fft.rfft(RC)
        lf[55:66] = 0
        rf[55:66] = 0
        lf[:LP] = 0
        lf[HP:] = 0
        rf[:LP] = 0
        rf[HP:] = 0
        normalizeLeft = np.fft.irfft(lf)
        normalizeRight = np.fft.irfft(rf)
        ns = np.column_stack((normalizeLeft, normalizeRight)).ravel().astype(np.int16)
        output.writeframes(ns.tostring())
        #print(frame)

    audiofile.close()
    output.close()

def getAmp(fileInfo, targetdB):

    delta = targetdB - fileInfo.dBFS
    result = fileInfo.apply_gain(delta)
    return result

def normalize(filename, targetAmp):
   
    audioFormat = filename[len(filename)-3:]
    audio = AudioSegment.from_file(filename, audioFormat)
    normalizedResult = getAmp(audio, targetAmp)
    number = csvLogger.getNum(filename)
    if number == None:
        number = 0
    newFN = filename[:len(filename)-4]+'/'+filename[:len(filename)-4]+'-version'+str(number)+'.wav'
    normalizedResult.export(newFN, audioFormat)

#normalize('spkr0.wav', -20)
#amplify('test.wav', 4)
#f = sf.SoundFile('test.wav')
#print('samples = {}'.format(len(f)))
#print(f)
#print(len(f))
#print('sample rate = {}'.format(f.samplerate))
#print('seconds = {}'.format(len(f) / f.samplerate))
