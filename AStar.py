import pygame
import config
import heapq  # 用於實現優先隊列

class AStarSolver:
    def __init__(self, maze, cell_size, win):
        self.maze = maze
        self.cell_size = cell_size
        self.win = win

    def solve_with_animation(self, start, goal, player):
        # 優先隊列，用來存儲節點的 f 值與節點
        priority_queue = []
        heapq.heappush(priority_queue, (0, start))  # (f 值, 節點)
        visited = set()
        parent = {start: None}
        g_scores = {start: 0}  # g 值，即起點到當前節點的代價

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # 上下左右

        def heuristic(node, goal):
            """啟發式函數，使用曼哈頓距離"""
            x1, y1 = node
            x2, y2 = goal
            return abs(x1 - x2) + abs(y1 - y2)

        while priority_queue:
            current_f, current = heapq.heappop(priority_queue)

            if current in visited:
                continue
            visited.add(current)

            # 動畫：顯示當前步驟
            self.animate_step(current, visited, player, goal)

            if current == goal:
                # 找到路徑後還原並返回路徑
                path = []
                while current:
                    path.append(current)
                    current = parent[current]
                return path[::-1]

            x, y = current
            for dx, dy in directions:  # 檢查每個方向
                nx, ny = x + dx, y + dy

                # 動畫：標示目前正在檢查的方向
                self.highlight_direction((x, y), (dx, dy), visited)

                if 0 <= nx < len(self.maze[0]) and 0 <= ny < len(self.maze) and self.maze[ny][nx] == 0:
                    tentative_g_score = g_scores[current] + 1  # 假設每步的代價為 1
                    if (nx, ny) not in g_scores or tentative_g_score < g_scores[(nx, ny)]:
                        g_scores[(nx, ny)] = tentative_g_score
                        f_score = tentative_g_score + heuristic((nx, ny), goal)
                        heapq.heappush(priority_queue, (f_score, (nx, ny)))
                        parent[(nx, ny)] = current

                # 動畫：清除方向標示
                self.clear_highlight((x, y), (dx, dy), visited)

        return None  # 無解

    def animate_step(self, current, visited, player, goal):
        self.win.fill(config.WHITE)

        # Draw maze
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                color = config.BLACK if self.maze[y][x] == 1 else config.WHITE
                pygame.draw.rect(self.win, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

        # Draw visited nodes
        for node in visited:
            pygame.draw.rect(
                self.win, config.LIGHT_BLUE,
                (node[0] * self.cell_size, node[1] * self.cell_size, self.cell_size, self.cell_size)
            )

        # Draw current step in yellow
        pygame.draw.rect(
            self.win, config.YELLOW,
            (current[0] * self.cell_size, current[1] * self.cell_size, self.cell_size, self.cell_size)
        )

        # Draw goal
        pygame.draw.rect(
            self.win, config.GREEN,
            (goal[0] * self.cell_size, goal[1] * self.cell_size, self.cell_size, self.cell_size)
        )

        # Update player position
        player.x, player.y = current
        player.rect.topleft = (current[0] * self.cell_size, current[1] * self.cell_size)

        all_sprites = pygame.sprite.Group(player)
        all_sprites.draw(self.win)

        pygame.display.update()
        pygame.time.delay(config.DELAYS["algorithm_step"])  # 使用 algorithm_step 延遲

    def highlight_direction(self, current, direction, visited):
        x, y = current
        dx, dy = direction
        highlight_x, highlight_y = x + dx, y + dy

        if 0 <= highlight_x < len(self.maze[0]) and 0 <= highlight_y < len(self.maze):
            color = config.LIGHT_BLUE if (highlight_x, highlight_y) in visited else config.YELLOW
            pygame.draw.rect(
                self.win, color,
                (highlight_x * self.cell_size, highlight_y * self.cell_size, self.cell_size, self.cell_size)
            )
            pygame.display.update()
            pygame.time.delay(config.DELAYS["algorithm_step"])

    def clear_highlight(self, current, direction, visited):
        x, y = current
        dx, dy = direction
        highlight_x, highlight_y = x + dx, y + dy

        if 0 <= highlight_x < len(self.maze[0]) and 0 <= highlight_y < len(self.maze):
            if self.maze[highlight_y][highlight_x] == 1:
                color = config.BLACK
            elif (highlight_x, highlight_y) in visited:
                color = config.LIGHT_BLUE
            else:
                color = config.WHITE

            pygame.draw.rect(
                self.win, color,
                (highlight_x * self.cell_size, highlight_y * self.cell_size, self.cell_size, self.cell_size)
            )
            pygame.display.update()