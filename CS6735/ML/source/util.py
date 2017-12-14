import sys
from attrs import attrs
from targets import targets
from math import sqrt

def std_dev(l):
    mean = lambda a: float(sum(a))/len(a)
    m = mean(l)
    return sqrt(mean([(x - m)**2 for x in l]));

def print_tree(tree):
    print(tree)

def vote(l):
    l = l[:]
    f = 0
    most_freq_v = None
    for v in unique(l):
        if l.count(v) > f:
            f = l.count(v)
            most_freq_v = v
    return most_freq_v

def unique(l):
    return list(set(l))

def get_data(filename):
    try:
        f = open(filename, "r")
    except IOError:
        print("error open file '%s'" % filename)
        sys.exit(0)
    else:
        instances = [l.strip() for l in f.readlines()]
        f.close()
    if filename == "breast-cancer-wisconsin.data": #first column is irrelavant
        instances = [instance.split(',')[1:] for instance in instances]
        for i,instance in enumerate(instances):
            if instance[5]=="?":
                if instance[-1]=="2":
                    instances[i][5] = 1
                else:
                    instances[i][5] = 10
    else:
        instances = [instance.split(',') for instance in instances]
    attributes = attrs[filename]
    target_attr = attributes[targets[filename]]
    data = [dict(zip(attributes, instance)) for instance in instances]
    return (data, attributes, target_attr)