import sys

# Calculates what teams are still challenging and which have been eliminated
def team_standings(teams, games):
    rankings = {'challenging': [], 'eliminated': []}
    source_node ='source'
    sink_node = 'sink'
    total_points = {}

    for team in teams:
        # Calculates the total number of points a team can earn
        total_points[team] = teams[team]['points'] + (teams[team]['remaining'] * 3)

    for team in teams:
        graph = {}
        max_points = 0 

        # Builds graph for each team's matches
        for teamx, teamy in games:
            if teamx != team and teamy != team:
                match_id = f"{teamx}-{teamy}"
                graph_edge(graph, source_node, match_id, 3)
                # Connects teams x and y nodes with "infinite" capacity
                graph_edge(graph, match_id, teamx, float(4000))
                graph_edge(graph, match_id, teamy, float(4000))
                # Adds 3 points for a win
                max_points += 3

        for opponent in teams:
            if team != opponent:
                # Max number of points the current team can earn in remaining matches
                max_points_possible = total_points[team] - teams[opponent]['points']
                # Adds graph edge from opponent team to sink node
                graph_edge(graph, opponent, sink_node, max_points_possible)

        # Calculates the max flow from the source node to sink
        max_flow = ford_fulkerson(graph, source_node, sink_node)

        if max_points <= max_flow:
            # Team is still challenging if their max possible points from remaining games does not exceed max flow
            rankings['challenging'].append((team, teams[team]['points'], max_flow))
        else:
            # Team is eliminated as there are not enough remianing matches for them to earn points to catch up
            message = '(as it cannot catch up)'
            rankings['eliminated'].append((team, teams[team]['points'], message))

    return rankings

# Creates graph edge using a starting and ending node and edge capacity
def graph_edge(graph, start_node, end_node, capacity):
    if start_node not in graph:
        graph[start_node] = {}

    if end_node not in graph:
        graph[end_node] = {}
    
    # Main graph flow edge
    graph[start_node][end_node] = capacity
    # Reversed edge
    graph[end_node][start_node] = 0

# Determines the maximum flow from the source node to the sink
def ford_fulkerson(graph, source_node, sink_node):
    prev_node = {}
    max_flow = 0

    # Finds an augmenting path from the sink to the 
    while dfs(graph, source_node, sink_node, prev_node):
        path = float(4000)
        t = sink_node

        # Finds the minimum edge on the path
        while t != source_node:
            path = min(path, graph[prev_node[t]][t])
            t = prev_node[t]

        v = sink_node
        # Updates residual edges on the path
        while v != source_node:
            u = prev_node[v]
            # Subtracts the residual capacities from each edge on the path
            graph[u][v] = graph[u][v] - path
            # Adds the residual capacities from each reverse edge on the path
            graph[v][u] = graph[v][u] + path
            v = prev_node[v]

        max_flow += path

    return max_flow

# Checks for path in residual graph between source node and the sink
def dfs(graph, source_node, sink_node, prev_node):
    stack = [source_node]
    visited = set()
    # Creates source node for graph
    visited.add(source_node)
    prev_node[source_node] = None

    while stack:
        current_node = stack.pop()

        # Traverse each node adjacent to the current node
        for adjacent_node, capacity in graph[current_node].items():
            # Checks for residual edge capacity and whether the adjacent node has been visited
            if capacity > 0 and adjacent_node not in visited:
                prev_node[adjacent_node] = current_node
                # Marks adjacent_node node as visited and adds to queue
                visited.add(adjacent_node)
                stack.append(adjacent_node)
                # Sink node is reached
                if adjacent_node == sink_node:
                    return True
    # Sink is not reached
    return False
    

if __name__ == "__main__":
    input = sys.argv[1]
    output = sys.argv[2]

    with open(input, 'r') as file:
        teams = {}
        games = []
        # Reads the total number of teams in tournament
        n = int(file.readline().strip())
        
        for _ in range(n):
            # Reads in each team name and their score
            team_name = file.readline().strip()
            score = int(file.readline().strip())

            # Creates a dictionary of teams and team information
            teams[team_name] = {'points': score, 'remaining': 0, 'total_points': score}

        # Reads in the number of remaining matches
        m = int(file.readline().strip())
        
        for _ in range(m):
            # Reads in the two teams names competing in a match
            team1 = file.readline().strip()
            team2 = file.readline().strip()
            # Tracks each team match up
            games.append((team1, team2))
            # Counts the number of remaining games for each team 
            teams[team1]['remaining'] += 1
            teams[team2]['remaining'] += 1

        for team in teams:
            # Calculates the total points a team can make (wins count as 3 points)
            teams[team]['total_points'] += teams[team]['remaining'] * 3

    rankings = team_standings(teams, games)

    with open(output, 'w') as f:
        # Prints teams that are still challenging, sorted based on current scores
        f.write("Teams still challenging are... \n")
        for team, score, flow_value in sorted(rankings['challenging'], key=lambda x:(-x[1])):
            f.write(f"{team} {score} (flow = {flow_value}) \n")

        # Prints teams that have been eliminated
        f.write("\nTeams that have been eliminated are... \n")
        for team, score, message in sorted(rankings['eliminated'], key=lambda x:(x[1], x[0]), reverse=True):
            f.write(f"{team} {score} {message} \n")