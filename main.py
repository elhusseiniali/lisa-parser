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
        predecessors = list(G.predecessors(x[0]))
        print("predecessors: ", predecessors)
        print("successors: ", successors)
        if "read" in label:
            file_name = re.findall(r"'\s*([^']+?)\s*'", label)
            print(Read(file_name))
        else:
            column_name = re.findall(r"'\s*([^']+?)\s*'", label)
            if column_name:
                print("column_name: ", column_name)
                if "project" in label:
                    column_name = re.findall(r"'\s*([^']+?)\s*'", label)
                    current_node = Projection(column_name=column_name)
                    print(current_node)
                elif "assign_to" in label:
                    column_name = re.findall(r"'\s*([^']+?)\s*'", label)
                    current_node = Projection(column_name=column_name)
                    print("&&&&&&&&&&&&&&&")
                    print(current_node)
                    for predecessor in predecessors:
                        print((predecessor, data[predecessor]))
                        p_label = clean_str(dict(data[predecessor])['label'])
                        print("p_label: ", p_label)
                        result = re.findall(r"'\s*([^']+?)\s*'", p_label)
                        print("result: ", result)
                        for name in column_name:
                            analysis.current["must"].add(name)
                            analysis.current["may"].add(name)
                        if not any(i in column_name for i in result):
                            for name in column_name:
                                analysis.current["must"].add(name)
                                analysis.current["may"].add(name)

                                analysis.added["may"].add(name)
                    print("&&&&&&&&&&&&&&&")

        # for successor in successors:
        #    print((successor, data[successor]))
        print("***********")
    with open(result_file_name, 'w') as writer:
        writer.write(pprint.pformat(str(analysis)))
    # print(analysis)


if __name__ == "__main__":
    main()
