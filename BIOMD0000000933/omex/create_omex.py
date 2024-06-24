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

r = te.loads("Kosiuk2015.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
te.saveToFile("promoted.xml", SBML)


r = te.loads("Kosiuk2015.xml")
SBML = r.getParamPromotedSBML(r.getSBML())

sedml = libsedml.readSedMLFromFile("../old_SEDML/Kosiuk2015.sedml")

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)

plot = sedml.getOutput(0)

plot.setName("Figure 3")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName(" ")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(40)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName(" ")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(1.1)

curve = plot.getCurve(0)
curve.setStyle("solid_green")
curve.setName("C")
curve = plot.getCurve(1)
curve.setStyle("solid_black")
curve.setName("M")
curve = plot.getCurve(2)
curve.setStyle("dashed_black")
curve.setName("X")



style1 = sedml.createStyle()
line1 = style1.createLineStyle()
line1.setColor("728f02")
line1.setType(libsedml.SEDML_LINETYPE_SOLID)
marker1 = style1.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style1.createFillStyle()
#fill.setColor("#000000FF")
style1.setId("solid_green")

style2 = sedml.createStyle()
line2 = style2.createLineStyle()
line2.setColor("000000") #balck
line2.setType(libsedml.SEDML_LINETYPE_SOLID)
marker2 = style2.createMarkerStyle()
marker2.setType(libsedml.SEDML_MARKERTYPE_NONE)
style2.setId("solid_black")

style2 = sedml.createStyle()
line2 = style2.createLineStyle()
line2.setColor("000000") #balck
line2.setType(libsedml.SEDML_LINETYPE_DASH)
marker2 = style2.createMarkerStyle()
marker2.setType(libsedml.SEDML_MARKERTYPE_NONE)
style2.setId("dashed_black")




#Now fix the fact that tellurium's handling of local parameters is off:
mod1 = sedml.getModel(0)
mod1.setSource("Kosiuk2015.xml")


sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("Kosiuk2015.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["Kosiuk2015.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000000933.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

# print(sed)
