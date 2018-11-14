import sys
import math

class Cavern():

    def __init__(self, parent=None, x=None, y=None):
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
        self.x = x
        self.y = y
        self.connections = []

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


#start is start index and end is end index of caverns array
def astar(caverns, start, end):

    # Create start and end node
    start_cavern = caverns[start]
    start_cavern.g = 0
    start_cavern.h = 0
    start_cavern.f = 0
    end_cavern = caverns[end]
    end_cavern.g = 0
    end_cavern.h = 0
    end_cavern.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_cavern)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_cavern = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_cavern.f:
                current_cavern = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_cavern)

        print("current cavern: " + str(caverns.index(current_cavern)) + " current connections: " + str(current_cavern.connections))

        # Found the goal
        if current_cavern == end_cavern:
            path = []
            current = current_cavern
            while current is not None:
                path.append("(" + str(current.x) + "," + str(current.y) + ")")
                current = current.parent
                if len(path) > 50:
                    break
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_cavern_index in current_cavern.connections: #cavern connections
            new_cavern = caverns[new_cavern_index]
            cavern_x = new_cavern.x
            cavern_y = new_cavern.y

            caverns[new_cavern_index].parent = current_cavern
            children.append(caverns[new_cavern_index])


        for child in children:
            if child in closed_list:
                continue
            
            cavern_id = caverns.index(current_cavern)
            child_id = caverns.index(child)
            
            child_distance = math.hypot(current_cavern.x - child.x, current_cavern.y - child.y)        
            child_distance_end = math.hypot(child.x - end_cavern.x, child.y - end_cavern.y)

            child.g = current_cavern.g + child_distance
            child.h = child_distance_end
            child.f = child.g + child.h

            print(f"current cavern: {str(cavern_id)}  - examining child: {str(child_id)} : d = {child_distance}, de = {child_distance_end}, g = {child.g}, h = {child.h}, f = {child.f}" )

            # Child is already in the open list
            skip_child = False
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    skip_child = True
                    break 

            if skip_child == True:
                    continue

            # Add the child to the open list
            open_list.append(child)


        print("open_list = " + str(open_list))

def get_cave_string():
    filename = sys.argv[1] + ".cav"
    f = open(filename, 'r')
    cave_string = f.read()
    f.close()
    return cave_string

def main():
    # 7,2,8,3,2,14,5,7,6,11,2,11,6,14,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,1,1,0,0,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0
    cave_string = get_cave_string()
    cave_string_split = cave_string.split(',') 
    cavern_count = int(cave_string_split[0])
    cavern_coords = cave_string_split[1:2 * cavern_count+1]
    cavern_connections = cave_string_split[len(cavern_coords) + 1:len(cave_string_split)]

    caverns = []
    for i in range(0, len(cavern_coords), 2):
        cavern = Cavern(None, int(cavern_coords[i]), int(cavern_coords[i + 1]))
        caverns.append(cavern)


    for cavern_index, i in enumerate(range(0, len(cavern_connections), cavern_count)):
        connections = cavern_connections[i:i + cavern_count]
        print("cavern " + str(cavern_index) + ": " + str(connections))
        for connection_index, connection in enumerate(connections):
            print(connection_index, connection)
            if connection == '1':
                caverns[connection_index].connections.append(cavern_index) 
                 

    for i, cavern in enumerate(caverns):
        print("cavern " + str(i) + " at coords " + str(cavern.x) + "," + str(cavern.y) + ". connections: " + str(cavern.connections))

  
    path = astar(caverns, 0, cavern_count-1)
    print(path)

if __name__ == '__main__':
    main()
