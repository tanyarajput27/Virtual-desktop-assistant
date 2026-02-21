import networkx as nx
import matplotlib.pyplot as plt
import pyttsx3
import re

# VOICE ENGINE

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()


# FIXED COORDINATES (aligned layout)

pos = {
    # LEFT VERTICAL LINE
    "Kaveri Hostel": (-6, 4),
    "Main Gate": (-6, 1),
    "Krishna Hostel": (-6, -2),

    # AUDITORIUM + PASSAGES + PARKING CLUSTER
    "Auditorium": (-3.5, 1),
    "Left Passage": (-2, 2),
    "Right Passage": (-2, 0),
    "Parking and Basketball Court": (-3.5, -2),

    # CENTRAL GROUND (big circle)
    "Central Ground": (0, 1),

    # ECE/CSE + IT (bottom)
    "ECE and CSE Department": (0, -2),
    "IT Department": (2, -2),

    # RIGHT-SIDE VERTICAL CHAIN
    "Canteen": (4, -2),
    "Examination Centre": (4, 0),
    "Academic Branch": (4, 2),
    "Architecture Department": (4, 4),

    # MECHANICAL (connecting left side + top)
    "Mechanical and Automation Department": (0, 4)
}


# CAMPUS MAP CONNECTIONS

campus_map = {
    "Main Gate": ["Kaveri Hostel", "Krishna Hostel", "Auditorium"],
    "Kaveri Hostel": ["Main Gate", "Mechanical and Automation Department"],
    "Krishna Hostel": ["Main Gate", "Parking and Basketball Court"],
    "Auditorium": ["Main Gate", "Left Passage", "Right Passage"],
    "Left Passage": ["Auditorium", "Central Ground"],
    "Right Passage": ["Auditorium", "Central Ground"],
    "Central Ground": ["Right Passage", "Left Passage", "Mechanical and Automation Department", "ECE and CSE Department"],
    "Mechanical and Automation Department": ["Kaveri Hostel", "Central Ground", "Architecture Department"],
    "Architecture Department": ["Mechanical and Automation Department", "Academic Branch"],
    "Academic Branch": ["Architecture Department", "Examination Centre"],
    "Examination Centre": ["Academic Branch", "Canteen"],
    "Canteen": ["Examination Centre", "IT Department"],
    "IT Department": ["Canteen", "ECE and CSE Department"],
    "ECE and CSE Department": ["IT Department", "Parking and Basketball Court", "Central Ground"],
    "Parking and Basketball Court": ["ECE and CSE Department", "Krishna Hostel"],
}

#  Ensure all connections are bidirectional
for node in list(campus_map.keys()):
    for neighbor in campus_map[node]:
        if neighbor not in campus_map:
            campus_map[neighbor] = []
        if node not in campus_map[neighbor]:
            campus_map[neighbor].append(node)


# ROUTE FINDING (BFS)

def find_route(start, destination):
    queue = [(start, [start])]
    visited = set()
    while queue:
        node, path = queue.pop(0)
        if node == destination:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in campus_map.get(node, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return None


# DESCRIBE PATH (natural directions)

def describe_route(path):
    if not path:
        return "Sorry, I couldn’t find that route."
    directions = []
    for i in range(len(path) - 1):
        current, nxt = path[i], path[i + 1]
        x1, y1 = pos[current]
        x2, y2 = pos[nxt]
        dx, dy = x2 - x1, y2 - y1

        if abs(dx) > abs(dy):
            move = "turn right" if dx > 0 else "turn left"
        elif dy > 0:
            move = "go straight ahead"
        else:
            move = "move slightly down"

        if i == 0:
            directions.append(f"From {current}, {move} to reach {nxt}.")
        elif i == len(path) - 2:
            directions.append(f"Finally, you’ll arrive at {nxt}.")
        else:
            directions.append(f"Then, {move} towards {nxt}.")
    return " ".join(directions)

# DRAW ROUTE ON MAP

def draw_route(path):
    G = nx.Graph()
    for node, neighbors in campus_map.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=2500, font_size=8, font_weight='bold', edge_color='gray')

    if path:
        edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, width=3, edge_color='red')
        nx.draw_networkx_nodes(G, pos, nodelist=[path[0]], node_color='green', node_size=2800)
        nx.draw_networkx_nodes(G, pos, nodelist=[path[-1]], node_color='red', node_size=2800)

    plt.title("🗺 IGDTUW Campus Map (Dynamic Route)", fontsize=12)
    plt.show()


# QUERY HANDLER (NEW: can detect start and destination)

def process_campus_query(query):
    query = query.lower()

    keyword_map = {
        "main gate": "Main Gate",
        "kaveri": "Kaveri Hostel",
        "kaveri hostel": "Kaveri Hostel",
        "krishna": "Krishna Hostel",
        "krishna hostel": "Krishna Hostel",
        "auditorium": "Auditorium",
        "left passage": "Left Passage",
        "right passage": "Right Passage",
        "central ground": "Central Ground",
        "central": "Central Ground",
        "mechanical": "Mechanical and Automation Department",
        "architecture": "Architecture Department",
        "academic": "Academic Branch",
        "exam": "Examination Centre",
        "examination": "Examination Centre",
        "canteen": "Canteen",
        "it": "IT Department",
        "it department": "IT Department",
        "ece": "ECE and CSE Department",
        "cse": "ECE and CSE Department",
        "ece and cse": "ECE and CSE Department",
        "parking": "Parking and Basketball Court",
        "basketball": "Parking and Basketball Court"
    }

    # detect "from X to Y"
    pattern = r"from (.?) to (.)"
    match = re.search(pattern, query)

    if match:
        start_text = match.group(1).strip()
        dest_text = match.group(2).strip()

        start = None
        destination = None

        # match start
        for k, v in keyword_map.items():
            if k in start_text:
                start = v
                break

        # match destination
        for k, v in keyword_map.items():
            if k in dest_text:
                destination = v
                break

        if not start or not destination:
            speak("Sorry, I couldn't identify one of the locations clearly.")
            print("❌ Unknown start or end location.")
            return

    else:
        # old behaviour (single location → assume main gate)
        found = []
        for k, v in keyword_map.items():
            if k in query:
                found.append(v)

        if len(found) == 0:
            speak("I could not understand the location.")
            return
        elif len(found) == 1:
            start = "Main Gate"
            destination = found[0]
        else:
            start, destination = found[0], found[1]

    # Now compute the route
    path = find_route(start, destination)
    description = describe_route(path)

    print(f"\n🗺 Route from {start} to {destination}:\n", description)
    speak(description)
    draw_route(path)

# MAIN LOOP

if __name__ == "__main__":
    print(" Welcome to IGDTUW Virtual Campus Assistant!")
    print("Now you can ask:")
    print(" - 'Where is the CSE Department?'")
    print(" - 'Show path from CSE Department to Canteen.'")
    print(" - 'How to go from Krishna Hostel to Mechanical Department?'")

    while True:
        q = input("\nAsk your query (or type 'exit'): ").strip()
        if q.lower() == "exit":
            speak("Goodbye! Have a great day at IGDTUW!")
            break
        process_campus_query(q)




