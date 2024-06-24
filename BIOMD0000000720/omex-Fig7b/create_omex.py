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

r = te.loads("Yan2012.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#te.saveToFile("promoted.xml", SBML)


r = te.loads("Yan2012.xml")
SBML = r.getParamPromotedSBML(r.getSBML())

sedml = libsedml.readSedMLFromFile("../old_SEDML/Yan2012.sedml")

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)


plot = sedml.getOutput(0)
plot.setName("Figure 7b")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("time(hr)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(200)


yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Concentration($\mu$m)")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(1.7)

curve = plot.getCurve(0)
curve.setName("CycE-Cdk2")
curve.setStyle("solid_green")

curve = plot.getCurve(1)
curve.setName("E2F")
curve.setStyle("solid_red")

curve = plot.getCurve(2)
curve.setName("MiR449")
curve.setStyle("solid_black")


style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("ff0000") #red
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_red")


style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("00ff00") #green
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_green")


style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("000000") #black
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_black")





#Now fix the fact that tellurium's handling of local parameters is off:
mod1 = sedml.getModel(0)
mod1.setSource("Yan2012.xml")


sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("Yan2012-Fig7b.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["Yan2012-Fig7b.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000000720-Fig7b.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

#print(sed)
