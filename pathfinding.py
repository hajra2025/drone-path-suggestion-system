import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_path(grid, start, goal, distance_weight, risk_weight):
    rows, cols = len(grid), len(grid[0])

    pq = []
    heapq.heappush(pq, (0, start))

    came_from = {}
    cost_so_far = {}

    came_from[start] = None
    cost_so_far[start] = 0

    while pq:
        _, current = heapq.heappop(pq)

        if current == goal:
            break

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy

            if 0 <= nx < rows and 0 <= ny < cols:

                # obstacle 
                if grid[nx][ny] == 1:
                    continue

                # base cost
                new_cost = cost_so_far[current] + distance_weight

                # risk penalty
                if grid[nx][ny] == 2:
                    new_cost += risk_weight * 10

                if (nx, ny) not in cost_so_far or new_cost < cost_so_far[(nx, ny)]:
                    cost_so_far[(nx, ny)] = new_cost
                    priority = new_cost + heuristic((nx, ny), goal)
                    heapq.heappush(pq, (priority, (nx, ny)))
                    came_from[(nx, ny)] = current

    # reconstruct path
    path = []
    node = goal

    if node not in came_from:
        return []

    while node:
        path.append(node)
        node = came_from[node]

    path.reverse()
    return path