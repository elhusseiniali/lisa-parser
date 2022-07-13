import networkx as nx
from operations import Read, Projection, ToDatetime
import re
from domain import ColumnDomain


def clean_str(input_string):
    return input_string.replace("&quot;", "'")


def main(input_file="./data/df5.dot"):
    G = nx.drawing.nx_agraph.read_dot(input_file)
    data = G.nodes.data()

    analysis = ColumnDomain()

    for x in data:
        print(x)
        label = clean_str(x[1]['label'])
        print("label: ", label)

        successors = list(G.successors(x[0]))

        if "read" in label:
            file_name = re.findall(r"'\s*([^']+?)\s*'", label)
            print(Read(file_name))
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
    # print(analysis)


if __name__ == "__main__":
    main()
