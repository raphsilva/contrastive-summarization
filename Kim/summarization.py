#from setup import *
from language import *
from similarity import psi, phi
import math

from setup import SUMLEN
from setup import ALLOW_REPETITION



# clustering algorithm used in the implementation of RF method
from sklearn.cluster import AgglomerativeClustering

# used to obtain the best alignment in polynomial time (Hungarian method)
from scipy.optimize import linear_sum_assignment

from itertools import permutations
from operator import itemgetter


from pprint import pprint


from setup import SIZE_FAC





# Defines the size of the summary of the sets 'side1' and 'side2'.
def summSize(side1, side2):    
    from setup import DATASET_ID
    from setup import METHOD, ASPECTS_TAGS
    l1 = len(side1)
    l2 = len(side2)
    if SUMLEN != None: # Force size to the value specified in the setup
        k = int(SUMLEN/2)
    else:    
        k = 1 + int(math.floor(math.log2(l1 + l2)))
        
    k = int(k*SIZE_FAC[ASPECTS_TAGS][METHOD][DATASET_ID])
    
    print(SIZE_FAC[ASPECTS_TAGS][METHOD][DATASET_ID])
    
    
    return min(k, l1, l2) # Don't allow summaries bigger than original sets (error would occur)




def findCentroids(clusters, text_info, polarity, k):
    centroids = [-1 for i in range(k)]

    # finding the centroids for clusters_x
    for cluster_id, cluster in enumerate(clusters):
        best_value = -math.inf
        best_sentence = -1

        for idx1 in cluster:

            value = 0.0
            for idx2 in cluster:
                value += phi(text_info[idx1], text_info[idx2])

            if value > best_value:
                best_value = value
                best_sentence = idx1

        centroids[cluster_id] = best_sentence
    return centroids





# <--------------------------->
# <-----> COS Functions <----->
# <--------------------------->

from random import uniform




#Representativeness-first approximation to solve the Contrastive Opinion Summarization problem (COS).
def representativeness_first(side1, side2, polarity1, polarity2, LAMBDA=0.5, CENTROIDS_AS_SUMMARY=False, USE_HUNGARIAN_METHOD=False):
    
    if len(side1) * len(side2) == 0: # Case when there's either no negative or no positive opinions; no pairs can be formed.
        return []
    
    contrastive_pairs = []
    
    text_info_1 = [s['text_info'] for s in side1]
    text_info_2 = [s['text_info'] for s in side2]

    # amount of sentence pairs we want in the summary
    k = summSize(side1, side2)    
    
    # calculating the distance matrices; will be used for agglomerative clustering
    # distance_matrix[i, j] = 1.0 - phi(i, j)
    distance_matrix_x = [[(1.0 - phi(text_info_1[i], text_info_1[j])) for j in range(len(side1))] for i in range(len(side1))]
    distance_matrix_y = [[(1.0 - phi(text_info_2[i], text_info_2[j])) for j in range(len(side2))] for i in range(len(side2))]

    # each one below is gonna be a list of clusters (list of lists)
    clusters_x = [list() for i in range(k)]
    clusters_y = [list() for i in range(k)]


    if k > 1:
        # defining the clustering model that is going to be used
        model = AgglomerativeClustering(affinity='precomputed', n_clusters=k, linkage='complete')

        # obtaining the clusters for X and Y
        model_labels_x = model.fit_predict(distance_matrix_x)
        model_labels_y = model.fit_predict(distance_matrix_y)
    
    else: # If there is only one cluster possible, don't try to cluster. 
        model_labels_x = [0 for i in range(len(side1))]
        model_labels_y = [0 for i in range(len(side2))]
        

    for i in range(len(side1)):
        clusters_x[model_labels_x[i]].append(i)
    for j in range(len(side2)):
        clusters_y[model_labels_y[j]].append(j)

    #debug.print_cluster(clusters_x, side1, k)

    # structures to store the centroids for each cluster
    centroids_x = findCentroids(clusters_x, text_info_1, polarity1, k)
    centroids_y = findCentroids(clusters_y, text_info_2, polarity2, k)

    # finding the best alignment
    best_alignment = -1

    if USE_HUNGARIAN_METHOD:
        # using the hungarian method in order to find the best alignment for the clusters
        row_ind, col_ind = linear_sum_assignment(
            [[-1.0 * psi(text_info_1[centroids_x[U]], text_info_2[centroids_y[V]]) for V in range(k)] for U in range(k)])
        best_alignment = list(zip(row_ind, col_ind))
   
    else:
        # using brute force in order to find the best alignment for the clusters
        best_value = -math.inf
        for permutation in permutations(range(k)):

            # turning alignment into a list of pairs like [(0, 1), (1, 2), (2, 0)]
            alignment = list(zip(range(k), list(permutation)))

            value = 0.0
            for U, V in alignment:
                value += psi(text_info_1[centroids_x[U]], text_info_2[centroids_y[V]])

            if value > best_value:
                best_value = value
                best_alignment = alignment
                

    if CENTROIDS_AS_SUMMARY:
        # using the centroids pairs to compose the summary
        for U, V in best_alignment:
            contrastive_pairs.append((centroids_x[U], centroids_y[V]))
            
    else:
        # choosing better sentence pairs than centroid pairs to compose the summary
        for U, V in best_alignment:

            list_pairs = list()
            for ui in clusters_x[U]:
                for vi in clusters_y[V]:
                    list_pairs.append((ui, vi, psi(text_info_1[ui], text_info_2[vi])))

            # sorting all the pairs in each cluster pair in descending order of ψ()
            list_pairs.sort(key=itemgetter(2), reverse=True)

            # obtaining the sentence pair that gives the highest gi value
            best_value = -math.inf
            best_pair = (-1, -1)
            for ui, vi, psi_value in list_pairs:

                sum_u = 0.0
                for x in clusters_x[U]:
                    sum_u += phi(text_info_1[x], text_info_1[ui])
                sum_u /= len(side1)

                sum_v = 0.0
                for y in clusters_y[V]:
                    sum_v += phi(text_info_2[y], text_info_2[vi])
                sum_v /= len(side2)

                value = LAMBDA * (sum_u + sum_v) + ((1.0 - LAMBDA) / k) * psi_value + uniform(-1E-5, 1E-5)

                if value > best_value:
                    best_value = value
                    best_pair = (ui, vi)

                # break loop when it reaches the centroid pair
                if (ui, vi) == (centroids_x[U], centroids_y[V]):
                    break

            # adding the sentence pair with highest gi to the summary
            contrastive_pairs.append(best_pair)
        
    r = []
    # Convert local IDs to the IDs on the source
    for i, j in contrastive_pairs:
        r.append((side1[i]['id'], side2[j]['id']))
    
    return r





# Contrastiveness-first approximation to solve the Contrastive Opinion Summarization problem (COS).
def contrastiveness_first(side1, side2, polarity1, polarity2, LAMBDA=0.5, CENTROIDS_AS_SUMMARY=False, USE_HUNGARIAN_METHOD=False):
    
    
    if len(side1) * len(side2) == 0: # If either side is empty, a summary can't be made.
        return []
    
    contrastive_pairs = []
    
    text_info_1 = [s['text_info'] for s in side1]
    text_info_2 = [s['text_info'] for s in side2]
    
    # amount of sentence pairs we want in the summary
    k = summSize(side1, side2)

    # structures used to find the sets X_ui and Y_vi defined in the paper
    max_similarity_x = [0.0 for sX in side1]
    max_similarity_y = [0.0 for sY in side2]
    
    

    # find the value of ψ for every possible pair
    psis = {}    
    for i in range(len(side1)):
        for j in range(len(side2)):
            psi_i_j = round(psi(text_info_1[i], text_info_2[j]),2)
            
            if (len(psis) == 0 or max(psis.values()) == 0) or psi_i_j > 0: # Threshold (saves a lot of time)
                if psi_i_j not in psis:
                    psis[psi_i_j] = []
                psis[psi_i_j].append((i,j))    

    # Sort pairs in order of contrastiviness
    pairs_rank = []
    for key in sorted(psis.keys(), reverse=True):
        pairs_rank += psis[key]
    
    best_pair = pairs_rank[0]
    
    contrastive_pairs.append(best_pair)

    # initializing the best φ values for each sentence
    for i in range(len(side1)):
        max_similarity_x[i] = phi(text_info_1[i], text_info_1[best_pair[0]])
    for j in range(len(side2)):
        max_similarity_y[j] = phi(text_info_2[j], text_info_2[best_pair[1]])


    # after choosing the ﬁrst pair, we will iteratively choose a pair to maximize the "gain function"
    for k_i in range(1, k): # k is the number of sentence pairs in the summary
        
        best_value = -math.inf
        best_pair = (-1, -1)

        # testing the pair (u, v)
        for u, v in pairs_rank:
            
            # skip pairs that are already in the summary 
            if (u,v) in contrastive_pairs:
                continue
            if not ALLOW_REPETITION:
                if u in [i[0] for i in contrastive_pairs]:
                    continue
                if v in [i[1] for i in contrastive_pairs]:
                    continue
                

            # compute the gain function for the pair (u, v)
            sum_in_x = 0
            sum_in_y = 0

            # These two following loops are computing the sums in gain function, considering the sets X_ui and Y_vi
            for e in range(len(side1)):
                dist = phi(text_info_1[e], text_info_1[u])
                if  dist > max_similarity_x[e]:
                    sum_in_x += dist
            sum_in_x /= len(side1)

            for e in range(len(side2)):
                dist = phi(text_info_2[e], text_info_2[v])
                if dist > max_similarity_y[e]:
                    sum_in_y += dist
            sum_in_y /= len(side2)

            value = LAMBDA * (sum_in_x + sum_in_y) + ((1 - LAMBDA) / k) * psi(text_info_1[u], text_info_2[v]) + uniform(-1E-5, 1E-5)

            if value > best_value:  # the pair that maximizes the gain function will be added to the summary
                best_value = value
                best_pair = (u, v)

        # add the pair with the highest gain function to summary
        contrastive_pairs.append(best_pair)


        # remember the best φ values for each of all sentences given by the i−1 already chosen sentence pairs at each step
        for u in range(len(side1)):
            max_similarity_x[u] = max(max_similarity_x[u], phi(text_info_1[u], text_info_1[best_pair[0]]))
        for v in range(len(side2)):
            max_similarity_y[v] = max(max_similarity_y[v], phi(text_info_2[v], text_info_2[best_pair[1]]))
    
    
    
    r = []
    # Convert local IDs to the IDs on the source
    for i, j in contrastive_pairs:
        r.append((side1[i]['id'], side2[j]['id']))
    
    
    return r
