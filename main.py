#!/usr/bin/python3
import csvLogger
import audiomin
import datetime
import os

def helloworld():
    print('helloworld')

def mainMenuPrint():
    print('\n\n===============================')
    print('0: quit the program')
    print('1: Print log')
    print('2: Amplify a sound clip')
    print('3: Remove background noise of a sound clip')
    print('4: Normalize a sound clip')
    print('===============================\n\n')

menuOptions = {0 : quit,
               1 : csvLogger.printGeneral,
               2 : None}
def main():

    amplifyDef = 4
    lowDef = 21
    highDef = 9000
    normDef = -20
    csvLogger.createGeneralLog()
    csvLogger.createVersionLog()

    while True: 
        while True:
            mainMenuPrint()
            try: 
                choice = int(input('please enter an option: '))
                if choice > 4:
                    raise LookupError
                break;
            except ValueError as error:
                print('Error: please enter a valid option(number)..\n')
            except LookupError as error:
                print('Error: please enter a valid option..\n')
            

        if choice < 2: 
            menuOptions[choice]()
        else:
            while True:
                filename = input('Please enter the file name that you want to modify (has to be in the same directory): ')
                if filename == 'm':
                    break;
                try:
                    if os.path.isfile(filename) == False or len(filename) < 5 or filename[-4:] != '.wav':
                        raise LookupError
                    break;
                except LookupError as error: 
                    print('\n\nError: please enter a valid file name in the same directory..')
                    print('Example: example.wav')
                    print('Enter m if you want to return to the main menu\n\n')
            #print('we are here after file addition')
            if filename != 'm':
                info = audiomin.getFileInfo(filename)
                csvLogger.createSpecificLog(filename, info)
                if choice == 2:
                    while True:
                        amplifySet = int(input('Please enter by how much you would want to amplify the audio clip(1-5), or 0 for the default value: '))
                        if amplifySet > 5 or amplifySet < 0:
                            print('error, please enter a valid value')
                        else:
                            break;
                    if amplifySet == 0:
                        audiomin.amplify(filename, amplifyDef)
                        setting = amplifyDef
                    else:
                        audiomin.amplify(filename, amplifySet)
                        setting = amplifySet
                    csvLogger.increFile(filename)
                    csvLogger.addNewEntry(filename, 'Yes', amplifySet, 'No', '(0, 0)', 'No', 0)
                elif choice == 3:
                    low = int(input('Please enter the number of the low frequency to filter out, or -1 for the default value: '))
                    if low == -1:
                        low = lowDef
                    high = int(input('Please enter the number of the high frequency to filter out, or -1 for the default value: '))
                    if high == -1:
                        high = highDef
                    audiomin.filterNoise(filename, 21, 9000)
                    csvLogger.increFile(filename)
                    csvLogger.addNewEntry(filename, 'No', 0, 'Yes', '('+str(low)+', '+str(high)+')', 'No', 0)
                elif choice == 4:
                    target = int(input('Please enter the the decibel, or -1 for the default value: '))
                    if target == -1:
                        target = normDef
                    audiomin.normalize(filename, target)
                    csvLogger.increFile(filename)
                    csvLogger.addNewEntry(filename, 'No', 0, 'No', '(0, 0)', 'Yes', target)


                    

                    
            







if __name__ == '__main__':
    main()
