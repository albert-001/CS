import sys
from dtree import create_decision_tree, classify_decision_tree
from util import print_tree, vote, get_data, std_dev


if __name__ == "__main__":
    filename = sys.argv[1]

    data, attributes, target_attr = get_data(filename)
    n = len(data)
    
    accs = []
    for i in range(5):
        valid_data = data[int(float(n)/5*i):int(float(n)/5*(i+1))] #validation data
        train_data = [d for d in data if not d  in valid_data] #training data
        tree = create_decision_tree(train_data, attributes, target_attr)
        labels = [d[target_attr] for d in valid_data]
        classification = classify_decision_tree(tree, valid_data, vote(labels))
        count = 0
        for x,y in zip(classification, labels):
            if x==y:
                count += 1
        acc = float(count)/len(classification)
        accs.append(acc)
        print("accuracy: " + str(100*acc) + "%")
    print("standard deviation: " + str(std_dev(accs)))
