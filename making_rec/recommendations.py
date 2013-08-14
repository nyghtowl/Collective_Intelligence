'''
Ch 2 Collective Intellience / Making Recommendations

'''

# A dictionary of movie critics and their ratings of a small set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

from math import sqrt

#Get the list of mutually rated items
def mutually_rated_items(prefs,p1,p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1
    return si

# Euclidean Distance Score returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
    si=mutually_rated_items(prefs,person1,person2)

    # If they have not ratings in common, return 0
    if len(si)==0: return 0

    # Add up the squares of all the differences
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in si])

    return 1/(1+sqrt(sum_of_squares))
    # Note the O'Reilly book answer for Lisa Rose and Gene Seymour is incorrect

# Pearson correlation coefficient for p1 and person2
def sim_pearson(prefs,p1,p2):
    si=mutually_rated_items(prefs,p1,p2)

    si_len = len(si)

    # If they have not ratings in common, return 0
    if si_len==0: return 0

    # Add the preferences 
    sum1 = sum([prefs[p1][item] for item in si])
    sum2 = sum([prefs[p2][item] for item in si])

    # Sum the squares
    sum1Sqr = sum([pow(prefs[p1][item],2) for item in si])
    sum2Sqr = sum([pow(prefs[p2][item],2) for item in si])

    # Sum the products
    pSum = sum([prefs[p1][item]*prefs[p2][item] for item in si])

    # Calculate Pearson score
    num = pSum-(sum1*sum2/si_len)
    den = sqrt((sum1Sqr-pow(sum1,2)/si_len)*(sum2Sqr-pow(sum2,2)/si_len))
    if den==0: return 0

    coefficient=num/den

    return coefficient

# Best matches for person from critics dictionary
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_pearson):
    scores=[(similarity(prefs,person,other),other) for other in prefs if other != person] # creates tuple of pearson score and cooresponding person

    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]

#Get recommendations for a person by using a weighted average of evey other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        # Don't compare me to myself
        if other == person: continue
        sim=similarity(prefs,person,other)

        # Ignore scores of zero or lower
        if sim <= 0: continue
        for item in prefs[other]:

            # Only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item,0)
                totals[item]+= prefs[other][item]*sim
                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim

    # Create the normalized list
    rankings = [(total/simSums[item], item) for item, total in totals.items()]

    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

# Transform dictionary to find movie recommendations based on a movie watched

def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})

            # Flip item and person
            result[item][person]=prefs[person][item]
    return result