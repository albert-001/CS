import sys
from util import unique, vote, get_data, std_dev
from collections import Counter
from math import log
from classes import classes


def prob_dic(l):
    p = dict(Counter(l))
    for k in p.keys():
        p[k] = p[k] / float(len(l))
    return p

def create_naive_bayes(data, attrs, target_attr, classes):
    #Naive Bayes
    #1. calculate the P(class)
    p_class = prob_dic(classes)

    #2. calculate P(attribute=value|class)
    p_class_attr_val = {}
    for c in classes:
        p_class_attr_val[c] = {}
        p_data = [d for d in data if d[target_attr]==c]
        for attr in attrs:
            values = [d[attr] for d in p_data]
            p_class_attr_val[c][attr] = prob_dic(values)

    #3. calculate P(attribute=value)
    p_attr_val = {}
    for attr in attrs:
        values = [d[attr] for d in data]
        p_attr_val[attr] = prob_dic(values)

    return (p_class, p_class_attr_val, p_attr_val)

def classify_naive_bayes(classifier, data, classes, attrs):
    p_class, p_class_attr_val, p_attr_val = classifier
    #4. P(class|attribute=value) = P(attribute=value|class)P(class)/P(attribute=value)
    classification = []
    for d in data:
        p_c = {}
        p_x = {}
        for c in classes:
            p_c[c] = 1.0
            p_x[c] = 1.0
            for attr in attrs:
                if not attr in p_class_attr_val[c]:
                   p_c[c] = 0
                   break
                if d[attr] in p_class_attr_val[c][attr]:
                   p_c[c] *= p_class_attr_val[c][attr][d[attr]]
                else:
                   p_c[c] = 0
                   break
                if d[attr] in p_attr_val[attr]:
                   p_x[c] *= p_attr_val[attr][d[attr]]
                else:
                   p_x[c] = 0
                   break
            p_c[c] = 0 if (p_x[c] == 0 or p_c[c] == 0) else p_c[c]*p_class[c]/p_x[c]
        max_p = max([p_c[c] for c in classes])
        for c in classes:
            if max_p==p_c[c]:
                classification.append(c)
                break
    return classification

if __name__ == "__main__":
    filename = sys.argv[1]

    data, attributes, target_attr = get_data(filename)
    n = len(data)

    accs = []
    for i in range(5):
        valid_data = data[int(float(n)/5*i):int(float(n)/5*(i+1))] #validation data
        train_data = [d for d in data if not d  in valid_data] #training data
        default = vote([d[target_attr] for d in train_data])
        attrs = [a for a in attributes if not a==target_attr]
        classifier = create_naive_bayes(train_data, attrs, target_attr, classes[filename])
        classification = classify_naive_bayes(classifier, valid_data, classes[filename], attrs)
        labels = [d[target_attr] for d in valid_data]
        count = 0
        for x,y in zip(classification, labels):
            if x==y:
                count += 1
        acc = float(count)/len(classification)
        accs.append(acc)
        print("accuracy: " + str(100*acc) + "%")
    print("standard deviation: " + str(std_dev(accs)))