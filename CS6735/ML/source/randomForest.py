import numpy
import sys
from dtree import create_decision_tree, classify_decision_tree
from math import sqrt
from util import vote, get_data, std_dev


def create_forest(data, attributes, target_attr, num_trees):
    forest = []
    for i in range(num_trees):
        #randomly select 30% of data with replacement
        train_data = numpy.random.choice(data, size=int(float(n)*0.3), replace=True)
        att_size = len(attributes)-1 if len(attributes)<10 else int(sqrt(len(attributes)))
        train_attr = list(numpy.random.choice([a for a in attributes if not a==target_attr], size=att_size))
        train_attr.append(target_attr)
        tree = create_decision_tree(train_data, train_attr, target_attr)
        forest.append(tree)
    return forest

if __name__ == "__main__":
    filename = sys.argv[1]
    num_trees = int(sys.argv[2])
    
    data, attributes, target_attr = get_data(filename)
    n = len(data)

    accs = []
    for i in range(5):
        valid_data = data[int(float(n)/5*i):int(float(n)/5*(i+1))] #validation data
        train_data = [d for d in data if not d  in valid_data] #training data
        labels = [d[target_attr] for d in valid_data]
        trees = create_forest(data, attributes, target_attr, num_trees)
        #classify
        classes = [];
        for tree in trees:
            classification = classify_decision_tree(tree, valid_data, vote(labels))
            classes.append(classification)
        classification = [vote(c) for c in zip(*classes)]
        count = 0
        for x,y in zip(classification, labels):
            if x==y:
                count += 1
        acc = float(count)/len(classification)
        accs.append(acc)
        print("accuracy: " + str(100*acc) + "%")
    print("standard deviation: " + str(std_dev(accs)))
