import math
import random
import ROOT  # ROOT for storing data in a TTree

# Function to generate the circle grid 
def generate_circle_grid(rows, cols, radius, col_spacing, row_spacing, col_offset):
    # Store circle centers and labels for path length tracking
    circle_centers = []
    circle_labels = []
    
    for i in range(rows):
        for j in range(cols):
            # Verticle offset function for every other column
            vertical_offset = col_offset if j % 2 == 1 else 0
            
            # Compute the position of each circle based on spacing and offset
            x_pos = j * (2 * radius + col_spacing)
            y_pos = -i * (2 * radius + row_spacing) + vertical_offset
            
            # Assign channel numbers based on column parity and row position
            if j % 2 == 0:  # Even columns
                if i < 4:  # Top half (first 4 rows)
                    channel = (j // 2) % 16 + 1  # Labels 1-16, same for top half of each column
                else:  # Bottom half (last 4 rows)
                    channel = (j // 2) // 2 + 1  # Bottom half labeled 1,1,2,2,...,16,16 for even columns
            else:  # Odd columns
                if i < 4:  # Top half (first 4 rows)
                    channel = (j // 2) % 16 + 17  # Labels 17-32, same for top half of each column
                else:  # Bottom half (last 4 rows)
                    channel = (j // 2) // 2 + 17  # Bottom half labeled 17,17,18,18,...,32,32 for odd columns
            
            # Store circle center and label for tracking path length
            circle_centers.append((x_pos, y_pos))
            circle_labels.append(channel)
    
    return circle_centers, circle_labels

# Function to track the vertical line path (updated to calculate correct path lengths)
def track_vertical_line_path(circles_centers, circles_labels, line_x_position, radius):
    path_lengths = {i: 0 for i in range(1, 65)}  # Initialize all path lengths to 0 (labels 1-64)
    
    # Iterate over all circles and check if the vertical line intersects them
    for i, (x_pos, y_pos) in enumerate(circles_centers):
        label = circles_labels[i]
        
        # Calculate the horizontal distance between the line and the circle center
        d = abs(x_pos - line_x_position)
        
        # Check if the vertical line intersects the circle (i.e., d <= radius)
        if d <= radius:
            # Calculate the path length 
            path_length = 2 * math.sqrt(radius**2 - d**2)
            
            # Add the path length for the current label
            path_lengths[label] += path_length
    
    return path_lengths

# Function to generate a random x position for the vertical line
def generate_random_x_position(cols, radius, col_spacing):
    min_x = 0
    max_x = (cols - 1) * (2 * radius + col_spacing)
    random_x = random.uniform(min_x, max_x)
    return random_x

# Function to create a ROOT TTree and store the results
def create_root_tree():
    # Create a ROOT file to store the TTree
    root_file = ROOT.TFile("hodoscope_simulation.root", "RECREATE")
    
    # Create a TTree to store the path lengths for each event
    tree = ROOT.TTree("path_lengths", "Path lengths for each event")
    
    # Define branches to store the path length data for each label
    labels = ROOT.std.vector("int")()  # Vector to store labels for the event
    lengths = ROOT.std.vector("float")()  # Vector to store corresponding path lengths
    line_x_position = ROOT.vector('float')(1)  # Store the x position of the line for each event
    
    tree.Branch("labels", labels)
    tree.Branch("lengths", lengths)
    tree.Branch("line_x_position", line_x_position)  # Branch for the line x position
    
    return root_file, tree, labels, lengths, line_x_position

# Function to simulate multiple events and store the data in ROOT
def run_simulation(events, rows, cols, radius, col_spacing, row_spacing, col_offset):
    # Generate the circle grid
    circle_centers, circle_labels = generate_circle_grid(rows, cols, radius, col_spacing, row_spacing, col_offset)
    
    # Create ROOT TTree to store the results
    root_file, tree, labels, lengths, line_x_position = create_root_tree()
    
    # Loop over the desired number of events
    for event_num in range(events):
        # Generate a random x position for the vertical line in this event
        line_x_pos = generate_random_x_position(cols, radius, col_spacing)
        
        # Track the path lengths for this vertical line
        path_lengths = track_vertical_line_path(circle_centers, circle_labels, line_x_pos, radius)
        
        # Clear previous event data
        labels.clear()
        lengths.clear()
        line_x_position[0] = line_x_pos  # Store the line x position for this event
        
        # Store the labels and corresponding path lengths for this event
        for label in range(1, 65):
            labels.push_back(label)
            lengths.push_back(path_lengths[label])
        
        # Fill the TTree with this event's data
        tree.Fill()
    
    # Write the TTree to the ROOT file
    root_file.Write()
    root_file.Close()

# Example usage: Run the simulation for n events
run_simulation(events=10000000, rows=8, cols=64, radius=0.25, col_spacing=-0.1, row_spacing=0.3, col_offset=0.4)
