import numpy
from math import sqrt, log, exp
from naiveBayes import classify_naive_bayes


def ada_boost_train(data, attributes, target_attr, classifier_generator, num_classifer, classifier_function, params):
    attrs = [a for a in attributes if not a==target_attr]
    classifiers = []
    class_weight = [1]*num_classifer
    dataset = data[:]
    n = len(dataset)
    if n> 5000 and (not len(attributes)==17):
        sub_p = 0.1
    else:
        sub_p = 0.8
    att_size = len(attributes)-1
    data_weight = [0]*n
    for i in range(n):
        data_weight[i] = 1.0/n #normalize
    for i in range(num_classifer):
        train_data = numpy.random.choice(dataset, size=int(float(n)*sub_p), replace=True, p=data_weight)
        train_attr = list(numpy.random.choice([a for a in attributes if not a==target_attr], size=att_size))
        train_attr.append(target_attr)
        if classifier_function == classify_naive_bayes:
            train_data = dataset
            train_attr = attributes
        valid_data = dataset #all data
        classifier = classifier_generator(train_data, train_attr, target_attr, params)
        results = classifier_function(classifier, valid_data, params, attrs)
        labels = [d[target_attr] for d in valid_data]
        count = 0
        for x,y in zip(results, labels):
            if not x==y:
                count += 1
        error = float(count)/len(results)
        error = 0.01 if error==0.0 else error #avoid division by zero
        alpha = 0.5*log(float(1-error)/float(error))
        #update weight of classifier
        class_weight[i] = alpha
        classifiers.append(classifier)
        #update weight of dataset
        total_dw = 0.0
        for i, d in enumerate(valid_data):
            dw = data_weight[i]*exp(-alpha*(1 if (results[i]==d[target_attr]) else -1))
            data_weight[i] = dw
            total_dw += dw
        for i, d in enumerate(valid_data):
            dw = data_weight[i]/total_dw #normalize
            data_weight[i] = dw
    return classifiers, class_weight

def ada_boost_classify(data, classifiers, weights, classifier_function, params, classes, attrs):
    valid_data = data[:]
    cs = []
    for classifier, w in zip(classifiers, weights):
        results = classifier_function(classifier, valid_data, params, attrs)
        rs = [w if (r==classes[0]) else -w for r in results]
        cs.append(rs)
    return [classes[0] if (sum(c)>0) else classes[1] for c in zip(*cs)]


def ada_boost_classify(data, classifiers, weights, classifier_function, params, classes, attrs):
    valid_data = data[:]
    cs = []
    rs = {}
    total_results = []
    for classifier, w in zip(classifiers, weights):
        results = classifier_function(classifier, valid_data, params, attrs)
        total_results.append(results)

    cs = []
    for i in range(len(total_results[0])):
        rs = {}
        for j in range(len(total_results)):
            for index,c in enumerate(classes):
                if c==total_results[j][i]:
                    if index in rs.keys():
                        rs[index] += w
                    else:
                        rs[index] = w
                else:
                    if not index in rs.keys():
                        rs[index] = 0
        cs.append(rs)
    classifications = []
    for c in cs:
        for i in range(len(classes)):
            if c[i]==max(c.values()):
                classifications.append(classes[i])
                break
    return classifications