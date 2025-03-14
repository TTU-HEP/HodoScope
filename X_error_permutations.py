import ROOT
import matplotlib.pyplot as plt

# making the histogram
def plot_x_error(input_file):
    root_file = ROOT.TFile(input_file, "READ")
    x_error_tree = root_file.Get("x_error_tree")
    x_error_hist = ROOT.TH1F("x_error_hist", "Histogram of x_error values", 300, -10, 10) 
    
    
    for event_num in range(x_error_tree.GetEntries()):
        x_error_tree.GetEntry(event_num)
        
        x_error_value = x_error_tree.x_error[0]  
        
        x_error_hist.Fill(x_error_value)
    
    canvas = ROOT.TCanvas("canvas", "x_error Histogram", 800, 600)
    x_error_hist.Draw()
    
    canvas.SaveAs("x_error_histogram.png")
    
    root_file.Close()
    
    print("Histogram saved as x_error_histogram.png")

# Example usage: Plot the x_error values from the output ROOT file
plot_x_error("x_error_values.root")
