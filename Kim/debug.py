from pprint import pprint

def print_cluster(cluster, side, k):    
    pprint(cluster)
    for i in range(k):
        print (' ---- CLUSTER', i)
        for j in cluster[i]:
            print (side[j])
        print()
    input()
