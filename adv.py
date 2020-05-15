from room import Room
from player import Player
from world import World
from collections import deque
import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = ['n', 's', 'e', 'w']

inverse_exits = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

vertices = {}
list_exits = {}

# exits = player.current_room.get_exits()
# print(exits)
for path in traversal_path:
    list_exits[path] = "?"

vertices[0] = list_exits


def get_next_unexplored(starting_room):
    """
    Uses a bfs on the starting room to get the next unexplored room
    """
    q = deque()
    q.append([starting_room])
    visited = set()

    while len(q) > 0:
        path = q.popleft()
        v = path[-1]
        if v not in visited:
            for i in vertices[v]:
                if vertices[v][i] == '?':
                    return path
            visited.add(v)
            for next_vertex in vertices[v]:
                path_copy = path.copy()
                path_copy.append(vertices[v][next_vertex])
                q.append(path_copy)
    return False


while len(room_graph):
    # hold the current room in a from_room
    from_room = player.current_room.id
    # get a list of the available exits from that room from the  graph
    exits = vertices[from_room]
    # get all unexplored directions for the room
    unexplored = []
    for dirs in exits:
        if exits[dirs] == '?':
            unexplored.append(dirs)

    random_dir = ''
    if len(unexplored):
        random_dir = unexplored[random.randint(0, len(unexplored) - 1)]
    else:
        # get the nearest room with an unexplored exit
        path_to_next_unexp = get_next_unexplored(from_room)
        if path_to_next_unexp:
            for room in path_to_next_unexp:
                cur = player.current_room.id
                pos_exit = player.current_room.get_exits()
                for exit in pos_exit:
                    # find the direction required to go to the next room returned in the bfs list
                    if room == vertices[cur][exit]:
                        traversal_path.append(exit)
                        player.travel(exit)
            continue
        # if there is no unexplored room anymore
        else:
            break

    player.travel(random_dir)
    traversal_path.append(random_dir)
    # set the new room to a variable
    to_room = player.current_room.id
    # fill in the from_room vertices with new known room
    vertices[from_room][random_dir] = to_room
    # create a new vertex if one does not yet exist for the room
    if to_room not in vertices:
        vertices[to_room] = set()
        # add edges with available exits
        list_exits = {}
        exits = player.current_room.get_exits()
        for exit in exits:
            list_exits[exit] = '?'
        vertices[to_room] = list_exits
    # add edge for the room travelled from
    vertices[to_room][inverse_exits[random_dir]] = from_room

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
    )
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
