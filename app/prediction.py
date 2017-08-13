import csv 
import numpy as np

#Base class for all algorithms 
#Subclasses should provide prediction methods,
#And this base class can load data/ provide generic model evaluation 

class Algorithm(object): 

	def __init__(self): 
		#keys are user id's, values are lists of article id's 
		self.clickthroughData = {}

	def load_clickthrough_file(self, filePath): 

		#load csv into data
		with open(filePath) as csvFile: 
			reader = csv.reader(csvFile, delimiter=",") 
			for clickthrough in reader: 
				userId = int(clickthrough[0])
				articleId = int(clickthrough[1])

				if not userId in self.clickthroughData:
					self.clickthroughData[userId] = [articleId]

				else: 
					#only add if unique 
					if not articleId in self.clickthroughData[userId]: 
						self.clickthroughData[userId].append(articleId) 

class UserBasedKNN(Algorithm): 

    #should implement constructor
    #which calls super constructor
    #and sets value for k 
    def __init__(self, knn): 
        self.knn = knn 
        super(UserBasedKNN, self).__init__()


    def recommend(self, user, amount): 

        recommendations = {}
        nearest_neighbors = self.kNearestNeighbors(user, self.knn)

        userRatings = self.clickthroughData[user] 
        totalDistsance = 0.0 

        #sum of distances, used to weight recommendations
        for user in nearest_neighbors: 
            totalDistsance += user[1]

        #actual KNN method
        for user in nearest_neighbors:
            currentUsername = user[0]
            currentWeight = user[1] / totalDistsance
            #gives list of all articles current user clicked on
            currentUserRatings = self.clickthroughData[currentUsername]

            for article in currentUserRatings: 
                if not article in userRatings:
                    if not article in recommendations:
                        recommendations[article] = currentWeight
                    else: 
                        recommendations[article] += currentWeight

        recommendations = list(recommendations.items())

        #sort recommendations by cumulative weight, in order from greatest to least
        recommendations.sort(key=lambda x: x[1], reverse = True)

        return recommendations[:amount]

    def kNearestNeighbors(self, user, k):
        similarities = [] 
        for currentUserId in self.clickthroughData: 
            if not currentUserId == user: 
                similarities.append((
                	currentUserId, 
                	self._cosine(
                		self.clickthroughData[currentUserId], 
                		self.clickthroughData[user]
                	)
                ))

        similarities = sorted(similarities, key = lambda x: x[1])
        return similarities[:k] 

    def _cosine(self, r1, r2):

        #since vectors are sets of article IDs, we can use this fact for faster magnitude calc
        m1 = len(r1) ** 0.5 
        m2 = len(r2) ** 0.5

        #iterate over one vector checking for values for same key in other
        #NOTE: non-shared keys do not contribute to dot product 
        dotProduct = 0 
        for article in r1: 
            if article in r2:
                dotProduct += 1
        return dotProduct / (m1 * m2)