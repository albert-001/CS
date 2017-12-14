import sys
from dtree import create_decision_tree, classify_decision_tree
from classes import classes
from util import vote, get_data, std_dev
from ada_boost import ada_boost_train, ada_boost_classify
from naiveBayes import create_naive_bayes, classify_naive_bayes

if __name__ == "__main__":
    filename = sys.argv[1]
    num_trees = int(sys.argv[2])
    classifier = int(sys.argv[3])

    data, attributes, target_attr = get_data(filename)
    n = len(data)

    accs = []
    for i in range(5):
        valid_data = data[int(float(n)/5*i):int(float(n)/5*(i+1))] #validation data
        train_data = [d for d in data if not d  in valid_data] #training data
        labels = [d[target_attr] for d in data]
        default = vote(labels)
        if classifier == 1: #decision tree
            classifier_generator = create_decision_tree
            classifier_function = classify_decision_tree
            params = default
        else: #naive bayes
            classifier_generator = create_naive_bayes
            classifier_function = classify_naive_bayes
            params = classes[filename]
        #train
        classifiers, weights = ada_boost_train(data, attributes, target_attr, classifier_generator, num_trees, classifier_function, params)
        #classify
        classification = ada_boost_classify(data, classifiers, weights, classifier_function, params, classes[filename], [a for a in attributes if not a==target_attr])
        count = 0
        for x,y in zip(classification, labels):
            if x==y:
                count += 1
        acc = float(count)/len(classification)
        accs.append(acc)
        print("accuracy: " + str(100*acc) + "%")
    print("standard deviation: " + str(std_dev(accs)))
