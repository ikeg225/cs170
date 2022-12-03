import random

# Start writing code here...
def solve(G: nx.Graph):
    # TODO implement this function with your solver
    # Assign a team to v with G.nodes[v]['team'] = team_id
    # Access the team of v with team_id = G.nodes[v]['team']
    k = random.randint(1, len(G.nodes))
    l = list(range(1, k + 1))
    random.shuffle(l)
    for node in G.nodes:
        if l:
            G.nodes[node]['team'] = l[0]
            l = l[1:]
        else:
            G.nodes[node]['team'] = random.randint(1, k)
    current = score(G)
    temp = 10000000
    #change
    while temp > 0.0001:
        D = []
        L = []
        Doriginal = []
        currentTeams = [0]*len(G.nodes)
        for node in G.nodes:
            currentTeams[node] = G.nodes[node]['team']
        for node in G.nodes:
            #change
            if random.uniform(0, 1) < .3:
                #change
                if random.uniform(0, 1) < 0.05:
                    #1/max(currentTeams):
                    D.append(node)
                    L.append(max(currentTeams) + 1)
                elif max(currentTeams) > 1:
                    D.append(node)
                    new_team = random.randint(1, max(currentTeams))
                    while new_team == G.nodes[node]['team']:
                        new_team = random.randint(1, max(currentTeams))
                    L.append(new_team)
        newCost = partc(G, D, L)
        # changed from newCost - current => current - netCost (gets rid of math.exp error)
        deltaE = current - newCost
        if newCost < current or random.uniform(0, 1) < math.exp(deltaE/temp):
            current = newCost
        else:
            for node in G.nodes:
                G.nodes[node]['team'] = currentTeams[node]
        #change
        temp = temp * .99
    # prints out the calculated cost
    # minTeam = float('inf')
    # for node in G.nodes:
    #     minTeam = min(minTeam, G.nodes[node]['team'])
    # for node in G.nodes:
    #     G.nodes[node]['team']
    print(current)
    return G

G = read_input('inputs/large36.in')
solve(G)
print("Nodes in G: ", G.nodes(data=True))
validate_output(G)

visualize(G)
score(G)