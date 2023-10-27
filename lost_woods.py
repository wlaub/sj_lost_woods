import itertools

import igraph
#adj = [
#'l1s': ['r2f', 'l4f', 'l5f'],
#'l1w': ['r2f', 'l4f', 'l5f'],
#'l1f': ['r2w', 'l4w', 't8w', 'l3w'],
#'l2s': []
#]

adj = {
'as': ['bf'],
'af': ['bw'],
'aw': ['bw'],
'aus': ['bw','bf'],
'auf': ['bs','bw'],
'auw': ['bs','bw'],
'bs': ['af', 'flf', 'auw', 'bw'],
'bf': ['aw', 'aus', 'fls', 'bw'],
'bw': ['af', 'aus', 'fls', 'ds', 'ef'],
'cs': ['bw', 'df'],
'cf': ['bw','ds', 'ew'],
'ds': ['cf','bf'],
'df': ['cs'],
'dw': ['cs', 'bs'],
'es': ['bw', 'ef', 'ew', 'frw'],
'ef': ['bw', 'ew', 'frs'],
'ew': ['cf', 'ef', 'es', 'frs'],
'fls': ['bf'],
'flf': ['bs'],
'flw': ['bs'],
'frs': ['bf','ew'],
'frf': ['bs','es'],
'frw': ['bs','es'],
}

node_map = {x:i for i,x in enumerate(adj.keys())}
node_map_rev = {i:x for i,x in enumerate(adj.keys())}
node_count = len(adj.keys())

start = 'as'
targets = ['frw', 'cf', 'bs']
end = 'aus'

edges = []
for source, dests in adj.items():
    for dest in dests:
        edges.append((node_map[source], node_map[dest]))

g = igraph.Graph(n=node_count, edges=edges, directed=True)


sequences = []
for order in itertools.permutations(targets):
    seq = (start, *order, end)
    sequences.append(seq)

path_map = {}
for seq in sequences:
    path_map[seq] = []
    for start, stop in zip(seq[:-1], seq[1:]):
        start = node_map[start]
        stop = node_map[stop]
        res = g.get_shortest_path(start, stop)
        res = [node_map_rev[x] for x in res]
        if len(path_map[seq]) > 0 and res[0] == path_map[seq][-1]:
            res = res[1:]
        path_map[seq].extend(res)

best = sorted(path_map.items(), key=lambda x: len(x[1]))
for seq, path in best:
    print(len(path), path)

