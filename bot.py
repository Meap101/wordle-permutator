import copy

dictionaryFile = open("dictionary.txt", "r") 
dictionary = dictionaryFile.read().split("\n")

del dictionary[-1] # txt files have an empty line at the end

starter = ["front", "lamed", "cuish"]

results = []
totalGuesses = 0
totalFails = 0

for word in starter: # remove starter from dictionary
    index = dictionary.index(word)
    
    if index > -1:
        del dictionary[index]
        
wordsChecked = 0

def solve(mutableDictionary, guessMemoryGrn, guessMemoryYlw, guessMemoryGry): # determines a list of possible solutions given constraints
    
   # if None not in guessMemoryGrn:
    #    return {''.join(guessMemoryGrn)}
    
    narrowedGuesses = set()
    
    for possibleGuess in mutableDictionary: # actually solve the wordle
        
        viable = True
            
        mutableGuess = possibleGuess
                
        for index, greenLetter in enumerate(guessMemoryGrn):
            if greenLetter is None:
                continue
            
            if mutableGuess[index] != greenLetter:
                viable = False
                break
            else:
                mutableGuess = mutableGuess[:index] + "0" + mutableGuess[index + 1:] # replace matched character with a placeholder 0 so that future checks for the same character will require a second instance of the character present. strings aren't mutable, use slices as a hack
        
        for yellowLetter in guessMemoryYlw:
            if yellowLetter not in mutableGuess:
                viable = False
                break
            elif mutableGuess[guessMemoryYlw[yellowLetter]] == yellowLetter: # if the letter is in the same pos as the yellow letter, it can't be viable
                viable = False
                break
            else:
                yellowIndex = mutableGuess.find(yellowLetter)
                
                mutableGuess = mutableGuess[:yellowIndex] + "0" + mutableGuess[yellowIndex + 1:] # replace matched character with a placeholder 0 so that future checks for the same character will require a second instance of the character present. strings aren't mutable, use slices as a hack
                
        for grayLetter in guessMemoryGry: # filter by gray letters last
            if grayLetter in mutableGuess:
                viable = False
                break
        
   #     if possibleGuess in guessHistory:
       #     continue
        
        if viable:
            narrowedGuesses.add(possibleGuess)
    
    return narrowedGuesses

def updateMemory(currentlyChecking, guessMemoryGrn, guessMemoryYlw, guessMemoryGry): # virtual recreation of the wordle server, giving the player information based on a guess
    
    for word in currentlyChecking:
            
            wordLetters = list(word)
            
            for i in range(5):

                if answerWord[i] == wordLetters[i]:
                    guessMemoryGrn[i] = wordLetters[i]
                    
                    if answerWord[i] in guessMemoryYlw: # remove from yellow memory once index is found
                        del guessMemoryYlw[answerWord[i]]
                elif wordLetters[i] in answerWord:
                    
                    if wordLetters[i] != guessMemoryGrn[answerWord.index(wordLetters[i])]: # only add to yellow memory if index has not already been identified
                        guessMemoryYlw[wordLetters[i]] = i
                else:
                    guessMemoryGry.add(wordLetters[i])
                    
    return guessMemoryGrn, guessMemoryYlw, guessMemoryGry

def heuristic(narrowedGuesses, guessMemoryGrn, guessMemoryYlw, guessMemoryGry): # chooses best option out of a list of options based on permutations eliminated
    
    maxPermutations = float('-inf')
    nextGuess = None
    
    for guess in narrowedGuesses:
        
        guessPermutations = 0

        newInformation = {x for x in guess if x not in guessMemoryGry and x not in guessMemoryGrn and x not in guessMemoryYlw} # assume all letters in the guess are gray to calculate permutations eliminated
        
        for otherGuess in narrowedGuesses:
            for letter in newInformation:
                if letter in otherGuess:
                    guessPermutations += 1
                    break
                
        #  guessMemoryGrn, guessMemoryYlw, guessMemoryGry = updateMemory([guess], guessMemoryGrn, guessMemoryYlw, guessMemoryGry) # uncomment to have the wordle bot cheat
      # guessPermutations = len(solve(narrowedGuesses, guessMemoryGrn, guessMemoryYlw, mutableGuessMemoryGry)) # uncomment to have the wordle bot cheat
    
        if guessPermutations > maxPermutations:
            maxPermutations = guessPermutations
            nextGuess = guess

    return nextGuess

for answerWord in dictionary:
    
    # initialize memory variables
    
    guessMemoryGrn = [None, None, None, None, None] # letter's list index indicates word index
    guessMemoryYlw = {} # dictionary of pairs (letter, index)
    guessMemoryGry = set()

    mutableDictionary = copy.deepcopy(dictionary)

    currentlyChecking = starter
    guessHistory = []

    gameOver = False
    guesses = 0
    
    wordsChecked += 1;

    print(str(wordsChecked) + "/" + str(len(dictionary)))
    
    while gameOver == False:
        
        guessHistory += currentlyChecking
        
        guessMemoryGrn, guessMemoryYlw, guessMemoryGry = updateMemory(currentlyChecking, guessMemoryGrn, guessMemoryYlw, guessMemoryGry)
        
        guesses += len(currentlyChecking)
        
        narrowedGuesses = solve(mutableDictionary, guessMemoryGrn, guessMemoryYlw, guessMemoryGry)
        
        mutableDictionary = copy.deepcopy(narrowedGuesses)
            
        nextGuess = narrowedGuesses.pop()
        
       # nextGuess = heuristic(narrowedGuesses, guessMemoryGrn, guessMemoryYlw, guessMemoryGry)   
        
        if nextGuess == answerWord or guesses > 5:
            gameOver = True
            
            guesses += 1
            
            if guesses <= 6:
                
                results.append(answerWord + " guessed in " + str(guesses) + " guesses")
                
                totalGuesses += guesses  
            else:
                results.append(answerWord + "failed")
                
                totalFails += 1
        else:
            currentlyChecking = [nextGuess]
            
print("Total Guesses: " + str(totalGuesses))
print("Total Fails: " + str(totalFails))
# print(results); # data dump from every single word
