'''
Date: 03/07/2017
Author: Sean Kinahan
Description: Coding test problem 2 for Enflux

Suppose there exists a social network with the following properties:
Any user may post original content
Any user may repost original content or another user's repost
Any user may follow any other user
The social network data is represented in a CSV file with the following format:

postId, repostId, followers
1, -1, 120
2, 1, 60
3, 1, 30
4, 2, 90
5, 3, 40
6, 4, 10
7, -1, 240
8, 7, 190
9, 7, 50


Where:
postId - The ID of the post or repost
repostId - The ID of the content that was reposted or -1 if this is an original post
followers - The number of followers the user that made the post has

Write a program that will analyze this social network to output the number of viewers any piece of original
content has reached. For the example above, the output would be:
1: 350
7: 480

Note: It is safe to make the assumption that no posts share any common followers.
'''
from ast import literal_eval
import csv
import unittest
import random

class Post():  
    def __init__(self, postId, repostId, followers):
        self.postId = postId
        self.repostId = repostId
        self.followers = followers
        self.reposters = []

    def add_reposter(self, repost):
        self.reposters.append(repost)    

    def num_followers(self):
        followTotal = self.followers
        for follower in self.reposters:
            followTotal += follower.num_followers()
        return followTotal

#helper function removes whitespaces and returns literal value
def splitConvertLiteral(str):
    return literal_eval(''.join(str.split()))

def sumFollowers(allPosts):
    originalPosts = {}
    for postId in allPosts:
        post = allPosts[postId]
        if post.repostId != -1:
            allPosts[post.repostId].add_reposter(post)
        else:
            originalPosts[postId] = post
    return [str(postId) + ' : ' + str(originalPosts[postId].num_followers()) for postId in originalPosts]

def performAnalysis(filename):
    allPosts = {}
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            postId, repostId, followers = [splitConvertLiteral(row[key]) for key in row.keys()]
            newPost = Post(postId, repostId, followers)
            allPosts[postId] = newPost
    csvfile.close()
    return sumFollowers(allPosts)

class TestSocialNetworkAnalysis(unittest.TestCase):

    def test_postclass(self):
        newPost = Post(300, 82, 65)
        assert newPost.postId == 300
        assert newPost.repostId == 82
        assert newPost.followers == 65

    def test_splitconvertliteral(self):
        str = ' -1   '
        assert splitConvertLiteral(str) == -1
        str2 = ' -0.00425  '
        assert splitConvertLiteral(str2) == -0.00425
        str3 = '      400000'
        assert splitConvertLiteral(str3) == 400000

    def test_simple(self):
        allPosts = {}
        for postId in range(0, 99):
            post = Post(postId, -1, 100)
            allPosts[postId] = post
        result = sumFollowers(allPosts)
        for idx in range(0, 99):
            assert result[idx] == (str(idx) + ' : ' + str(100))

    def test_skewed(self):
        allPosts = {}
        for postId in range(0, 10):
            post = Post(postId, postId-1, 100)
            allPosts[postId] = post
        result = sumFollowers(allPosts)
        for str in result:
            item = str.split(' : ')
            assert splitConvertLiteral(item[0]) == 0
            assert splitConvertLiteral(item[1]) == 1000

    def test_big_skewed(self):
        for numPosts in range (0, 100):
            for numIndividualFollowers in range(0, 100):
                allPosts = {}
                for postId in range(0, numPosts):
                    post = Post(postId, postId-1, numIndividualFollowers)
                    allPosts[postId] = post
                result = sumFollowers(allPosts)
                for str in result:
                    item = str.split(' : ')
                    assert splitConvertLiteral(item[0]) == 0
                    assert splitConvertLiteral(item[1]) == (numPosts*numIndividualFollowers)

    def test_big_random(self):
        allPosts = {}
        totalNumFollowers = 0
        for postId in range(0, 100):
            if postId == 0:
                post = Post(postId, -1, 200)
            else:
                post = Post(postId, random.randrange(-1, postId), 200)
            totalNumFollowers += 200
            allPosts[postId] = post
        result = sumFollowers(allPosts)
        for str in result:
            item = str.split(' : ')
            assert splitConvertLiteral(item[1]) <= totalNumFollowers
            
    def test_provided(self):
        result = performAnalysis('socialnetwork.csv')
        assert '1 : 350' in result
        assert '7 : 480' in result
    
if __name__ == '__main__':
    unittest.main()
