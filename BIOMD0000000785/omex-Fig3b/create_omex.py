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

r = te.loads("Sotolongo-Costa2003.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#te.saveToFile("promoted.xml", SBML)


r = te.loads("Sotolongo-Costa2003.xml")
SBML = r.getParamPromotedSBML(r.getSBML())

sedml = libsedml.readSedMLFromFile("../old_SEDML/Sotolongo-Costa2003.sedml")

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)


plot = sedml.getOutput(0)
plot.setName("Figure 3b")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("t")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(180)


yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("X")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(2.5)

curve = plot.getCurve(0)
curve.setName("Evolution of malignant cells on time without treatment")
curve.setStyle("solid_blue")


style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("ff0000") #red
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_red")


style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("0000FF") #blue
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_blue")


style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("FFA500") #orange
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_orange")





#Now fix the fact that tellurium's handling of local parameters is off:
mod1 = sedml.getModel(0)
mod1.setSource("Sotolongo-Costa2003.xml")


sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("Sotolongo-Costa2003-Fig3b.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["Sotolongo-Costa2003-Fig3b.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000000785-Fig3b.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

#print(sed)
