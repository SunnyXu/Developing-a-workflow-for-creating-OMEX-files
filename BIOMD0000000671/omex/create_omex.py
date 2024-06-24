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

r = te.loads("BIOMD0000000671_url.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#te.saveToFile("promoted.xml", SBML)


r = te.loads("BIOMD0000000671_url.xml")
SBML = r.getParamPromotedSBML(r.getSBML())

sedml = libsedml.readSedMLFromFile("../old_SEDML/MODEL1708250001.sedml")

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

#removeModelRefsFromDataGenerators(sedml)

plot = sedml.getOutput(0)

plot.setName("Figure 3")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time (d)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(120)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Tumor Size (mm$^3$)")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(4500)


curve = plot.getCurve(0)
curve.setStyle("solid_green")
curve.setName("Bertalanffy")
curve = plot.getCurve(1)
curve.setStyle("solid_black")
curve.setName("Exponential")
curve = plot.getCurve(2)
curve.setStyle("solid_pink")
curve.setName("Gompertz")
curve = plot.getCurve(3)
curve.setStyle("solid_light_blue")
curve.setName("Linear")
curve = plot.getCurve(4)
curve.setStyle("solid_yellow")
curve.setName("Logistic")
curve = plot.getCurve(5)
curve.setStyle("solid_blue")
curve.setName("Mendelsohn")
curve = plot.getCurve(6)
curve.setStyle("solid_red")
curve.setName("Surface")

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

style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("00ff00") #green
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_green")

style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("33FFF9") #light blue
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_light_blue")


style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("000000") #black
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_black")

style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("ffff00") #yellow
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_yellow")

style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("FF1493") #deep pink
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_pink")



#Now fix the fact that tellurium's handling of local parameters is off:
mod1 = sedml.getModel(0)
mod1.setSource("BIOMD0000000671_url.xml")


sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("MODEL1708250001-Fig3.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["MODEL1708250001-Fig3.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000000671-Fig3.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

# print(sed)
