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

r = te.loads("Kurlovics2021.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#te.saveToFile("promoted.xml", SBML)


r = te.loads("Kurlovics2021.xml")
SBML = r.getParamPromotedSBML(r.getSBML())


sedml = libsedml.readSedMLFromFile("../old_SEDML/Kurlovics2021.sedml")

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)

plot = sedml.getOutput(0)
plot.setName("Figure 7A Metformin concentration dynamics")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time, h")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(40)


yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Metformin concentration, ng/mL")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(650)

curve = plot.getCurve(0)
curve.setName("Plasma")
curve.setStyle("solid_red")


curve = plot.getCurve(1)
curve.setName("RBC")
curve.setStyle("solid_green")

plot = sedml.getOutput(1)
plot.setName("Figure 7B Reaction fluxes")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time, h")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(40)


yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Metformin flux, ng/h")
yaxis.setGrid(False)
yaxis.setMin(-10000)
yaxis.setMax(65000)

curve = plot.getCurve(2)
curve.setName("Summary flux")
curve.setStyle("solid_red")

curve = plot.getCurve(1)
curve.setName("From RBC")
curve.setStyle("solid_green")

curve = plot.getCurve(0)
curve.setName("To RBC")
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
line.setColor("00ff00") #green
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_green")


style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("0000ff") #blue
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_blue")





#Now fix the fact that tellurium's handling of local parameters is off:
mod1 = sedml.getModel(0)
mod1.setSource("Kurlovics2021.xml")


sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("Kurlovics2021.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["Kurlovics2021.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000001026.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

#print(sed)
