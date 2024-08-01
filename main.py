import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Robot:
    def __init__(self, grid_size):
        self.position = (grid_size // 2, grid_size // 2)  # Start in the middle of the grid
        self.grid_size = grid_size
        self.map = np.zeros((grid_size, grid_size))  # 0 for unexplored, 1 for free space, -1 for obstacles
        self.visited = set()
        self.sensors = self.initialize_sensors()
        self.stack = [self.position]  # Stack for DFS

    def initialize_sensors(self):
        # Initialize sensors, if needed
        return

    def move(self, direction):
        x, y = self.position
        if direction == 'up' and y > 0:
            self.position = (x, y - 1)
        elif direction == 'down' and y < self.grid_size - 1:
            self.position = (x, y + 1)
        elif direction == 'left' and x > 0:
            self.position = (x - 1, y)
        elif direction == 'right' and x < self.grid_size - 1:
            self.position = (x + 1, y)
        # Simulate movement delay, sensor update, etc.
        self.update_map()

    def read_sensors(self):
        # Simulate sensor reading
        sensor_data = {}
        x, y = self.position
        sensor_data['up'] = self.is_obstacle(x, y - 1)
        sensor_data['down'] = self.is_obstacle(x, y + 1)
        sensor_data['left'] = self.is_obstacle(x - 1, y)
        sensor_data['right'] = self.is_obstacle(x + 1, y)
        return sensor_data

    def is_obstacle(self, x, y):
        if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size:
            return True  # Out of bounds is considered an obstacle
        # Simulate sensor reading: 10% chance of obstacle
        return np.random.random() < 0.1

    def update_map(self):
        x, y = self.position
        self.map[x, y] = 1  # Mark current position as free space
        sensor_data = self.read_sensors()
        for direction, is_obstacle in sensor_data.items():
            if direction == 'up' and y > 0 and is_obstacle:
                self.map[x, y - 1] = -1
            elif direction == 'down' and y < self.grid_size - 1 and is_obstacle:
                self.map[x, y + 1] = -1
            elif direction == 'left' and x > 0 and is_obstacle:
                self.map[x - 1, y] = -1
            elif direction == 'right' and x < self.grid_size - 1 and is_obstacle:
                self.map[x + 1, y] = -1

    def is_visited(self, position):
        return position in self.visited

    def explore(self):
        while self.stack:
            current_position = self.stack[-1]
            self.visited.add(current_position)

            unvisited_neighbors = self.get_unvisited_neighbors(current_position)
            if unvisited_neighbors:
                next_position = unvisited_neighbors[0]
                self.move_to(next_position)
                self.stack.append(next_position)
            else:
                self.stack.pop()  # Backtrack

                # Perform random walk if stuck
                if not self.stack:
                    self.perform_random_walk()

            yield self.map, self.position

    def get_unvisited_neighbors(self, position):
        neighbors = self.get_neighbors(position)
        return [neighbor for neighbor in neighbors if
                not self.is_visited(neighbor) and self.map[neighbor[0], neighbor[1]] != -1]

    def get_neighbors(self, position):
        x, y = position
        neighbors = []
        if y > 0:
            neighbors.append((x, y - 1))  # Up
        if y < self.grid_size - 1:
            neighbors.append((x, y + 1))  # Down
        if x > 0:
            neighbors.append((x - 1, y))  # Left
        if x < self.grid_size - 1:
            neighbors.append((x + 1, y))  # Right
        return neighbors

    def move_to(self, position):
        x, y = self.position
        target_x, target_y = position
        if target_y < y:
            self.move('up')
        elif target_y > y:
            self.move('down')
        elif target_x < x:
            self.move('left')
        elif target_x > x:
            self.move('right')

    def perform_random_walk(self):
        directions = ['up', 'down', 'left', 'right']
        while True:
            direction = np.random.choice(directions)
            self.move(direction)
            if not self.is_visited(self.position):
                self.stack.append(self.position)
                break

    def display_map(self):
        print(self.map)


# Global variables for visualization
fig, ax, img, robot_marker = None, None, None, None


# Visualization code
def update_visualization(data):
    global img, robot_marker
    map_data, position = data
    img.set_array(map_data)
    robot_marker.set_data([position[1]], [position[0]])  # Provide x and y as sequences
    return img, robot_marker


def main():
    global fig, ax, img, robot_marker
    grid_size = 10
    robot = Robot(grid_size)

    # Set up plot
    fig, ax = plt.subplots()
    img = ax.imshow(robot.map, cmap='gray', vmin=-1, vmax=1, animated=True)
    robot_marker, = ax.plot([], [], 'ro')  # Robot's current position

    ani = animation.FuncAnimation(fig, update_visualization, frames=robot.explore, repeat=False, blit=True,
                                  save_count=50)

    plt.show()


if __name__ == "__main__":
    main()
