from fuzzywuzzy import fuzz as f
from fuzzywuzzy import process as p

import Levenshtein

namesofTeamVariants = [
'console.log(326)',
'console.log326',
'console.log 326',
'consolelog(326)',
'console log 326',
'console log326',
'console log(326)',
'console.log',
'consolelog326',
'console.log.326'
]

def thisNameOfTeam(string):
    if string in namesofTeamVariants:
        return True
    d = Levenshtein.distance(string, 'console.log(326)')/(len(string)/2)
    print(string, d)
    if d > 0.5 :
        return True

    return False

def inListNameOfTeam(array):
    for string in array:
        if thisNameOfTeam(string):
            return True
    return False

def isFirstInSpeech(value):
    k = f.WRatio(value, 'вездекод консоль лог триста двадцать шесть')
    return k > 90

def getBestCategories(userrow):
    userrow['step'] = -99
    values = list(userrow.values())
    keys = list(userrow.keys())
    max_value = max(values)
    tag_max = keys[values.index(max_value)]

    return tag_max
