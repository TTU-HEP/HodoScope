import random
import math
import numpy as np
import ROOT
ROOT.gROOT.SetBatch(True)

def makeBranch(tree, name, t):
    b = None
    if t == "vector":
        b = ROOT.vector('double')()
        tree.Branch(name, b)
    elif t == "D":
        b = np.zeros(1, dtype=float)
        tree.Branch(name, b, name+"/"+t)
    else:
        print("Branch type not supported yet. Add it here")
    return b
    
def saveHisto(c, hDic, name, drawOpt=""):
    hDic[name].Draw(drawOpt)
    c.SaveAs(name+".png")    

def rand(m=0,M=100):
    a = random.uniform(m,M)
    return a

def find_nearest(array, value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return array[idx-1], idx-1
    else:
        return array[idx], idx

def getLocalX(x, p):
    localXtruth = x
    if localXtruth > p/2.0:
        localXtruth -= p/2.0
    elif localXtruth < p/2.0:
        localXtruth += p/2.0
    else:
        pass
    return localXtruth
    
def getADCForTriangle(p, x):
    #p1 = (-pitch/2, 0)
    #p2 = (0, h)
    #p3 = (pitch/2, 0)
    h=1.0
    f=10.0
    d = None
    if x < -p/2.0:
        d = 0
    elif -p/2.0 <= x and x < 0:
        d = (2*h/p)*x + h
    elif 0 <= x and x < p/2.0:
        d = -(2*h/p)*x + h
    elif p/2.0 <= x:
        d = 0
    return f*d

def getADCForBinary(p, x):
    h=1.0
    f=10.0
    d = None
    if x < -p/2.0:
        d = 0
    elif -p/2.0 <= x and x <= p/2.0:
        d = h
    elif p/2.0 < x:
        d = 0
    return f*d

def getNoise(m, w):
    n = random.gauss(m,w)
    return n

def fullGeo(pitch):
    info = {}
    info["pitch"] = pitch
    info["nchannel"] = 32
    info["xmidloc"] = np.arange(-(info["nchannel"])*info["pitch"]/2.0, (info["nchannel"])*info["pitch"]/2.0 + info["pitch"], info["pitch"]).tolist()
    info["xmidloc2"] = np.arange(-(info["nchannel"])*info["pitch"]/2.0-info["pitch"]/2.0, (info["nchannel"])*info["pitch"]/2.0 + info["pitch"]/2.0, info["pitch"]).tolist()    
    return info
    
def main():
    # Some useful hardcoded stuff
    nEvents = 100000
    nBins = 400
    low  = -10.0
    high =  10.0
    pitch = 2.0
    outfile = "hodoScopeData.root"
    meanNoise = 2.0
    widthNoise = 1.0

    # Define TTrees and TBranches
    root_file = ROOT.TFile(outfile, "RECREATE")
    tree = ROOT.TTree("tree","tree")
    amp1_   = makeBranch(tree, "amp1", "vector")
    amp2_   = makeBranch(tree, "amp2", "vector")
    xtruth_ = makeBranch(tree, "xtruth", "D")
    
    # Define histos
    histos = {}
    histos["xtruth"] = ROOT.TH1D("xtruth","xtruth; x_{truth} [mm]; events", nBins,-15,15); histos["xtruth"].SetMinimum(0)
    histos["xreco"] = ROOT.TH1D("xreco","xreco; x_{reco} [mm]; events", nBins,-15,15); histos["xreco"].SetMinimum(0)
    histos["xdiff"] = ROOT.TH1D("xdiff","xdiff; xdiff [mm]; events", 100,-20,20)
    histos["binary_adc_x"] = ROOT.TH2D("binary_adc_x","binary_adc_x; x_{truth} [mm]; adc; events", nBins,-pitch,pitch, 100,0,15)
    histos["tri_adc_x"] = ROOT.TH2D("tri_adc_x","tri_adc_x; x_{truth} [mm]; adc; events", nBins,-pitch,pitch, 100,0,15)
    histos["binary_adcMax_x"] = ROOT.TH2D("binary_adcMax_x","binary_adcMax_x; x_{truth} [mm]; adc; events", nBins,-15,15, 100,0,15)
    histos["tri1_adcMax_x"] = ROOT.TH2D("tri1_adcMax_x","tri1_adcMax_x; x_{truth} [mm]; adc; events", nBins,-15,15, 100,0,15)
    histos["tri2_adcMax_x"] = ROOT.TH2D("tri2_adcMax_x","tri2_adcMax_x; x_{truth} [mm]; adc; events", nBins,-15,15, 100,0,15)
    
    # TrackerGeo
    geo = fullGeo(pitch)
    print(geo)
    
    # Loop over events
    for i in range(nEvents):
        # Generate Truth level info
        xtruth = rand(low, high)
        #xtruth = random.gauss(0.0, 2.5)

        #############################################
        # Calculate adc per channel
        #############################################

        # Plane 1
        maxChannelX1, maxChannelIdx1 = find_nearest(geo["xmidloc"], xtruth)
        ampBinary = [-10.0]*len(geo["xmidloc"])
        ampTri1 = [-10.0]*len(geo["xmidloc"])
        for i in range(len(geo["xmidloc"])):
            if i == maxChannelIdx1:
                localX1 = xtruth-geo["xmidloc"][i]
                ampBinary[i] = getADCForBinary(pitch, localX1) + getNoise(meanNoise, widthNoise)
                ampTri1[i] = getADCForTriangle(pitch, localX1) + getNoise(meanNoise, widthNoise)
            else:
                ampBinary[i] = 0.0
                ampTri1[i] = 0.0
        ampMaxBinary = max(ampBinary)
        ampMaxTri1 = max(ampTri1)

        # Plane 2
        maxChannelX2, maxChannelIdx2 = find_nearest(geo["xmidloc2"], xtruth)
        #ampBinary = [-10.0]*len(geo["xmidloc2"])
        ampTri2 = [-10.0]*len(geo["xmidloc2"])
        for i in range(len(geo["xmidloc2"])):
            if i == maxChannelIdx2:
                localX2 = xtruth-geo["xmidloc2"][i] #getLocalX(xtruth-geo["xmidloc2"][i], pitch)
                #ampBinary[i] = getADCForBinary(pitch, localX1)
                ampTri2[i] = getADCForTriangle(pitch, localX2)
            else:
                #ampBinary[i] = 0.0
                ampTri2[i] = 0.0
        #ampMaxBinary = max(ampBinary)
        ampMaxTri2 = max(ampTri2)

        
        # Calculate xreco
        xreco = maxChannelX1
        xrecoTriangle = maxChannelX1

        # Fill histos
        histos["xtruth"].Fill(xtruth)
        histos["xreco"].Fill(xreco)
        histos["xdiff"].Fill(xtruth - xreco)
        histos["binary_adc_x"].Fill(xtruth, getADCForBinary(pitch, xtruth))
        histos["tri_adc_x"].Fill(xtruth, getADCForTriangle(pitch, xtruth))
        histos["binary_adcMax_x"].Fill(xtruth, ampMaxBinary)
        histos["tri1_adcMax_x"].Fill(xtruth, ampMaxTri1)
        histos["tri2_adcMax_x"].Fill(xtruth, ampMaxTri2)

        # Save to TTree
        xtruth_[0] = xtruth
        for x in ampTri1:
            amp1_.push_back(x)
        for x in ampTri2:
            amp2_.push_back(x)

        tree.Fill()
        amp1_.clear()
        amp2_.clear()
        
    # Draw histos
    c1 = ROOT.TCanvas( "c", "c", 800, 700)
    saveHisto(c1, histos, "xtruth")
    saveHisto(c1, histos, "xreco")
    saveHisto(c1, histos, "xdiff")
    saveHisto(c1, histos, "binary_adc_x", "colz")
    saveHisto(c1, histos, "tri_adc_x", "colz")
    saveHisto(c1, histos, "binary_adcMax_x", "colz")
    saveHisto(c1, histos, "tri1_adcMax_x", "colz")
    saveHisto(c1, histos, "tri2_adcMax_x", "colz")

    # Write everything out
    root_file.Write()
    tree.Write()
    root_file.Close()
        
if __name__ == '__main__':
    main()
