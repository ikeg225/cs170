import numpy as np
import math
from constants import score

#returns new Cp value
def cp(b_vector, i, j, norm_b, v):
    return math.exp(70 * np.sqrt((norm_b) ** 2) - (b_vector[i] ** 2) - (b_vector[j] ** 2) + ((b_vector[i] - (1 / v)) ** 2) + ((b_vector[j] + (1 / v)) ** 2))

#returns change in Cw
def cw(G, i, j, v):
    s = 0
    for edge in G.edges(data=True):
        if edge[1] == v:
            if G.nodes[edge[0]]['team'] == i:
                s -= edge[2]['weight']
            elif G.nodes[edge[0]]['team'] == j:
                s += edge[2]['weight']
        elif edge[0] == v:
            if G.nodes[edge[1]]['team'] == i:
                s -= edge[2]['weight']
            elif G.nodes[edge[1]]['team'] == j:
                s += edge[2]['weight']
    return s
    
def partc(G, D, L):
    C_w, C_k, C_p = score(G, True)
    output = [G.nodes[v]['team'] for v in range(G.number_of_nodes())]
    np.sort(output)
    teams, counts = np.unique(output, return_counts=True)
    k = np.max(teams)
    b = (counts / G.number_of_nodes()) - 1 / k
    C_k = 100*math.exp(0.5*k)
    for i in range(len(D)):
        #check to see if it will remove team
        team_i = G.nodes[D[i]]['team'] - 1
        team_j = L[i] - 1
        if abs(b[team_i] - (1/len(G.nodes) - 1/k)) < 0.0001 and L[i] > k:
            continue
        elif abs(b[team_i] - (1/len(G.nodes) - 1/k)) < 0.0001:
            b = b + (1 / k) - (1 / (k - 1)) 
            k -= 1 
            C_p = math.exp(70*math.sqrt(np.linalg.norm(b, 2)**2 - b[team_i]**2 - b[team_j]**2 + (b[team_j] + 1/len(G.nodes))**2))
            C_w += cw(G, G.nodes[D[i]]['team'], L[i], D[i])
            C_k = 100*math.exp(0.5*k)
            b[team_j] += 1/len(G.nodes)
            b = np.delete(b, team_i)
            G.nodes[D[i]]['team'] = L[i]
            for node in G.nodes:
                if G.nodes[node]['team'] > team_i + 1:
                    G.nodes[node]['team'] -= 1
            for team in range(len(L)):
                if L[team] > team_i + 1:
                    L[team] -= 1
        elif L[i] > k:
            b = b + (1 / k) - (1 / (k + 1))
            b = np.append(b, [-1/(k + 1)])
            k += 1
            C_p = cp(b, team_i, team_j, np.linalg.norm(b, 2), len(G.nodes))
            C_w += cw(G, G.nodes[D[i]]['team'], L[i], D[i])
            C_k = 100*math.exp(0.5*k)
            b[team_i] -= 1/len(G.nodes)
            b[team_j] += 1/len(G.nodes)
            G.nodes[D[i]]['team'] = L[i]

        else:
            C_p = cp(b, G.nodes[D[i]]['team'] - 1, L[i] - 1, np.linalg.norm(b, 2), len(G.nodes))
            C_w += cw(G, G.nodes[D[i]]['team'], L[i], D[i])
            b[team_i] -= 1/len(G.nodes)
            b[team_j] += 1/len(G.nodes)
            G.nodes[D[i]]['team'] = L[i]
    return C_w + C_k + C_p
