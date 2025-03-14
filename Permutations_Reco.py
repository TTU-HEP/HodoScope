import ROOT

# Reconstruction Function
def calculate_reco_x(triggered_labels):
    # Reconstruction logic (so many if statements)
    if set(triggered_labels) == {1}:
        return 0.0
    elif set(triggered_labels) == {1, 17}:
        return 0.2
    # accounting for the edge case where two single label columns are triggered
    elif set(triggered_labels) == {17}:
        return 0.4
    elif set(triggered_labels) == {1, 2}:
        return 0.8
    elif set(triggered_labels) == {17, 18}:
        return 1.2
    elif set(triggered_labels) == {2, 3}:
        return 1.6
    elif set(triggered_labels) == {18, 19}:
        return 2.0
    elif set(triggered_labels) == {2, 4}:
        return 2.4
    elif set(triggered_labels) == {18, 20}:
        return 2.8
    elif set(triggered_labels) == {3, 5}:
        return 3.2
    elif set(triggered_labels) == {19, 21}:
        return 3.6
    elif set(triggered_labels) == {3, 6}:
        return 4.0
    elif set(triggered_labels) == {19, 22}:
        return 4.4
    elif set(triggered_labels) == {4, 7}:
        return 4.8
    elif set(triggered_labels) == {20, 23}:
        return 5.2
    elif set(triggered_labels) == {4, 8}:
        return 5.6
    elif set(triggered_labels) == {20, 24}:
        return 6.0
    elif set(triggered_labels) == {5, 9}:
        return 6.4
    elif set(triggered_labels) == {21, 25}:
        return 6.8
    elif set(triggered_labels) == {5, 10}:
        return 7.2
    elif set(triggered_labels) == {21, 26}:
        return 7.6
    elif set(triggered_labels) == {6, 11}:
        return None
        # this column is causing issues because it has the same label's trigger as the column that returns 16.8 why its currently set to none
    elif set(triggered_labels) == {22, 27}:
        return None
            # this column is causing issues because it has the same label's trigger as the column that returns 17.2 why its currently set to none
    elif set(triggered_labels) == {6, 12}:
        return 8.8
    elif set(triggered_labels) == {22, 28}:
        return 9.2
    elif set(triggered_labels) == {7, 13}:
        return 9.6
    elif set(triggered_labels) == {23, 29}:
        return 10.0
    elif set(triggered_labels) == {7, 14}:
        return 10.4
    elif set(triggered_labels) == {23, 30}:
        return 10.8
    elif set(triggered_labels) == {8, 15}:
        return 11.2
    elif set(triggered_labels) == {24, 31}:
        return 11.6
    elif set(triggered_labels) == {8, 16}:
        return 12.0
    elif set(triggered_labels) == {24, 32}:
        return 12.4
    elif set(triggered_labels) == {1, 9}:
        return 12.8
    elif set(triggered_labels) == {17, 25}:
        return 13.2
    elif set(triggered_labels) == {2, 9}:
        return 13.6
    elif set(triggered_labels) == {18, 25}:
        return 14.0
    elif set(triggered_labels) == {3, 10}:
        return 14.4
    elif set(triggered_labels) == {19, 26}:
        return 14.8
    elif set(triggered_labels) == {4, 10}:
        return 15.2
    elif set(triggered_labels) == {20, 26}:
        return 15.6
    elif set(triggered_labels) == {5, 11}:
        return 16.0
    elif set(triggered_labels) == {21, 27}:
        return 16.4
    elif set(triggered_labels) == {6, 11}:
        return None
        # this column is causing issues because it has the same label's trigger as the column that returns 8.0 why its currently set to none
    elif set(triggered_labels) == {22, 27}:
        return None
        # this column is causing issues because it has the same label's trigger as the column that returns 8.4 why its currently set to none
    elif set(triggered_labels) == {7, 12}:
        return 17.6
    elif set(triggered_labels) == {23, 28}:
        return 18.0
    elif set(triggered_labels) == {8, 12}:
        return 18.4
    elif set(triggered_labels) == {24, 28}:
        return 18.8
    elif set(triggered_labels) == {9, 13}:
        return 19.2
    elif set(triggered_labels) == {25, 29}:
        return 19.6
    elif set(triggered_labels) == {10, 13}:
        return 20.0
    elif set(triggered_labels) == {26, 29}:
        return 20.4
    elif set(triggered_labels) == {11, 14}:
        return 20.8
    elif set(triggered_labels) == {27, 30}:
        return 21.2
    elif set(triggered_labels) == {12, 14}:
        return 21.6
    elif set(triggered_labels) == {28, 30}:
        return 22.0
    elif set(triggered_labels) == {13, 15}:
        return 22.4
    elif set(triggered_labels) == {29, 31}:
        return 22.8
    elif set(triggered_labels) == {14, 15}:
        return 23.2
    elif set(triggered_labels) == {30, 31}:
        return 23.6
    elif set(triggered_labels) == {15, 16}:
        return 24.0
    elif set(triggered_labels) == {31, 32}:
        return 24.4
    elif set(triggered_labels) == {16}:
        return 24.8
    elif set(triggered_labels) == {32}:
        return 25.2
    elif set(triggered_labels) == {16, 32}:
        return 25.0
    # accounting for the edge case where two single label columns are hit
    else:
        return None  # Was there for debugging earlier, expected output is no events returning none

# Saving output files to another root file because trying to fill the histogram in this file was crashing my computer and some reconstruction logic
def reconstruction(input_file, output_file):
    # Open the ROOT file
    root_file = ROOT.TFile(input_file, "READ")
    
    # Create a new ROOT file to store the x_error values
    output_root_file = ROOT.TFile(output_file, "RECREATE")
    
    # Create a new TTree to store x_error values
    x_error_tree = ROOT.TTree("x_error_tree", "Tree with x_error values")
    
    # Create a branch to store the x_error
    x_error = ROOT.vector('float')()  # This will store the x_error value for each event
    x_error_tree.Branch("x_error", x_error)
    
    # Get the TTree containing path lengths and line_x_position
    tree = root_file.Get("path_lengths")
    
    # Loop over all events
    for event_num in range(tree.GetEntries()):
        # Get the current event
        tree.GetEntry(event_num)
        
        # Get the path lengths for each event
        lengths = tree.lengths  # Path lengths for each "label"
        line_x_position = tree.line_x_position  # True x pos
        
        # Access the first element if line_x_position is a vector (check type using ROOT.vector('float'))
        if isinstance(line_x_position, ROOT.vector('float')):
            true_line_x = line_x_position[0]
        else:
            true_line_x = line_x_position
        
        # Finding the average path length to help determine which labels are considered triggered
        avg_path_length = sum(lengths) / len(lengths)  
        
        # Find triggered labels (path length > 6 * avg path length)
        event_triggered_labels = []
        for i, length in enumerate(lengths):
            if length > 6 * avg_path_length:
                # Add the label (i + 1 because labels are 1-indexed) to the list of triggered labels
                event_triggered_labels.append(i + 1)
        
        # If more than 2 labels triggered, apply the logic to sum the path lengths from 1-16 and 17-32 (help prevent multiplicity by chosing which of the two hit columns has the higher amplitude)
        if len(event_triggered_labels) > 2:
            # Separate the labels into two groups: 1-16 and 17-32
            group_1_sum = sum(lengths[i-1] for i in event_triggered_labels if 1 <= i <= 16)
            group_2_sum = sum(lengths[i-1] for i in event_triggered_labels if 17 <= i <= 32)
            
            # Determine which group has the larger sum of path lengths
            if group_1_sum > group_2_sum:
                # Only keep the labels from 1-16
                event_triggered_labels = [label for label in event_triggered_labels if 1 <= label <= 16]
            else:
                # Only keep the labels from 17-32
                event_triggered_labels = [label for label in event_triggered_labels if 17 <= label <= 32]
        
        # Calculate the reconstructed x position (reco_x) based on triggered labels
        reco_x = calculate_reco_x(event_triggered_labels)
        
        # Check if reco_x is None before calculating x_error
        if reco_x is not None:
            # Calculate the x_error (true line_x position - reco_x)
            x_error_value = true_line_x - reco_x
            x_error.clear()  # Clear the vector
            x_error.push_back(x_error_value)  # Add the x_error value to the branch
            
            # Fill the tree with the x_error value
            x_error_tree.Fill()
    
    # Write the tree to the output ROOT file
    output_root_file.Write()
    
    root_file.Close()
    output_root_file.Close()
    
    print("x_error values have been saved to", output_file)

reconstruction("hodoscope_simulation.root", "x_error_values.root")
