import csv 
import numpy as np
import pandas as pd
from scipy import spatial

#Base class for all algorithms 
#Subclasses should provide prediction methods,
#And this base class can load data/ provide generic model evaluation 

class PredictionAlgorithm(object):

    #clickthrough matrix is arranged such that user with ID 1 
    #would be clickthroughMatrix[0] (due to nature of arrays)
    def __init__(self):
        self.clickthroughMatrix = None
        self.clickthroughData = []

    def load_clickthrough_file(self, filePath):

        #load csv into data
        with open(filePath) as csvFile:
            reader = csv.reader(csvFile, delimiter=",")
            for clickthrough in reader:
                userId = int(clickthrough[0])
                articleId = int(clickthrough[1])

                self.clickthroughData.append((userId, articleId))

        #set these global constants
        self.USER_COUNT = max(self.clickthroughData, key= lambda x: x[0])[0]
        self.ARTICLE_COUNT = max(self.clickthroughData, key= lambda x: x[1])[1]
        self.clickthroughMatrix = np.zeros((self.USER_COUNT, self.ARTICLE_COUNT))

        for clickthrough in self.clickthroughData:
            USER_INDEX = clickthrough[0] - 1
            ARTICLE_INDEX = clickthrough[1] - 1

            self.clickthroughMatrix[USER_INDEX][ARTICLE_INDEX] = 1

        print self.clickthroughMatrix

#predicts based on how the user rated similar items
class ItemBasedKNN(PredictionAlgorithm):

    #pass in amount of neighbors to use
    def __init__(self, knn):
        self.knn = knn
        self.inv_map = {}

        super(ItemBasedKNN, self).__init__()


    #override loading of clickthrough file to include the initialization of inverted map
    def load_clickthrough_file(self, filePath):
        #call super method
        super(ItemBasedKNN, self).load_clickthrough_file(filePath)

        for userId, articleList in self.clickthroughData.iteritems():
            for article in articleList:
                self.inv_map.setdefault(article,[])
                self.inv_map[article].append(userId)

    #returns sorted list of tuples in the form (ARTICLE_ID, SIMILARITY)
    def kNearestNeighbors(self, user, k):
        similarities = []
        for currentUserId in self.clickthroughData:
            if not currentUserId == user:
                similarities.append((
                    currentUserId,
                    self._cosine(
                        currentUserId,
                        user
                    )
                ))

        similarities = sorted(similarities, key = lambda x: x[1])
        return similarities[:k]


    #cosine similarity between two ITEMS 
    def _cosine(self, item1, item2):
        return scipy.spatial.distance.cosine(
            self.clickthroughMatrix[:,(item1-1)],
            self.clickthroughMatrix[:,(item2-1)]
        )

#predicts based on what similar users liked
class UserBasedKNN(PredictionAlgorithm):

    #pass in amount of neighbors to use
    def __init__(self, knn):
        self.knn = knn
        super(UserBasedKNN, self).__init__()


    def recommend(self, user, amount):

        #dict that will store articles and recommendation strengths
        recommendations = {}
        nearest_neighbors = self.kNearestNeighbors(user, self.knn)

        #binary vector of user ratings
        userRatings = self.clickthroughMatrix[user-1]
        totalDistsance = 0.0

        #sum of distances, used to weight recommendations
        for user in nearest_neighbors:
            totalDistsance += user[1]

        #actual KNN method
        for user in nearest_neighbors:
            currentUsername = user[0]
            currentWeight = user[1] / totalDistsance
            #binary vector of all articles current user has rated
            currentUserRatings = self.clickthroughMatrix[currentUsername-1]

            for articleId in range(len(currentUserRatings)):
                #if current user rated item, and our target user did not 
                if currentUserRatings[articleId] == 1 and userRatings[articleId] == 0:
                    #on a normal rating system, we would multiply the current weight by the user rating
                    #since we are on binary scale, user rating is one, so we can ignore it and just add the weight
                    #must add one  to recommendation dict since we are dealing in indexes 
                    if not articleId + 1 in recommendations:
                        recommendations[articleId + 1] = currentWeight
                    else:
                        recommendations[articleId + 1] += currentWeight

        recommendations = list(recommendations.items())

        #sort recommendations by their weighted strength, in order from greatest to least
        recommendations.sort(key=lambda x: x[1], reverse = True)

        return recommendations[:amount]

    #returns sorted list of tuples in the form (ARTICLE_ID, SIMILARITY)
    def kNearestNeighbors(self, user, k):
        similarities = []
        for currentUserId in xrange(1,self.USER_COUNT+1):
            if not currentUserId == user:
                print currentUserId, user
                similarities.append((
                    currentUserId,
                    self._cosine(
                        currentUserId,
                        user
                    )
                ))

        similarities = sorted(similarities, key = lambda x: x[1])
        return similarities[:k]


    #uses default scipy cosine similarity, super-fast because numpy
    def _cosine(self, user1, user2):
        distance = spatial.distance.cosine(
            self.clickthroughMatrix[user1-1],
            self.clickthroughMatrix[user2-1]
        )

        return distance 