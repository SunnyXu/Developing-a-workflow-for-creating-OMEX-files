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

r = te.loads("Wang2016_1.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
te.saveToFile("promoted.xml", SBML)


r = te.loads("Wang2016_1.xml")
SBML = r.getParamPromotedSBML(r.getSBML())

sedml = libsedml.readSedMLFromFile("../old_SEDML/Wang2016_1.sedml")

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

#removeModelRefsFromDataGenerators(sedml)

plot = sedml.getOutput(0)

plot.setName("Figure 6")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("t")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(2500)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Solution")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(0.45)

curve = plot.getCurve(0)
curve.setStyle("solid_red")
curve.setName("M")
curve = plot.getCurve(1)
curve.setStyle("solid_blue")
curve.setName("N")
curve = plot.getCurve(2)
curve.setStyle("solid_orange")
curve.setName("S")
curve = plot.getCurve(3)
curve.setStyle("solid_green")
curve.setName("T")



style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("ff0000") #red
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_red")

style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("0000ff") #blue
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_blue")

style2 = sedml.createStyle()
line2 = style2.createLineStyle()
line2.setColor("FF7F50") #coral/orange
line2.setType(libsedml.SEDML_LINETYPE_SOLID)
marker2 = style2.createMarkerStyle()
marker2.setType(libsedml.SEDML_MARKERTYPE_NONE)
style2.setId("solid_orange")

style2 = sedml.createStyle()
line2 = style2.createLineStyle()
line2.setColor("00ff00") #green
line2.setType(libsedml.SEDML_LINETYPE_SOLID)
marker2 = style2.createMarkerStyle()
marker2.setType(libsedml.SEDML_MARKERTYPE_NONE)
style2.setId("solid_green")


#Now fix the fact that tellurium's handling of local parameters is off:
mod1 = sedml.getModel(0)
mod1.setSource("Wang2016_1.xml")


sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("Wang2016_1.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["Wang2016_1.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000000780-Fig6.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

# print(sed)
