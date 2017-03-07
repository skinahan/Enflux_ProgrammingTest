'''
Date: 03/07/2017
Author: Sean Kinahan
Description: Coding test problem 1 for Enflux

Write a function or program that will take 2 arrays of integers, "current" and "target",
and produce 2 arrays representing an additions list and a deletions list such that applying the additions
and deletions to the "current" array will yield the "target" array.

For example, given the following inputs:
current: [1, 3, 5, 6, 8, 9]
target: [1, 2, 5, 7, 9]

The outputs would be:
additions: [2, 7]
deletions: [3, 6, 8]

So that the following is true:
current([1, 3, 5, 6, 8, 9]) + additions([2, 7]) - deletions([3, 6, 8]) = target([1, 2, 5, 7, 9])
'''

import unittest

# Naive/pedantic implementation - Time: ~93s
'''
def array_diff(current, target):
    additions = []
    deletions = []
    for item in current:
        if item not in target:
            deletions.append(item)
    for item in target:
        if item not in current:
            additions.append(item)
    return additions, deletions      
'''

# Better implementation, using list comprehensions - Time: ~47s
'''
def array_diff(current, target):
    current = set(current)
    additions = [item for item in target if item not in current]
    deletions = [item for item in current if item not in target]
    return additions, deletions
'''

# Best implementation, using sets (assuming order does not matter, otherwise would need to call sort() on arrays
# before returning) - Time: ~16s
def array_diff(current, target):
    additions = list(set(target) - set(current))
    deletions = list(set(current) - set(target))
    return additions, deletions


class TestArrayDiff(unittest.TestCase):

    def test_provided(self):
        current = [1,3,5,6,8,9]
        target = [1,2,5,7,9]
        expectedAdditions = [2,7]
        expectedDeletions = [3, 6, 8]
        additions, deletions = array_diff(current, target)
        for item in expectedAdditions:
            assert item in additions
        for item in expectedDeletions:
            assert item in deletions

    def test_validity(self):
        additions, deletions = array_diff([1,3,5,6,8,9],[1,2,5,7,9])
        for item in additions:
            assert item not in deletions
        for item in deletions:
            assert item not in additions

    def test_fulladdition(self):
        target = [x for x in range(0, 1000)]
        additions, deletions = array_diff([], target)
        assert additions == target
        assert deletions == []

    def test_fulldeletion(self):
        current = [x for x in range(0, 1000)]
        additions, deletions = array_diff(current, [])
        assert additions == []
        assert deletions == current

    def test_big_no_additions(self):
        current = [x for x in range(0, 60000)]
        target  = [x for x in range(30000, 60000)]
        additions, deletions = array_diff(current, target)
        assert additions == []
        for i in range(0, 29999):
            assert i in deletions

    def test_big_no_deletions(self):
        current = [x for x in range(0, 30000)]
        target  = [x for x in range(0, 60000)]
        additions, deletions = array_diff(current, target)
        assert deletions == []
        for i in range(30001, 60000):
            assert i in additions

if __name__ == '__main__':
    unittest.main()
