# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 10:59:50 2017

@author: Raksunaksu
"""

import re
import time
import random
import collections

output_size = 100
#look_ahead = 5
#weights = [5, 5, 3, 1, 1]     # Longest combination first
look_ahead = 3
weights = [10, 5, 1]


assert(len(weights) == look_ahead)


brain = {}
brain_size = 0

# punctuations: .,!?
pattern = re.compile(r"([.,!\?:;-])")

print('Teaching')

fi = open("alice.txt", "r")

line = ""

last_word = collections.deque("", look_ahead)

while True:
    line = fi.readline()

    if not line:
        break

    #print line

    line_length = len(line)

    if line_length == 0:
        continue
    
    # Switch all to lower case
    #line = line.lower()    
    
    # Split line with preserving punctuations
    #line2 = pattern.sub(" \\1", line)
    #line_words = line2.split()
    line_words = line.split()
    n_words = len(line_words)    
    
    for word in line_words:
        word = word.strip()

        # Create prefixes of different lengths
        for x in range(0, min(look_ahead,len(last_word))):
            prefix = ""
            for y in range(x, min(look_ahead, len(last_word))):
                prefix = prefix + " " + last_word[y]
                prefix = prefix.strip()

            #print word, "\t", prefix

            if not prefix in brain:
                brain[prefix] = {"n":0, "next":{}}

            brain[prefix]["n"] += 1
                
            if not word in brain[prefix]["next"]:
                brain[prefix]["next"][word] = 1
            else:
                brain[prefix]["next"][word] += 1
            
        last_word.append(word)


fi.close()

print('Teaching done')



random.seed(time.time())

last_word = collections.deque("", look_ahead)

# Select first word randomly
word = random.choice(brain.keys())
print word,
for part in word.split():
    last_word.append(part)


# Then continue in chain
for n in range(output_size-1):
    result = random.random()
    choices = {}
    choice_amount = 0

    # Create selection of choices of next words
    for x in range(0, min(look_ahead,len(last_word))):
        prefix = ""
        weight = weights[x]

        for y in range(x, min(look_ahead, len(last_word))):
            prefix = prefix + " " + last_word[y]

        prefix = prefix.strip()
        #print "\t", prefix
        
        if not prefix in brain:
            #print "\t", "Not found:", prefix
            continue

        # Go through possible next words
        for choice in brain[prefix]["next"]:
            we = weight * brain[prefix]["next"][choice]
            
            if not choice in choices:
                choices[choice] = we
            else:
                choices[choice] += we

            choice_amount += we

            #print "\t", choice, weight, brain[prefix]["next"][choice]

    # If there was some choices for the next word
    if len(choices) > 0:
        prob = 0
        for choice in choices:
            prob += choices[choice] / float(choice_amount)
            #print "\t", result, prob, choice
            if result <= prob:
                print choice,
                last_word.append(choice)
                break
                
    else: # If not, just select something randomly
        # print "XXX",
        
        word = random.choice(brain.keys())
        print word,
        for part in word.split():
            last_word.append(part)

