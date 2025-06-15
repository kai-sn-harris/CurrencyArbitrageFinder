import math


def ArbitrageFinder(currencies, exchange_rates, start_amount):

    n = len(currencies)

    # making into log to make it adding rather then mulitplying
    log_graph = [[-math.log(exchange_rates[i][j]) if exchange_rates[i][j] > 0 else float('inf') for j in range(n)] for i in range(n)]

    next_node = [[j for j in range(n)] for i in range(n)]

    # Floyd–Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if log_graph[i][k] + log_graph[k][j] < log_graph[i][j]:
                    log_graph[i][j] = log_graph[i][k] + log_graph[k][j]
                    next_node[i][j] = next_node[i][k]

    for start in range(n):
        if log_graph[start][start] < 0: # if profit is made
            cycle = [start]

            visited = set()

            while True:
                next_i = next_node[cycle[-1]][start]
                if next_i in visited:
                    idx = cycle.index(next_i)
                    cycle = cycle[idx:] + [cycle[idx]]  # Close the loop
                    break
                visited.add(next_i)
                cycle.append(next_i)

            # Simulate arbitrage
            amount = start_amount
            for i in range(len(cycle) - 1):
                from_idx = cycle[i]
                to_idx = cycle[i + 1]
                rate = exchange_rates[from_idx][to_idx]
                amount *= rate

            return {
                "path": [currencies[i] for i in cycle],
                "starting_amount": start_amount,
                "final_amount": amount,
                "profit": amount - start_amount
            }

    return None 


currencies = ["USD", "EUR", "GBP"]
exchange_rates = [
    [1.0, 0.9, 0.75],
    [1.1, 1.0, 0.83],
    [1.35, 1.2, 1.0]
]

result = ArbitrageFinder(currencies,exchange_rates,10_0000)

print(result)
