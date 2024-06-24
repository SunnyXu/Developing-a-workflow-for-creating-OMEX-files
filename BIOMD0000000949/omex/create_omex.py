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

r = te.loads("Chitnis2008.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#te.saveToFile("promoted.xml", SBML)



r = te.loads("Chitnis2008.xml")
SBML = r.getParamPromotedSBML(r.getSBML())

sedml = libsedml.readSedMLFromFile("../old_SEDML/Chitnis2008.sedml")

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)

plot = sedml.getOutput(0)

plot.setName("Plot of human population against time")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time (days)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(10000)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Number of people")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(60)

curve = plot.getCurve(0)
curve.setStyle("dashed_red")
curve.setName("Exposed humans")
curve = plot.getCurve(1)
curve.setStyle("solid_blue")
curve.setName("Infectious humans")
curve = plot.getCurve(2)
curve.setStyle("dashed_black")
curve.setName("Recovered humans")



plot = sedml.getOutput(1)

plot.setName("Plot of human population against time")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time (days)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(10000)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Number of people")
yaxis.setGrid(False)
yaxis.setMin(480)
yaxis.setMax(600)

curve = plot.getCurve(0)
curve.setStyle("solid_blue")
curve.setName("Susceptible humans")



plot = sedml.getOutput(2)

plot.setName("Plot of mosquito population against time")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time (days)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(10000)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Number of mosquitoes")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(60)


curve = plot.getCurve(0)
curve.setStyle("dashed_red")
curve.setName("Exposed mosquitoes")
curve = plot.getCurve(1)
curve.setStyle("solid_blue")
curve.setName("Infectious mosquitoes")



plot = sedml.getOutput(3)

plot.setName("Plot of mosquito population against time")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time (days)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(10000)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Number of mosquitoes")
yaxis.setGrid(False)
yaxis.setMin(2330)
yaxis.setMax(2410)


curve = plot.getCurve(0)
curve.setStyle("solid_blue")
curve.setName("Susceptible mosquitoes")



style1 = sedml.createStyle()
line1 = style1.createLineStyle()
line1.setColor("0000ff") #blue
line1.setType(libsedml.SEDML_LINETYPE_SOLID)
marker1 = style1.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style1.createFillStyle()
#fill.setColor("#000000FF")
style1.setId("solid_blue")


style1 = sedml.createStyle()
line1 = style1.createLineStyle()
line1.setColor("000000") #black
line1.setType(libsedml.SEDML_LINETYPE_DASH)
marker1 = style1.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style1.createFillStyle()
#fill.setColor("#000000FF")
style1.setId("dashed_black")

style1 = sedml.createStyle()
line1 = style1.createLineStyle()
line1.setColor("ff0000") #red
line1.setType(libsedml.SEDML_LINETYPE_DASH)
marker1 = style1.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style1.createFillStyle()
#fill.setColor("#000000FF")
style1.setId("dashed_red")





#Now fix the fact that tellurium's handling of local parameters is off:
mod1 = sedml.getModel(0)
mod1.setSource("Chitnis2008.xml")

sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("Chitnis2008-Fig2.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["Chitnis200-Fig2.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000000949-Fig2.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

# print(sed)
