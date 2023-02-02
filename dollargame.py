import random
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backend_bases import MouseButton


class Node:
    def __init__(self):
        self.value = 0
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
        neighbor.neighbors.append(self)

    def give(self):
        self.value -= len(self.neighbors)
        for neighbor in self.neighbors:
            neighbor.value += 1

    def take(self):
        self.value += len(self.neighbors)
        for neighbor in self.neighbors:
            neighbor.value -= 1


node_dict = {}


def add_edges(graph, extra):
    S = list(graph.nodes)
    current_node = random.sample(S, 1).pop()
    S.remove(current_node)
    while S:
        next_node = random.sample(S, 1).pop()
        S.remove(next_node)
        Node.add_neighbor(current_node, next_node)
        graph.add_edge(current_node, next_node)
        current_node = next_node
        if current_node in S:
            S.remove(current_node)
    T = list(graph.nodes)
    for i in range(extra):
        node_1 = random.sample(T, 1).pop()
        possible = [_ for _ in T if _ not in node_1.neighbors and _ is not node_1]
        node_2 = random.sample(possible, 1).pop()
        Node.add_neighbor(node_1, node_2)
        graph.add_edge(node_1, node_2)


def set_weights(graph, difficulty):
    genus = len(list(graph.edges)) - len(list(graph.nodes)) + 1
    total_value = genus + difficulty
    tally = 0
    node_count = 0
    for node in graph.nodes:
        if node_count < len(list(graph.nodes)) - 1:
            new_val = -1 * (-1 * total_value // len(list(graph.nodes))) + random.randrange(-3, 3)
            node.value = new_val
            node_dict[node] = str(node.value)
            tally += new_val
            node_count += 1
        else:
            node.value = total_value - tally
            node_dict[node] = str(node.value)


def create_board(size, extra_edges, difficulty):
    board = nx.Graph()
    for i in range(size):
        board.add_node(Node())
    add_edges(board, extra_edges)
    set_weights(board, difficulty)
    return board


def check_win(board):
    for node in list(board.nodes):
        if node.value < 0:
            return False
    return True


def win_dialogue():
    plt.close()
    node_dict.clear()
    window = Toplevel()
    message = Label(window, text='You Win!', padx=10, pady=10)
    message.pack()
    again_button = Button(window, text='Play Again?', bg='lime', command=root.deiconify)
    again_button.pack()


def begin_game(size, difficulty):
    def on_click(event):
        (x, y) = (event.xdata, event.ydata)
        for node in new_board.nodes:
            coords = pos[node]
            distance = pow(x - coords[0], 2) + pow(y - coords[1], 2)
            if distance < 0.01:
                if event.button == MouseButton.LEFT:
                    Node.give(node)
                elif event.button == MouseButton.RIGHT:
                    Node.take(node)
                for node in new_board.nodes:
                    node_dict[node] = str(node.value)
                plt.clf()
                nx.draw(new_board, pos, labels=node_dict, font_weight='bold', node_size=500, font_size=16)
                plt.show()
        if check_win(new_board):
            win_dialogue()
    root.withdraw()
    fig, ax = plt.subplots()
    new_board = create_board(size, random.randint(1, size//2), difficulty)
    pos = nx.kamada_kawai_layout(new_board)
    nx.draw(new_board, pos, labels=node_dict, font_weight='bold', node_size=500, font_size=16)
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()



root = Tk()
root.title('Dollar Game')

options_frame = LabelFrame(root, text='Options', padx=5, pady=5)
options_frame.pack(padx=10, pady=10)
node_label = Label(options_frame, text='Nuber of Nodes')
diff_label = Label(options_frame, text='Difficulty')
node_slider = Scale(options_frame, from_=20, to=5)
diff_slider = Scale(options_frame, from_=5, to=0)

node_label.grid(row=0, column=0)
diff_label.grid(row=0, column=1)
node_slider.grid(row=1, column=0)
diff_slider.grid(row=1, column=1)

begin_button = Button(root, text='Begin Game', bg='lime', command=lambda: begin_game(node_slider.get(), 5 - diff_slider.get()))
begin_button.pack()

instructions_frame = LabelFrame(root, text='Instructions', padx=5, pady=5)
instructions_frame.pack(padx=10, pady=10)
instructions = Label(instructions_frame, text='Use the nodes slider to select the number of nodes that will appear in '
                                                  'your graph. \nUse the difficulty slider to choose the challenge of the '
                                                  'game. Higher numbers are harder. \nThe objective of the game is to '
                                                  'eliminate all negative values from the graph. \nLeft click on a node to '
                                                  'give 1 to all connected nodes. \nRight click a node to take 1 from all '
                                                  'connected nodes. \nWhen your desired options are set, press Begin Game.')
instructions.pack()


mainloop()
