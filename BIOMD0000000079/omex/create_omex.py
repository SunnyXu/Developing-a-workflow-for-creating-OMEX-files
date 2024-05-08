import tellurium as te
import phrasedml 
import libsedml
import os
from biosimulators_utils.combine.io import CombineArchiveWriter  # type: ignore
from biomodels_qc.utils import build_combine_archive

combine_writer = CombineArchiveWriter()

def removeModelRefsFromDataGenerators(sedml):
    for dg in range(sedml.getNumDataGenerators()):
        datagen = sedml.getDataGenerator(dg)
        for v in range(datagen.getNumVariables()):
            var = datagen.getVariable(v)
            var.setModelReference("")

def globalToLocalParameter(target):
    core_id = target.split("'")[1]
    (rxn, param) = core_id.split("_")
    return "/sbml:sbml/sbml:model/sbml:listOfReactions/sbml:reaction[@id='" + rxn + "']/sbml:kineticLaw/sbml:listOfParameters/sbml:parameter[@id='" + param + "']/@value"

r = te.loads("BIOMD0000000079_url.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#te.saveToFile("promoted.xml", SBML)


phrased = phrasedml.convertFile(r"C:\Users\Lucian\Desktop\temp-biomodels\manual_curation\BIOMD0000000079\new_curation\BIOMD0000000079_url.sedml")

sed = phrasedml.convertString("""
// Created by libphrasedml v1.3.0
// Models
mod_v01 = model "BIOMD0000000079_url.xml" with P = 0.1, P = 0.01, P = 0.01, P = 0.01, P = 0.01, P=0.25, Q=0.9, R=0.02
mod_v12 = model mod_v01 with P = 1.2
mod_v23 = model mod_v01 with P = 2.3
mod_v34 = model mod_v01 with P = 3.4
mod_v45 = model mod_v01 with P = 4.5
mod_v56 = model mod_v01 with P = 5.6
mod_v67 = model mod_v01 with P = 6.7
mod_v78 = model mod_v01 with P = 7.8
mod_v89 = model mod_v01 with P = 8.9
mod_v100 = model mod_v01 with P = 10.0

BIOMD0000000079_url = model "BIOMD0000000079_url.xml" with P=0.43, Q=0.73, R=0.55
//BIOMD0000000079_url = model mod_v01 with P=0.43, Q=0.73, R=0.55

// Simulations
fig3 = simulate uniform(0, 40, 1000)

// Tasks
fig3task = run fig3 on BIOMD0000000079_url

// Outputs

// Simulations
sim1 = simulate uniform(0, 140, 1000)

// Tasks
task1 = run sim1 on mod_v01
task2 = run sim1 on mod_v12
task3 = run sim1 on mod_v23
task4 = run sim1 on mod_v34
task5 = run sim1 on mod_v45
task6 = run sim1 on mod_v56
task7 = run sim1 on mod_v67
task8 = run sim1 on mod_v78
task9 = run sim1 on mod_v89
task10 = run sim1 on mod_v100

// Outputs
report "Full report for tasks 1-10, including all symbols in SBML with mathematical meaning, both constant and variable." task1.time, task1.P, task1.Q, task1.R, task1.body, task1.reaction_0, task1.reaction_1, task1.reaction_2, task1.reaction_3, task1.reaction_4, task1.reaction_5, task2.P, task2.Q, task2.R, task2.body, task2.reaction_0, task2.reaction_1, task2.reaction_2, task2.reaction_3, task2.reaction_4, task2.reaction_5, task3.P, task3.Q, task3.R, task3.body, task3.reaction_0, task3.reaction_1, task3.reaction_2, task3.reaction_3, task3.reaction_4, task3.reaction_5, task4.P, task4.Q, task4.R, task4.body, task4.reaction_0, task4.reaction_1, task4.reaction_2, task4.reaction_3, task4.reaction_4, task4.reaction_5, task5.P, task5.Q, task5.R, task5.body, task5.reaction_0, task5.reaction_1, task5.reaction_2, task5.reaction_3, task5.reaction_4, task5.reaction_5, task6.P, task6.Q, task6.R, task6.body, task6.reaction_0, task6.reaction_1, task6.reaction_2, task6.reaction_3, task6.reaction_4, task6.reaction_5, task7.P, task7.Q, task7.R, task7.body, task7.reaction_0, task7.reaction_1, task7.reaction_2, task7.reaction_3, task7.reaction_4, task7.reaction_5, task8.P, task8.Q, task8.R, task8.body, task8.reaction_0, task8.reaction_1, task8.reaction_2, task8.reaction_3, task8.reaction_4, task8.reaction_5, task9.P, task9.Q, task9.R, task9.body, task9.reaction_0, task9.reaction_1, task9.reaction_2, task9.reaction_3, task9.reaction_4, task9.reaction_5, task10.P, task10.Q, task10.R, task10.body, task10.reaction_0, task10.reaction_1, task10.reaction_2, task10.reaction_3, task10.reaction_4, task10.reaction_5
plot "Figure 3" fig3task.time vs fig3task.P, fig3task.Q, fig3task.R
plot "Figure 4 V4 = 0.1" task1.time vs task1.P, task2.P, task3.P, task4.P, task5.P, task6.P, task7.P, task8.P, task9.P, task10.P 
""")


sedml = libsedml.readSedMLFromString(sed)

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)

for m in range(10):
    mod = sedml.getModel(m)
    change = mod.getChange(0)
    change.setTarget(r"/sbml:sbml/sbml:model/sbml:listOfReactions/sbml:reaction[@id=&apos;reaction_5&apos;]/sbml:kineticLaw/sbml:listOfParameters/sbml:parameter[@id=&apos;V&apos;]/@value")
    

mod = sedml.getModel(0)
change = mod.getChange(1)
change.setTarget(r"/sbml:sbml/sbml:model/sbml:listOfReactions/sbml:reaction[@id=&apos;reaction_2&apos;]/sbml:kineticLaw/sbml:listOfParameters/sbml:parameter[@id=&apos;K1&apos;]/@value")

change = mod.getChange(2)
change.setTarget(r"/sbml:sbml/sbml:model/sbml:listOfReactions/sbml:reaction[@id=&apos;reaction_3&apos;]/sbml:kineticLaw/sbml:listOfParameters/sbml:parameter[@id=&apos;K2&apos;]/@value")

change = mod.getChange(3)
change.setTarget(r"/sbml:sbml/sbml:model/sbml:listOfReactions/sbml:reaction[@id=&apos;reaction_4&apos;]/sbml:kineticLaw/sbml:listOfParameters/sbml:parameter[@id=&apos;k3&apos;]/@value")

change = mod.getChange(4)
change.setTarget(r"/sbml:sbml/sbml:model/sbml:listOfReactions/sbml:reaction[@id=&apos;reaction_5&apos;]/sbml:kineticLaw/sbml:listOfParameters/sbml:parameter[@id=&apos;Km&apos;]/@value")


plot = sedml.getOutput(1)

plot.setName("Figure 3A")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(40)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("P")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(1.1)

curve = plot.getCurve(0)
curve.setStyle("solid_blue")
curve.setName("P")

curve = plot.getCurve(1)
curve.setStyle("solid_red")
curve.setName("Q")

curve = plot.getCurve(2)
curve.setStyle("solid_green")
curve.setName("R")


plot = sedml.getOutput(2)

plot.setName("Figure 4")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(140)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("P")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(2)

curve = plot.getCurve(0)
curve.setName("V4 = 0.1")

curve = plot.getCurve(1)
curve.setName("V4 = 1.2")

curve = plot.getCurve(2)
curve.setName("V4 = 2.3")

curve = plot.getCurve(3)
curve.setName("V4 = 3.4")

curve = plot.getCurve(4)
curve.setName("V4 = 4.5")

curve = plot.getCurve(5)
curve.setName("V4 = 5.6")

curve = plot.getCurve(6)
curve.setName("V4 = 6.7")

curve = plot.getCurve(7)
curve.setName("V4 = 7.8")

curve = plot.getCurve(8)
curve.setName("V4 = 8.9")

curve = plot.getCurve(9)
curve.setName("V4 = 10.0")





style1 = sedml.createStyle()
line1 = style1.createLineStyle()
line1.setColor("C03E68") #blue
line1.setType(libsedml.SEDML_LINETYPE_SOLID)
marker1 = style1.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style1.createFillStyle()
#fill.setColor("#000000FF")
style1.setId("solid_red")


style2 = sedml.createStyle()
line1 = style2.createLineStyle()
line1.setColor("007948") #blue
line1.setType(libsedml.SEDML_LINETYPE_SOLID)
marker1 = style2.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style2.createFillStyle()
#fill.setColor("#000000FF")
style2.setId("solid_green")


style3 = sedml.createStyle()
line1 = style3.createLineStyle()
line1.setColor("0000ff") #blue
line1.setType(libsedml.SEDML_LINETYPE_SOLID)
marker1 = style3.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style3.createFillStyle()
#fill.setColor("#000000FF")
style3.setId("solid_blue")




#Now fix the fact that tellurium's handling of local parameters is off:
mod1 = sedml.getModel(0)
mod1.setSource("BIOMD0000000079_url.xml")

sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("BIOMD0000000079_url.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["BIOMD0000000079_url-Fig6-Ki=0.1.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000000079.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

# print(sed)
