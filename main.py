import networkx as nx
from operations import Read, Projection, Conversion, Assignment
import re
from domain import ColumnDomain

import pprint


def clean_str(input_string):
    return input_string.replace("&quot;", "'")


def separate_graph(input_graph):
    node_data = input_graph.nodes.data()
    descendants = {}

    for x in node_data:
        node_name = x[0]
        label = clean_str(x[1]['label'])

        if "read" in label:
            file_name = re.findall(r"'\s*([^']+?)\s*'", label)[0]

            descendants[str(file_name)] = list(
                nx.descendants(input_graph, source=node_name))
    return descendants


def process_graph(input_graph):
    node_table = {}
    node_data = input_graph.nodes.data()

    descendants = separate_graph(input_graph)

    analysis = {}
    for key in descendants.keys():
        analysis[key] = ColumnDomain()

    for x in node_data:
        node_name = x[0]
        label = clean_str(x[1]['label'])

        predecessors = list(input_graph.predecessors(node_name))
        edge_data = input_graph.edges.data()

        if "read" in label:
            file_name = re.findall(r"'\s*([^']+?)\s*'", label)
            node_table[node_name] = Read(file_name)
        else:
            column_name = re.findall(r"'\s*([^']+?)\s*'", label)
            for dataframe in descendants.keys():
                if node_name in descendants[dataframe]:
                    current_dataframe = dataframe

            if column_name:
                if "project" in label:
                    node_table[node_name] = Projection(
                        column_name=column_name[0])

                    analysis[current_dataframe].\
                        current["must"].add(column_name[0])
                    analysis[current_dataframe].\
                        current["may"].add(column_name[0])

                elif "assign_to" in label:
                    for predecessor in predecessors:
                        # print((predecessor, node_data[predecessor]))
                        p_name = predecessor

                        for y in edge_data:
                            if (p_name == y[0] and node_name == y[1]):
                                edge = y
                                edge_color = y[2]['color']

                                if edge_color == 'blue':
                                    value = edge[0]
                                    value_column_name = clean_str(
                                        dict(node_data[value])['label'])
                                    result = re.findall(r"'\s*([^']+?)\s*'",
                                                        value_column_name)
                                    for name in column_name:
                                        analysis[current_dataframe]\
                                            .current["must"].add(name)
                                        analysis[current_dataframe]\
                                            .current["may"].add(name)
                                    if not any(i in column_name
                                               for i in result):
                                        for name in column_name:
                                            analysis[current_dataframe]\
                                                .added["may"].add(name)
                        node_table[node_name] = Assignment(
                            column_name=column_name, value=value)

                elif "assign" in label:
                    for name in column_name:
                        analysis[current_dataframe]\
                            .current["must"].add(name)
                        analysis[current_dataframe]\
                            .current["may"].add(name)

                elif "TO_DATETIME" in label or "TO_GEOCODE" in label:
                    # if column_name wasn't added, then it must be in the
                    # original file
                    node_table[node_name] = Conversion(column_name)
                    for name in column_name:
                        analysis[current_dataframe]\
                            .current["must"].add(name)
                        analysis[current_dataframe]\
                            .current["may"].add(name)

                        if not analysis[current_dataframe].was_added(name):
                            analysis[current_dataframe]\
                                .original["must"].add(name)
                            analysis[current_dataframe]\
                                .original["may"].add(name)

    return analysis


def build_graph(node_table, edge_data):
    pass


def main(input_file="./data/df3.dot"):
    G = nx.drawing.nx_agraph.read_dot(input_file)

    analysis = process_graph(G)
    for dataframe in analysis.keys():
        print(dataframe, ": ", analysis[dataframe])

    result_file_name = 'output.txt'
    with open(result_file_name, 'w') as writer:
        for dataframe in analysis.keys():
            writer.write("----")
            writer.write(dataframe)
            writer.write(": \n")
            writer.write(pprint.pformat(str(analysis[dataframe])))
            writer.write("\n\n")


if __name__ == "__main__":
    main()
