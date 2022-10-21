import sys, os, time, numpy, json

dictWire={
 1:{
  "wireSize" : 0.2893, "res" : 0.1264
}, 2:{
  "wireSize" : 0.2576, "res" : 0.1593
}, 3:{
  "wireSize" : 0.2294, "res" : 0.2009
}, 4:{
  "wireSize" : 0.2043, "res" : 0.2533
}, 5:{
  "wireSize" : 0.1819, "res" : 0.3195
}, 6:{
  "wireSize" : 0.1643, "res" : 0.3952
}, 7:{
  "wireSize" : 0.1466, "res" : 0.4981
}, 8:{
  "wireSize" : 0.1306, "res" : 0.6281
}, 9:{
  "wireSize" : 0.1165, "res" : 0.7925
}, 10:{
  "wireSize" : 0.1039, "res" : 0.9988
}, 11:{
  "wireSize" : 0.0927, "res" : 1.2600
}, 12:{
  "wireSize" : 0.0827, "res" : 1.59
}, 13:{
  "wireSize" : 0.0739, "res" : 2.00
}, 14:{
  "wireSize" : 0.0660, "res" : 2.52
}, 15:{
  "wireSize" : 0.0589, "res" : 3.18
}, 16:{
  "wireSize" : 0.0525, "res" : 4.02
}, 17:{
  "wireSize" : 0.0469, "res" : 5.05
}, 18:{
  "wireSize" : 0.0418, "res" : 6.39
}, 19:{
  "wireSize" : 0.0374, "res" : 8.05
}, 20:{
  "wireSize" : 0.0334, "res" : 10.1
}, 21:{
  "wireSize" : 0.0299, "res" : 12.8
}, 22:{
  "wireSize" : 0.0267, "res" : 16.2
}, 23:{
  "wireSize" : 0.0239, "res" : 20.31
}, 24:{
  "wireSize" : 0.0213, "res" : 25.67
}, 25:{
  "wireSize" : 0.0191, "res" : 32.37
}, 26:{
  "wireSize" : 0.0170, "res" : 41.02
}, 27:{
  "wireSize" : 0.0153, "res" : 51.43
}, 28:{
  "wireSize" : 0.0136, "res" : 65.33
}, 29:{
  "wireSize" : 0.0123, "res" : 81.22
}, 30:{
  "wireSize" : 0.0109, "res" : 103.2
}, 31:{
  "wireSize" : 0.0098, "res" : 130.9
}, 32:{
  "wireSize" : 0.0088, "res" : 162.0
}, 33:{
  "wireSize" : 0.0079, "res" : 205.7
}, 34:{
  "wireSize" : 0.0071, "res" : 261.3
}, 35:{
  "wireSize" : 0.0063, "res" : 330.7
}, 36:{
  "wireSize" : 0.0057, "res" : 414.8
}, 37:{
  "wireSize" : 0.0051, "res" : 512.1
}, 38:{
  "wireSize" : 0.0045, "res" : 648.2
}, 39:{
  "wireSize" : 0.0040, "res" : 846.6
}, 40:{
  "wireSize" : 0.0036, "res" : 1079.0
}, 41:{
  "wireSize" : 0.0032, "res" : 1323.0
}, 42:{
  "wireSize" : 0.0028, "res" : 1659.0
}, 43:{
  "wireSize" : 0.0025, "res" : 2143.0
}, 44:{
  "wireSize" : 0.0023, "res" : 2593.0
}, 45:{
  "wireSize" : 0.00206, "res" : 3348.0}}

def Roundoff(v):
  Value = v * 100;
  Value = round(Value);
  Value = Value / 100;
  return Value;


def calculate(wireSize, res, diameter,coilLen,inductance):

  #enter coil Inner Diameter (in inches)
  # diameter = 1
  ##enter ideal coil height
  # coilLen = 0.625


  # for Coil Outer Diameter (in inches = 1)
  DM = 0.03937 # (in mm)
  #for wire diameter (in mm)
  wM = 39.37
  #for wire length scale (in meters)
  WM = 3.281
  #for coil Inner Diameter (in inches = 1)
  dM = 0.03937 #(in mm)
  #for coil Height (in inches =1)
  lM = 0.03937 #(in mm)
  #for coil Inductance (in H =1000, microH = 0.001)
  LM = 1 #(in mH)
    
  coilLen = coilLen * lM

  diameter = diameter * dM

  inductance = inductance * LM
  diammax = diameter;
  currentInd = 0;
  turns = 1;
  diamavg = 0.0;

  turnsPerLevel = coilLen / wireSize;
  while currentInd < inductance:
    diamavg = 0.0;
    diammax = diameter;
    tempTurns = turns;
    while tempTurns > 0.0:
      if tempTurns < turnsPerLevel:
        diamavg += diammax * tempTurns;
      else:
        diamavg += diammax * turnsPerLevel;
      diammax += (2.0*wireSize);
      tempTurns -= turnsPerLevel;
    diamavg /= turns;
    currentInd = ( diamavg / 1000.0 ) * diamavg * turns * turns / (( 18.0 * diamavg ) + ( 40.0 * coilLen ))
    turns += 1
  feet = (diamavg * turns * 3.14159 ) / 12.0;
  resistance = (2.52 * feet ) / 1000.0;
  level = turns / turnsPerLevel;

  return resistance, Roundoff((wireSize*1000)/wM), Roundoff(turns), Roundoff(feet/WM),  Roundoff(diammax/DM), Roundoff(level), Roundoff(turnsPerLevel)
  ##  DC Resistance (R)--- Wire Diameter (in mm)--- Number of Turns--- Wire Length (in meters)--- Coil Outer Diameter (in mm)--- Number of Layers---  Turns per Layer



################################ Function Main (below) ################################
#Enter Inner Diameter Values
minDiam = 0.5
maxDiam = 5

#Enter Coil Height Values
mincoilLen = 0.5
maxcoilLen = 5

#Enter Max Resistance
maxR = 0.18

#Enter Inductance Values (in mH)
minInduct = 0.1
maxInduct = 10

stepInc = 0.01

results = []

totalDiam = (maxDiam-minDiam)/stepInc + 1
totalCoilLen = (maxDiam-minDiam)/ stepInc + 1
print("Total Diam Count: ",round(totalDiam))
print("Total Coil Len Count: ",round(totalCoilLen))

totalWireComb = len(list(dictWire.keys()))
print("Total AWG Wires Count: ",round(totalWireComb))

totalSim = totalDiam*totalCoilLen*totalWireComb
print("total Simulations: ",round(totalSim))
print()
print()
print("Starting in 3 Seconds...")
time.sleep(3)

permCount = 0
try:
    for induct in numpy.arange(minInduct,maxInduct,stepInc):
        for key, val in dictWire.items():
            for diam in numpy.arange(minDiam,maxDiam,stepInc):
                for coilLen in numpy.arange(mincoilLen,maxcoilLen,stepInc):
                    permCount += 1
                    print()
                    print()
                    print("Simulation No. ",permCount," (of ",totalSim,"total, current AWG:",key,")")
                    r, wd, nT, wL, cOD, nL, TpL = calculate(val["wireSize"], val["res"], diam, coilLen,induct)
                    newDict = {
                            "simNum":permCount,
                            "resistance": r,
                            "awg": key,
                            "inductance": induct,
                            "coilHeight(mm)": coilLen,
                            "wireDiameter(mm)": wd,
                            "coilInnerDiameter(mm)": diam,
                            "coilOuterDiameter(mm)": cOD ,
                            "numOfTurns": nT,
                            "totalWireLen(meters)":wL,
                            "numOfLayers": nL,
                            "turnsPerLayer": TpL
                    }
                    results.append(newDict)
    with open('result.json', 'w') as fp:
        json.dump(results, fp)
except KeyboardInterrupt:
    try:
        with open('result.json', 'w') as fp:
            json.dump(results, fp)
        print('Keyboard Interrupt Detected...')
        print('Number of Matched Criteria found so far: ',len(results))



        print("Json File Dumped...")
        print("Program End")

          # for item in results:
          #   print("Simulation No:",item["simNum"])
          #   print("Resistance: ",item["resistance"])
          #   print("Wire Diameter: ",item["wireDiameter"])
          #   print("No. Of Turns:",item["numOfTurns"])
          #   print("Wire Length: ",item["wireLen"])
          #   print("Coil Outer Diameter: ",item["coilOuterDiameter"])
          #   print("Num Of Layers: ",item["numOfLayers"])
          #   print("Turns Per Layer: ",item["turnsPerLayer"])

        sys.exit(0)
    except SystemExit:
        os._exit(0)

