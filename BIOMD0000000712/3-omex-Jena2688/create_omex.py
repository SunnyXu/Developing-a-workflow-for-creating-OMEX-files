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

r = te.loads("Jena2688.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#te.saveToFile("promoted.xml", SBML)



r = te.loads("Jena2688.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
sedml = libsedml.readSedMLFromFile("../old_SEDML/Jena5258.sedml")

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)

plot = sedml.getOutput(0)

plot.setName("Jena/2688(H1N1)")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Days after infection")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(22)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("All Variables")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(7)

curve = plot.getCurve(0)
curve.setStyle("dashed_blue")
curve.setName("P")
curve = plot.getCurve(1)
curve.setStyle("dashed_black")
curve.setName("D")
curve = plot.getCurve(2)
curve.setStyle("dashed_green")
curve.setName("I")
curve = plot.getCurve(3)
curve.setStyle("dashed_red")
curve.setName("S")


style1 = sedml.createStyle()
line1 = style1.createLineStyle()
line1.setColor("0000ff") #blue
line1.setType(libsedml.SEDML_LINETYPE_DASH)
marker1 = style1.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style1.createFillStyle()
#fill.setColor("#000000FF")
style1.setId("dashed_blue")

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
line1.setColor("00ff00") #green
line1.setType(libsedml.SEDML_LINETYPE_DASH)
marker1 = style1.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style1.createFillStyle()
#fill.setColor("#000000FF")
style1.setId("dashed_green")

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
mod1.setSource("Jena2688.xml")


sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("Jena2688.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["Jena2688.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000000712-3-Jena2688.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

# print(sed)
