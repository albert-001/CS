import sys
from math import sqrt
from operator import itemgetter
from util import vote, get_data, std_dev
from copy import deepcopy

#calculate Euclidean distance with selected attributes
def euclidean_distance(x1, x2, selected_attrs):
	return sqrt(sum([pow((x1[attr] - x2[attr]), 2) for attr in selected_attrs]))

def get_neighbors(train_data, valid_d, k, selected_attrs):
	distances = {}
	for d in train_data:
		dis = euclidean_distance(d, valid_d, selected_attrs)
		distances[dis] = d
	return [distances[i] for i in sorted(distances.iterkeys())[:k]]

def kNN_classifier(neighbors, target_attr):
	return vote([n[target_attr] for n in neighbors])

def normonize(ds, attrs, c_range):
    #data = deepcopy(ds)
    data = ds[:]
    cols = {}
    col_max = {}
    col_min = {}
    for i in c_range:
        cols[i] = [float(d[attrs[i]]) for d in data]
        col_max[i] = max([col for col in cols[i]])
        col_min[i] = min([col for col in cols[i]])
    for i in range(len(data)):
        for j in c_range:
            if not col_max[j]==col_min[j]:
                data[i][attrs[j]] = (float(data[i][attrs[j]]) - col_min[j]) / (col_max[j] - col_min[j])
            else:
                data[i][attrs[j]] = 0.0
    return data
	
if __name__ == "__main__":
    filename = sys.argv[1]
    k = int(sys.argv[2])

    data, attributes, target_attr = get_data(filename)
    n = len(data)

    accs = []
    for i in range(5):
        valid_data = deepcopy(data[int(float(n)/5*i):int(float(n)/5*(i+1))]) #validation data
        train_data = deepcopy([d for d in data if not d  in valid_data]) #training data
        labels = [d[target_attr] for d in valid_data]

	    #preprocess data
        if filename == "breast-cancer-wisconsin.data":
            c_range = range(5)
            selected_attrs = [attributes[i] for i in c_range]
            train_data = normonize(train_data, attributes, c_range)
            valid_data = normonize(valid_data, attributes, c_range)
        elif filename == "car.data":
            cols = [{"vhigh":1, "high":2, "med":3, "low":4},
                    {"vhigh":1, "high":2, "med":3, "low":4},{},{},
                    {"small":1, "med":2, "big":3},
                    {"low":1, "med":2, "high":3}]
            c_range = range(6)
            for i in range(len(train_data)):
                for j in c_range:
                    if j==2:
                        if train_data[i][attributes[2]]=="5more":
                            train_data[i][attributes[2]] = 6
                    elif j==3:
                        if train_data[i][attributes[3]]=="more":
                            train_data[i][attributes[3]] = 6
                    else:
                        train_data[i][attributes[j]] = cols[j][train_data[i][attributes[j]]]
            for i in range(len(valid_data)):
                for j in c_range:
                    if j==2:
                        if valid_data[i][attributes[2]]=="5more":
                            valid_data[i][attributes[2]] = 6
                    elif j==3:
                        if valid_data[i][attributes[3]]=="more":
                            valid_data[i][attributes[3]] = 6
                    else:
                        valid_data[i][attributes[j]] = cols[j][valid_data[i][attributes[j]]]
            selected_attrs = [attributes[i] for i in c_range]
            train_data = normonize(train_data, attributes, c_range)
            valid_data = normonize(valid_data, attributes, c_range)
        elif filename == "ecoli.data":
            c_range = (1,2,5,6,7)
            selected_attrs = [attributes[i] for i in c_range]
            train_data = normonize(train_data, attributes, c_range)
            valid_data = normonize(valid_data, attributes, c_range)
        elif filename == "mushroom.data":
            c_range = range(1, 9)
            cols = [{},{"b":1, "c":2, "x":3, "f":4, "k":5, "s":6},
                    {"f":1, "g":2, "y":3, "s":4},
                    {"n":1, "b":2, "c":3, "g":4, "r":5, "p":6, "u":7, "e":8, "w":9, "y":10},
                    {"t":1, "f":2}, {"a":1, "l":2, "c":3, "y":4, "f":5, "m":6, "n":7, "p":8, "s":9},
                    {"a":1, "d":2, "f":3, "n":4}, {"c":1, "w":2, "d":3}, {"b":1, "n":2}]
            selected_attrs = [attributes[i] for i in c_range]
            for i in range(len(train_data)):
                for j in c_range:
                    train_data[i][attributes[j]] = cols[j][train_data[i][attributes[j]]]
            for i in range(len(valid_data)):
                for j in c_range:
                    valid_data[i][attributes[j]] = cols[j][valid_data[i][attributes[j]]]
            train_data = normonize(train_data, attributes, c_range)
            valid_data = normonize(valid_data, attributes, c_range)
        elif filename == "letter-recognition.data":
            c_range = range(1, 17)
            selected_attrs = [attributes[i] for i in c_range]
            train_data = normonize(train_data, attributes, c_range)
            valid_data = normonize(valid_data, attributes, c_range)

        classification = []
        for d in valid_data:
            neighbors = get_neighbors(train_data, d, k, selected_attrs)
            c = kNN_classifier(neighbors, target_attr)
            classification.append(c)
        count = 0
        for x,y in zip(classification, labels):
            if x==y:
                count += 1
        acc = float(count)/len(classification)
        accs.append(acc)
        print("accuracy: " + str(100*acc) + "%")
    print("standard deviation: " + str(std_dev(accs)))