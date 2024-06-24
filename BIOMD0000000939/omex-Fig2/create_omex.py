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

r = te.loads("Iwamoto2010.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#te.saveToFile("promoted.xml", SBML)


r = te.loads("Iwamoto2010.xml")
SBML = r.getParamPromotedSBML(r.getSBML())

sedml = libsedml.readSedMLFromFile("../old_SEDML/iwamoto2010_Fig2.sedml")

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)

plot = sedml.getOutput(0)

plot.setName("Figure 2")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time (-)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(6000)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Concentration (-)")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(20)

curve = plot.getCurve(0)
curve.setStyle("solid_orange")
curve.setName("APC$^{cdc20}$")
curve = plot.getCurve(1)
curve.setStyle("solid_blue")
curve.setName("tCycA")
curve = plot.getCurve(2)
curve.setStyle("solid_pink")
curve.setName("tCycB")
curve = plot.getCurve(3)
curve.setStyle("solid_light_blue")
curve.setName("aCycE/Cdk2")
curve = plot.getCurve(4)
curve.setStyle("solid_green")
curve.setName("tCycE")
curve = plot.getCurve(5)
curve.setStyle("solid_red")
curve.setName("p27")



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
line1.setColor("#FF7F50") #orange
line1.setType(libsedml.SEDML_LINETYPE_SOLID)
marker1 = style1.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style1.createFillStyle()
#fill.setColor("#000000FF")
style1.setId("solid_orange")

style1 = sedml.createStyle()
line1 = style1.createLineStyle()
line1.setColor("00ff00") #green
line1.setType(libsedml.SEDML_LINETYPE_SOLID)
marker1 = style1.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style1.createFillStyle()
#fill.setColor("#000000FF")
style1.setId("solid_green")

style1 = sedml.createStyle()
line1 = style1.createLineStyle()
line1.setColor("ff0000") #red
line1.setType(libsedml.SEDML_LINETYPE_SOLID)
marker1 = style1.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style1.createFillStyle()
#fill.setColor("#000000FF")
style1.setId("solid_red")

style1 = sedml.createStyle()
line1 = style1.createLineStyle()
line1.setColor("#FF69B4") #pink
line1.setType(libsedml.SEDML_LINETYPE_SOLID)
marker1 = style1.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style1.createFillStyle()
#fill.setColor("#000000FF")
style1.setId("solid_pink")

style1 = sedml.createStyle()
line1 = style1.createLineStyle()
line1.setColor("ADD8E6") #light blue
line1.setType(libsedml.SEDML_LINETYPE_SOLID)
marker1 = style1.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style1.createFillStyle()
#fill.setColor("#000000FF")
style1.setId("solid_light_blue")


#Now fix the fact that tellurium's handling of local parameters is off:
mod1 = sedml.getModel(0)
mod1.setSource("Iwamoto2010.xml")

sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("iwamoto2010_Fig2.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["iwamoto2010_Fig2.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000000939-Fig2.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

# print(sed)
