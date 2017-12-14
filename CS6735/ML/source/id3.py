import math
from collections import Counter

def entropy(data, target_attr):
    e = 0.0
    c = Counter([record[target_attr] for record in data])
    for t in c.values():
        e += (-float(t)/len(data)) * math.log(float(t)/len(data), 2)
    return e
    
def infogain(data, attr, target_attr):
    subset_entropy = 0.0
    c= Counter([record[attr] for record in data])
    for val in c.keys():
        val_prob = float(c[val]) / sum(c.values())
        data_subset = [record for record in data if record[attr] == val]
        subset_entropy += val_prob * entropy(data_subset, target_attr)
    return (entropy(data, target_attr) - subset_entropy)
            
