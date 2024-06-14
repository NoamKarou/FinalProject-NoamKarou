import customtkinter as ctk
import math
import random


class ConnectionsViewer:
    def __init__(self, parent, fetch_callback):
        self.parent = parent
        self.fetch_callback = fetch_callback

        # Create a canvas widget
        self.canvas = ctk.CTkCanvas(parent, width=800, height=800, bg='gray10')
        self.canvas.pack()

        # Create a label to display IP and port information
        self.text = ctk.StringVar()
        self.info_label = ctk.CTkLabel(parent, textvariable=self.text)
        self.info_label.pack()

        self.nodes = []
        self.connections = []

        self.fetch_node_details()

    def on_enter(self, event, ip, port):
        self.text.set(f"IP: {ip}, Port: {port}")

    def on_leave(self, event):
        self.text.set("")

    def calculate_positions(self, nodes, center_x, center_y, radius):
        angle_step = 2 * math.pi / (len(nodes) - 1)
        positions = []
        for i in range(len(nodes)):
            if nodes[i]["name"] == "you":
                positions.append((center_x, center_y))
            else:
                angle = angle_step * (i - 1)
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                positions.append((x, y))
        return positions

    def fetch_node_details(self):
        self.nodes, self.connections = self.fetch_callback()
        self.update_graph()
        self.parent.after(1000, self.fetch_node_details)  # Schedule the function to be called after 1 second

    def update_graph(self):
        self.canvas.delete("all")

        # Center and radius for the circular layout
        center_x, center_y = 400, 400
        radius = 200

        # Calculate positions for nodes
        positions = self.calculate_positions(self.nodes, center_x, center_y, radius)

        # Draw connections
        for conn in self.connections:
            node1 = next(node for node in self.nodes if node["name"] == conn[0])
            node2 = next(node for node in self.nodes if node["name"] == conn[1])
            pos1 = positions[self.nodes.index(node1)]
            pos2 = positions[self.nodes.index(node2)]
            self.canvas.create_line(pos1[0], pos1[1], pos2[0], pos2[1], fill="black")

        # Draw nodes
        for i, node in enumerate(self.nodes):
            x, y = positions[i]
            r = 45
            fill_color = "yellow" if node["name"] == "you" else "gray"
            oval_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill_color)
            #self.canvas.create_text(x, y, text=node["name"], fill="green")

            # Bind hover events
            self.canvas.tag_bind(oval_id, "<Enter>",
                                 lambda event, ip=node["ip"], port=node["port"]: self.on_enter(event, ip, port))
            self.canvas.tag_bind(oval_id, "<Leave>", self.on_leave)


# Callback function to fetch node details
def fetch_callback():
    # Simulating fetching node details (In real scenario, this can be an API call or database query)
    new_nodes = [
        {"name": "you", "ip": "192.168.1.1", "port": "8080"}
    ]

    for i in range(1, random.randint(4, 6)):
        new_nodes.append({
            "name": f"node{i}",
            "ip": f"192.168.1.{random.randint(1, 254)}",
            "port": f"{random.randint(8000, 9000)}"
        })

    new_connections = [("you", node["name"]) for node in new_nodes if node["name"] != "you"]

    return new_nodes, new_connections


# Create the main window
root = ctk.CTk()
root.title("Graph Visualization")

# Create an instance of ConnectionsViewer
viewer = ConnectionsViewer(root, fetch_callback)

# Start the customtkinter event loop
root.mainloop()
