from id3 import infogain
from util import unique, vote


def get_values(data, attr):
    data = data[:]
    return unique([record[attr] for record in data])

def choose_attribute(data, attributes, target_attr):
    data = data[:]
    best_gain = 0.0
    best_attr = None
    for attr in attributes:
        gain = infogain(data, attr, target_attr)
        if (gain >= best_gain and attr != target_attr):
            best_gain = gain
            best_attr = attr  
    return best_attr

def get_sub_dataset(data, best, value):
    data = data[:]
    return [record for record in data if record[best] == value]

def classify_record(tree, record, default):
    if type(tree) == type("string"): #leaf node
        return tree
    else:
        attr = list(tree.keys())[0]
        if(record[attr] in tree[attr]):
            t = tree[attr][record[attr]]
        else:
            #cannot find the path with this value, can return a random class
            return default
        return classify_record(t, record, default)

def classify_decision_tree(tree, data, default, params=None):
    data = data[:]
    return [classify_record(tree, record, default) for record in data]

def create_decision_tree(data, attributes, target_attr, params=None):
    data = data[:]
    target_vals = [record[target_attr] for record in data]
    default = vote(target_vals)
    if len(data)<=20 or len(attributes) <= 1: #we stop early to prevent overfitting
        return default
    elif target_vals.count(target_vals[0]) == len(target_vals): #all True or all False
        return target_vals[0]
    else:
        best = choose_attribute(data, attributes, target_attr)
        tree = {best:{}}
        for val in get_values(data, best):
            subtree = create_decision_tree(
                get_sub_dataset(data, best, val),
                [attr for attr in attributes if attr != best],
                target_attr, default)
            tree[best][val] = subtree
    return tree
