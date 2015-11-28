#!/usr/bin/python
__author__ = 'Athanasios Garyfalos'

def test(sample) :
    if 'This' in sample :
        return 'Return with String'
    else :
        return

print(test('This'))
emptyString = test('That')
if emptyString is not None :
    print 'Not empty, Impossible'
else :
    print 'Empty String'
