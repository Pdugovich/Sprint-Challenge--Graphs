from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval


""" Creating function for bfs"""

def bfs_maze(starting_vertex):
    """
    Return a list containing the shortest path from
    starting_vertex to destination_vertex in
    breath-first order.
    """
    
    # create a queue and enqueue a starting index
    qq = Queue()
    qq.enqueue([starting_vertex])
    # create a set of traversed vertices
    visited = set()
    # while queue is not empty
    while qq.size() > 0:
        # dequeue/pop the first vertex
        path = qq.dequeue()
        # if not visited
        if path[-1] not in visited and '?' in traversal_graph[path[-1]].values():
            #print(path)
            return path
        else:
            # DO THE THING!!!
            #print(path[-1])
            # mark as visited
            visited.add(path[-1])
            # enqueue all neighbors
            for next_vert in traversal_graph[path[-1]].values():
                new_path = list(path)
                new_path.append(next_vert)
                qq.enqueue(new_path)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Make the structure of the graph
traversal_graph = {}

# Noting reverse directions for going backwards for bfs
reverse_direction = {'n': 's','s': 'n', 'e': 'w', 'w':'e'}

# Be in a room
player = Player(world.starting_room)

# Add that room and it's possible directions to the traversal_graph
traversal_graph[player.current_room.id] = {direction: '?' for direction in player.current_room.get_exits()}

# While the length of the traversal_graph

while len(traversal_graph) < len(room_graph):
# is less than 500 (or whatever the length of the room is)
    # If there are '?' in current room
    if '?' in traversal_graph[player.current_room.id].values():
        # Get possible directions - get exits
        # These are the edges that connect nodes
        possible_directions = player.current_room.get_exits()

        # Saving this, so we can ammend the dictionary in the future
        start_step_node = player.current_room.id
        # Check the traversal graph to see if
        # you've visited the node in that direction
        # If that direction is '?' travel to it
        unknown_directions = []
        for dir in possible_directions:
            if traversal_graph[player.current_room.id][dir] == '?':
                unknown_directions.append(dir)
        #print(f'unknown_directions = {unknown_directions}')
        # OLD if traversal_graph[player.current_rooom.id][direction] == '?':
        # OLD direction = random.choice([dir in possible_directions if traversal_graph[player.current_room.id][dir]]=='?')
        direction = random.choice(unknown_directions)
        # move player to that node
        player.travel(direction)
        # Add direction (n, s, e, w) to traversal path
        traversal_path.append(direction)
        #print(traversal_path)
        # add the current node id to the appropriate 
        # direction in the previous node
        traversal_graph[start_step_node][direction] = player.current_room.id
        #print(f'traversal_graph[start_step_node][direction] = {traversal_graph[start_step_node][direction]}')
        # add the previous node id to the appropriate
        # direction in the current node
        # traversal_graph[player.current_room.id] = {dir: '?' for dir in player.current_room.get_exits()}
        # If the room exists in the traversal graph, add the direction
        if player.current_room.id in traversal_graph:
            traversal_graph[player.current_room.id][reverse_direction[direction]] = start_step_node
        else:
            traversal_graph[player.current_room.id] = {direction: '?' for direction in player.current_room.get_exits()}
            traversal_graph[player.current_room.id][reverse_direction[direction]] = start_step_node
        # both in traversal_graph
        # Printing length of traversal path for debugging
        print(len(traversal_graph))

        # Else, if all directions are known
        # TODO: Implement BFS!!!!
    else:
        # create a temporary path to traverse down until you get to a room with '?'
        # temp_path = traversal_path.copy()
        # # retrace your steps, using the traversal path
        # while '?' not in traversal_graph[player.current_room.id].values():
        #     # travel in that direction
        #     player.travel(reverse_direction[temp_path[-1]])
        #     # With each backwards move, add that direction
        #     traversal_path.append(reverse_direction[temp_path[-1]])
        #     print(f'temp_path = {temp_path}')
        #     print(f'Travel Path while reversing = {traversal_path}')
        #     temp_path.pop()
        
        # BFS inplementation
        # qq = []
        # qq.append([player.current_room.id])
        # bfs_visited = set()
        # bfs_path = []
        # while len(qq) > 0:
        #     bfs_path = qq.pop(0)
        #     print(bfs_path)
        #     # if '?' in traversal_graph[bfs_path[-1]].values():
        #     #     path_to_follow = bfs_path
        #     #     print(f'path_to_follow = {path_to_follow}')
        #     if bfs_path[-1] not in bfs_visited:
        #         bfs_visited.add(bfs_path[-1])
        #         for neighbor in traversal_graph[bfs_path[-1]].values():
        #             new_path = list(bfs_path)
        #             new_path.append(neighbor)
        #             qq.append(new_path)
        # print(qq)
        path_to_follow = []
        chain_to_unknown = bfs_maze(player.current_room.id)
        for node in chain_to_unknown[:-1]:
            next_index = chain_to_unknown.index(node) + 1
            direction_to_previous = [k for k,v in traversal_graph[node].items() if v == chain_to_unknown[next_index]]
            # print(direction_to_previous)
            path_to_follow.append(direction_to_previous[-1])
        print(path_to_follow)
        for step in path_to_follow:
            traversal_path.append(step)
            player.travel(step)



# Print traversal graph so we have it
print(traversal_path)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")


"""
TEST PASSED !!!

TESTS PASSED: 991 moves, 500 rooms visited

traversal_path = ['n', 's', 'w', 'w', 's', 'w', 's', 's', 'n', 'n', 'e', 'n', 'e', 'n', 'w', 'w', 'w', 's', 's', 's', 'w', 'w', 'w', 's', 'w', 'n', 's', 'e', 'n', 'e', 'e', 'n', 'w', 'w', 'w', 'e', 'e', 'e', 's', 'e', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'w', 'e', 'n', 'e', 's', 'n', 'e', 's', 's', 's', 'w', 'e', 'n', 'e', 'w', 'n', 'n', 'w', 'w', 'n', 'n', 'n', 'w', 's', 'w', 's', 'w', 'e', 's', 'w', 'e', 'n', 'n', 'e', 's', 's', 'n', 'n', 'n', 'e', 'n', 'n', 'w', 'w', 'w', 'n', 's', 'w', 'n', 'w', 'w', 'n', 'w', 'e', 's', 'e', 'n', 'n', 'w', 'n', 'e', 'n', 'e', 'e', 'e', 'n', 'e', 's', 'n', 'n', 'e', 'n', 's', 'e', 'e', 'e', 'e', 'n', 'n', 'w', 'w', 'w', 'n', 'n', 'w', 'n', 's', 'e', 's', 's', 'w', 'w', 'n', 'w', 'n', 'n', 'n', 'n', 'n', 'n', 's', 's', 'w', 'e', 's', 's', 's', 'w', 'n', 'n', 's', 's', 'w', 'n', 'w', 'e', 'n', 'n', 's', 's', 's', 'w', 'w', 's', 'w', 'e', 'n', 'w', 'e', 'e', 'e', 'e', 'e', 's', 'w', 'w', 'e', 'e', 'e', 'n', 'n', 'n', 'n', 's', 's', 's', 's', 's', 'e', 'n', 's', 'e', 'e', 'e', 'n', 'w', 'n', 's', 'e', 'n', 'n', 'w', 'n', 's', 'w', 'n', 'w', 'e', 's', 'e', 'e', 's', 's', 's', 'e', 'e', 'n', 'n', 'w', 'n', 'n', 'w', 'n', 'w', 'e', 'e', 'w', 's', 'e', 's', 's', 'e', 'n', 'n', 'e', 'e', 'e', 'e', 'w', 'n', 'e', 'e', 'w', 'n', 'e', 'e', 'n', 's', 'e', 'w', 'w', 'n', 's', 'w', 's', 'w', 'n', 'w', 'n', 'n', 'n', 'n', 'e', 'e', 'w', 'w', 's', 'w', 'w', 's', 's', 's', 's', 'e', 'w', 's', 's', 'e', 'e', 'w', 'w', 'n', 'n', 'n', 'w', 'w', 'w', 'n', 'n', 'n', 'n', 's', 's', 's', 'w', 'n', 'n', 'w', 'e', 's', 's', 'e', 's', 'w', 's', 'w', 'e', 'n', 'w', 'w', 'n', 's', 'e', 'n', 's', 'e', 'e', 'e', 'e', 'n', 'w', 'n', 's', 'e', 'n', 's', 's', 'e', 'e', 'n', 'n', 's', 's', 'w', 'n', 'n', 'n', 'e', 'n', 'w', 'w', 'e', 'e', 's', 'e', 's', 's', 's', 'e', 'n', 'e', 'n', 'n', 's', 'e', 'n', 'e', 's', 'n', 'e', 'w', 'w', 'n', 's', 's', 'w', 's', 'w', 'n', 'n', 's', 's', 's', 's', 's', 'w', 'n', 's', 'w', 'w', 's', 's', 's', 's', 's', 'n', 'w', 'n', 's', 's', 'w', 'e', 's', 'e', 's', 's', 'w', 's', 'w', 'e', 'n', 'e', 'e', 'w', 's', 's', 's', 's', 's', 's', 'e', 's', 's', 'w', 's', 's', 'n', 'n', 'e', 's', 'e', 'e', 'e', 'n', 'e', 'e', 's', 's', 'e', 'w', 's', 's', 'n', 'n', 'n', 'n', 'e', 'w', 'w', 's', 's', 'n', 'n', 'w', 's', 'w', 'w', 's', 'e', 's', 's', 'n', 'n', 'e', 's', 's', 'n', 'n', 'w', 'w', 's', 's', 'n', 'n', 'n', 'w', 's', 's', 'w', 's', 'n', 'e', 's', 's', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'w', 's', 'n', 'n', 'n', 'n', 'e', 's', 's', 'n', 'n', 'e', 's', 'e', 'n', 'e', 's', 's', 'n', 'n', 'w', 's', 'w', 's', 's', 's', 's', 'e', 'w', 'n', 'n', 'n', 'e', 's', 's', 'e', 'e', 'e', 'e', 'w', 'w', 'w', 'w', 'n', 'e', 'w', 'n', 'w', 'n', 'n', 'w', 'w', 'n', 'w', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'n', 'n', 'n', 'n', 'n', 'w', 'w', 'w', 'n', 's', 'e', 's', 'e', 's', 's', 's', 'n', 'n', 'n', 'w', 's', 'n', 'w', 's', 'n', 'e', 'n', 'e', 'n', 'w', 'e', 'n', 'w', 'e', 'n', 'w', 'w', 's', 'n', 'e', 'e', 'n', 'w', 'e', 'n', 'e', 'w', 'w', 'e', 'e', 'e', 'n', 'e', 's', 'n', 'w', 'n', 'n', 'e', 'e', 'e', 'e', 's', 'n', 'e', 'e', 'e', 'w', 'w', 's', 'e', 'e', 'e', 'n', 's', 'e', 'w', 'w', 'w', 'w', 'n', 'w', 'w', 'n', 'e', 'e', 'e', 'e', 'e', 'e', 's', 'n', 'w', 'w', 'w', 'w', 'w', 'n', 'e', 'n', 'e', 's', 'n', 'e', 'e', 'e', 'w', 'n', 'e', 'w', 's', 'w', 's', 'e', 'e', 'e', 's', 'n', 'w', 'w', 'w', 'n', 'w', 'w', 'n', 'e', 'e', 'n', 'e', 'w', 's', 'w', 'n', 'n', 'e', 'e', 'e', 's', 'n', 'w', 'w', 'w', 's', 's', 'w', 's', 's', 'w', 's', 'w', 's', 'w', 's', 'e', 's', 's', 'e', 'w', 'n', 'e', 'e', 's', 's', 's', 's', 'e', 'e', 'w', 'w', 's', 'e', 'e', 'w', 'w', 'n', 'n', 'e', 'e', 'w', 'n', 's', 'w', 'n', 'n', 'e', 'e', 's', 'n', 'e', 'w', 'w', 'w', 'n', 'e', 'e', 'e', 'w', 'w', 'w', 'w', 'w', 'n', 'w', 's', 's', 'n', 'n', 'n', 'w', 'n', 'n', 'n', 'n', 'n', 's', 's', 'e', 'n', 'n', 's', 's', 'w', 's', 's', 'e', 'n', 'e', 'n', 'n', 'n', 'n', 's', 's', 's', 'e', 'n', 'n', 'e', 'n', 'n', 'e', 'n', 's', 'e', 'n', 's', 'e', 'e', 'w', 'n', 's', 'w', 'w', 'w', 's', 's', 'w', 'n', 's', 's', 's', 'w', 's', 'w', 's', 'w', 's', 'w', 'n', 'w', 'w', 'w', 'n', 's', 'w', 'n', 's', 'w', 'w', 'n', 'w', 'n', 'w', 'e', 's', 'w', 'e', 'e', 's', 'w', 'w', 'w', 'w', 'e', 'n', 'w', 'w', 's', 'n', 'w', 'e', 'e', 'n', 'n', 's', 'w', 'w', 'w', 'e', 'e', 'e', 's', 'e', 'n', 's', 's', 'e', 'e', 'e', 's', 'w', 'w', 'w', 'e', 'e', 's', 'w', 'w', 'w', 'w', 'w', 'e', 'n', 's', 'e', 'n', 's', 's', 'w', 'w', 'e', 's', 'e', 's', 's', 'e', 's', 'w', 'w', 's', 'w', 's', 'n', 'e', 'n', 'e', 'e', 'e', 'e', 'e', 's', 'w', 's', 'w', 's', 'n', 'e', 'n', 'w', 'w', 'w', 'e', 's', 'w', 'w', 'e', 'e', 's', 's', 's', 's', 's', 'e', 'w', 'n', 'e', 'w', 'n', 'n', 'n', 'w', 'w', 'w', 'w', 'e', 'e', 'e', 's', 's', 'w', 'e', 's', 's', 'n', 'w', 'w', 'e', 'e', 'n', 'n', 'w', 'e', 'n', 'e', 'n', 'n', 'e', 'e', 'e', 'n', 'e', 'n', 'n', 'w', 's', 'w', 'e', 'n', 'w', 'e', 'e', 'n', 'n', 'n', 'n', 'e', 's']

"""