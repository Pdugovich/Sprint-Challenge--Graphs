"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {} # This is our adjacency list

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        # Check if they exist
        if v1 in self.vertices and v2 in self.vertices:
            # add the edge to both
            self.vertices[v1].add(v2)
        else:
            print("ERROR ADDING EDGE: VERTEX NOT FOUND")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        else:
            return None
            # Might want to raise an exception here, but we don't


    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
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
            if path[-1] not in visited:
                # DO THE THING!!!
                print(path[-1])
                # mark as visited
                visited.add(path[-1])
                # enqueue all neighbors
                # This is necessary because if you change the path
                # If will effect all of the paths. Not a good idea
                for next_vert in self.get_neighbors(path[-1]):
                    new_path = list(path)
                    new_path.append(next_vert)
                    qq.enqueue(new_path)


    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # create a queue and enqueue a starting index
        ss = Stack()
        ss.push([starting_vertex])
        # create a set of traversed vertices
        visited = set()
        # while queue is not empty
        while ss.size() > 0:
            # dequeue/pop the first vertex
            path = ss.pop()
            # if not visited
            if path[-1] not in visited:
                # DO THE THING!!!
                print(path[-1])
                # mark as visited
                visited.add(path[-1])
                # enqueue all neighbors
                for next_vert in self.get_neighbors(path[-1]):
                    new_path = list(path)
                    new_path.append(next_vert)
                    ss.push(new_path)

    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        # Initial case
        if visited is None:
            visited = set()
        # Check if the "starting_vertex" is in the visited list
        # Note what "Starts" will change with the recursion
        if starting_vertex not in visited:
            # add that node to the list of visited nodes
            visited.add(starting_vertex)
            # print the node
            print(starting_vertex)
            # Put each of the adjescent nodes through the 
            # function. It will ignore the ones that have been visted
            for adj in self.get_neighbors(starting_vertex):
                # Voila!
                self.dft_recursive(adj, visited)


    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Copied the traversal, except I included a
        # if statement. If the last item in the path
        # is the destination, then return the path!
        # otherwise, continue on
        
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
            if path[-1] == destination_vertex:
                return path
            else:
                # DO THE THING!!!
                #print(path[-1])
                # mark as visited
                visited.add(path[-1])
                # enqueue all neighbors
                for next_vert in self.get_neighbors(path[-1]):
                    new_path = list(path)
                    new_path.append(next_vert)
                    qq.enqueue(new_path)



    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        # Copied the traversal, except I included a
        # if statement. If the last item in the path
        # is the destination, then return the path!
        # otherwise, continue on

        # create a queue and enqueue a starting index
        ss = Stack()
        ss.push([starting_vertex])
        # create a set of traversed vertices
        visited = set()
        # while queue is not empty
        while ss.size() > 0:
            # dequeue/pop the first vertex
            path = ss.pop()
            # if not visited
            if path[-1] == destination_vertex:
                return path
            else:
                # DO THE THING!!!
                print(path[-1])
                # mark as visited
                visited.add(path[-1])
                # enqueue all neighbors
                for next_vert in self.get_neighbors(path[-1]):
                    new_path = list(path)
                    new_path.append(next_vert)
                    ss.push(new_path)


    def dfs_recursive(self, starting_vertex, destination_vertex, visited = None, path = None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if visited == None:
            visited = set()
        if path == None:
            path = []
        # Check if the "starting_vertex" is in the visited list
        # Note what "Starts" will change with the recursion
        if starting_vertex not in visited:
            # add that node to the list of visited nodes
            visited.add(starting_vertex)
            # Making a copy of the path
            path_copy = path.copy()
            # Appending the node to the vertex
            path_copy.append(starting_vertex)
            # If we're at the destination, GREAT! We can return the path
            if starting_vertex == destination_vertex:
                return path_copy
            
            for adj in self.get_neighbors(starting_vertex):
                # If we're not at the destination, make a variable that will contain the path
                final_path = self.dfs_recursive(adj, destination_vertex, visited, path_copy)
                # This will either return None, or the path leading to the destination.
                if final_path is not None:
                    # If it's not None, send the Final Path back up
                    return final_path
