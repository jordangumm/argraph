import networkx
import obonet

graph = obonet.read_obo('data/aro.obo')

print(graph.graph)

for i, node in enumerate(graph):
    print(node)
    print(graph[node])

    if i == 20:
        break

print(graph['ARO:3000185'])
