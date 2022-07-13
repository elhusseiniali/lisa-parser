import networkx as nx
from operations import Read, Projection, ToDatetime, Assignment
import re
from domain import ColumnDomain

import pprint


def clean_str(input_string):
    return input_string.replace("&quot;", "'")


def main(input_file="./data/df3.dot"):
    G = nx.drawing.nx_agraph.read_dot(input_file)
    data = G.nodes.data()

    analysis = ColumnDomain()
    result_file_name = 'output.txt'

    for x in data:
        print(x)
        label = clean_str(x[1]['label'])
        print("label: ", label)

        successors = list(G.successors(x[0]))
        if "read" in label:
            file_name = re.findall(r"'\s*([^']+?)\s*'", label)
            print(Read(file_name))
        elif "project" in label:
            column_name = re.findall(r"'\s*([^']+?)\s*'", label)
            current_node = Projection(column_name=column_name)
            print(current_node)
        elif "assign_to" in label:
            column_name = re.findall(r"'\s*([^']+?)\s*'", label)
            current_node = Projection(column_name=column_name)
            print("&&&&&&&&&&&&&&&")
            print(current_node)
            for successor in successors:
                print((successor, data[successor]))
                successor_label = clean_str(dict(data[successor])['label'])
                result = re.findall(r"'\s*([^']+?)\s*'", successor_label)
                print(result)
                for name in column_name:
                    analysis.current["must"].add(name)
                    analysis.current["may"].add(name)
                if column_name in result:
                    print(True)
                else:
                    for name in column_name:
                        analysis.current["must"].add(name)
                        analysis.current["may"].add(name)

                        analysis.added["may"].add(name)
                    print(False)
            print("&&&&&&&&&&&&&&&")
        else:
            column_name = re.findall(r"'\s*([^']+?)\s*'", label)
            if column_name:
                print("column_name: ", column_name)
                for name in column_name:
                    analysis.current["must"].add(name)
                    analysis.current["may"].add(name)

                    analysis.original["must"].add(name)
                    analysis.original["may"].add(name)
            if "assign_to" in label:
                print("###############")
                print(successors)
                for successor in successors:
                    print((successor, data[successor]))
                print("###############")

        print("***********")
    with open(result_file_name, 'w') as writer:
        writer.write(pprint.pformat(str(analysis)))
    # print(analysis)


if __name__ == "__main__":
    main()
