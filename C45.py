import math

import sys


class decisionTreeNode():
    def __init__(self, is_leaf_node, classification, attribute_split_index,partition_set, attribute_split_value, parent, height):
        self.classification = classification
        self.attribute_split_gain = None
        self.attribute_split_column = None
        self.attribute_split_character_list = None
        self.partition_set = partition_set
        self.children = []
        self.parent = parent
        self.height = None
        self.is_leaf_node = True

def create_decision_tree(training_set,set_attributes, parent):

    if not training_set:
        classification = count_parent_classifications(parent)
        node = decisionTreeNode(True, classification, None,None,None,parent,0)
        return node

    node = decisionTreeNode(True, None, None,None, None, parent, 0)
    if parent == None:
        node.height = 0
    else:
        node.height = node.parent.height + 1
    if len(set_attributes) >=1:
        node.is_leaf_node = False

    set_attribute_index = 0
    entropy = calculate_gain(training_set, set_attributes, set_attribute_index)


    splitting_attribute = None

    maximum_info_gain = 0
    column = 0
    character_list = []

    #for each column of data we have. Will have to remove columns we have already split on.
    for attribute_index in range(1,len(set_attributes)):
        if(set_attributes[attribute_index] != 0):
            outer_loop_gain = 0

            list_of_column_attributes = set_attributes[attribute_index]
        if len(list_of_column_attributes) <=1:
            continue
        #now we calculate the gain for each column and save the maximum
        for attr in list_of_column_attributes:
            outer_loop_gain += specific_conditional_entropy(training_set, attr, attribute_index,set_attributes)


        column_gain = calculate_gain(training_set,set_attributes,attribute_index)
        outer_loop_gain = (entropy - outer_loop_gain) / (column_gain + 0.0000001)
        if outer_loop_gain > maximum_info_gain:
            maximum_info_gain = outer_loop_gain
            column = attribute_index
            character_list = list_of_column_attributes
    if maximum_info_gain == 0:
        classification = determine_classification(training_set)
        node = decisionTreeNode(True, classification, None,None,None,parent,0)
        return node
    node.attribute_split_character_list = character_list
    node.attribute_split_column = column
    node.attribute_split_gain = maximum_info_gain
    node.partition_set = training_set
    for character in character_list:
        smaller_set = []
        for line in training_set:
            if line[column] == character:
                smaller_set.append(line)

                #remove attributes not going to be used in recursive call.

        child_attribute_set = set_attributes[:]
        child_attribute_set.pop(column)
        empty_list = []
        child_attribute_set.insert(column,empty_list)




        node.children.append(create_decision_tree(smaller_set,child_attribute_set,node))
    return node


def print_tree(node):
    if node.is_leaf_node:
        classification = node.classification
        print('Found a leaf! This leaf is predicted to be: '+classification)
        return
    elif node.parent == None:
        print('This is the root node. splitting on ' + str(node.attribute_split_column))
        print("\n")
        index = 0
        for character in node.attribute_split_character_list:
            print('Traversing to ' + character)
            print_tree(node.children[index])
            index += 1
    elif node.parent != None:
        print('This node in the tree will split on ' + str(node.attribute_split_column))
        index = 0
        for character in node.attribute_split_character_list:
            print('Traversing to ' + character)
            print_tree(node.children[index])
            index += 1

def predict(data, node):
    classified_data = []

    for line in data:
        prediction = classify_line(line, node)
        line.insert(0,prediction)
        classified_data.append(line)
    x = 4
    return classified_data

def classify_line(line, node):

    next = None

    while node.is_leaf_node is False:
        split_column = node.attribute_split_column
        index = 0
        for character in node.attribute_split_character_list:
            if line[split_column-1] == character:
                next = node.children[index]
                node = next
                break
            index += 1
    prediction = node.classification
    return prediction




def determine_classification(training_set):
    set_to_count = training_set
    p = 0
    e = 0
    for line in set_to_count:
        if line[0] == "p":
            p += 1
        else:
            e += 1
    if p > e:
        return "p"
    else:
        return "e"

def count_parent_classifications(parent_node):
    set_to_count = parent_node.partition_set
    p = 0
    e = 0
    for line in set_to_count:
        if line[0] == "p":
            p+=1
        else: e+=1
    if p > e:
        return "p"
    else: return "e"


def specific_conditional_entropy(data_set, attribute, column,set_attributes):
    count = 0
    smaller_dataset = []

    for line in data_set:
        if line[column] == attribute and line[0] == "p":
            smaller_dataset.append(line)
        elif line[column] == attribute and line[0] == "e":
            smaller_dataset.append(line)
    total_small_dataset_lines = len(smaller_dataset)
    total_dataset_lines = len(data_set)
    if total_small_dataset_lines == 0:
        return 0
    attribute_entropy = 0
    attribute_entropy += calculate_gain(smaller_dataset,set_attributes,0) * total_small_dataset_lines/total_dataset_lines
    return attribute_entropy





def calculate_gain(data_set, set_attributes, set_attribute_index):

    gain = 0
    for classifier in set_attributes[set_attribute_index]:
        attribute_count = count_attribute_occurence(data_set, classifier,set_attribute_index)

        total_rows = len(data_set)

        p = attribute_count / total_rows

        if (p!= 0 ):
            gain += p * math.log(p,2)


    gain = -gain
    return gain



def count_attribute_occurence(data_set, attribute,set_attribute_index):
    index = set_attribute_index
    count = 0
    for line in data_set:
        if (line[index] == attribute):
            count += 1

    return count

def accuracy_test(test_data,accuracy_test_set):
    count = 0
    for i in range(len(test_data)):
        if test_data[i][0] == accuracy_test_set[i][0]:
            count += 1

    return count / len(test_data)

def output_results(count, predicted_list, output):
    out = open(output, "w+")
    out.write("Using the given test file we have " + str(count) + "% accuracy\n")
    index = 1
    for line in predicted_list:
        predicted_label = line[0]
        out.write("Predicted label for row " + str(index) + " is: " + predicted_label + ". The whole line is: " + str(line))
        out.write("\n")
        index += 1
def run_decision_tree(training,testing,output):

        data = open(training)
        training_set = []
        training_set_attributes = []
        temp_set = []

        for line in data:
            training_set += [line.split()]

        columns = len(training_set[0])
        index = 0
        for i in range(0, columns):
            temp_set = []
            for line in training_set:
                if line[index] not in temp_set:
                    temp_set.append(line[index])
            index += 1
            training_set_attributes.append(temp_set)


        root = create_decision_tree(training_set,training_set_attributes, None)


        test_tree_data = open(testing)
        test_set = []
        accuracy_test_set = []
        for line in test_tree_data:
            accuracy_test_set += [line.split()]
        for line in accuracy_test_set:
            test_set += [line[1:]]


        predicted_list = predict(test_set,root)
        count = accuracy_test(predicted_list,accuracy_test_set)
        count = count * 100




        output_results(count, predicted_list, output)



if __name__ == "__main__":


    training_data = sys.argv[1]
    testing_data = sys.argv[2]
    output_file = sys.argv[3]

    run_decision_tree(training_data,testing_data,output_file)




