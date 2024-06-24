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

r = te.loads("BIOMD0000000618_url.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#te.saveToFile("promoted.xml", SBML)


r = te.loads("BIOMD0000000618_url.xml")
SBML = r.getParamPromotedSBML(r.getSBML())

sedml = libsedml.readSedMLFromFile("../old_SEDML/BIOMD0000000618.sedml")

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)

plot = sedml.getOutput(0)


xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time(wks)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(150/6+5)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Brain $Ab42$ (ng/mg protein)")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(1200)

curve = plot.getCurve(0)
curve.setName("butter-solubble-1")
curve.setStyle("dashed")

plot = sedml.getOutput(1)

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time(wks)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(150/6+5)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Brain Ab42 (ng/mg protein)")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(12000)

curve = plot.getCurve(0)
curve.setName("guanidine-solubble-1")
curve.setStyle("dashed")

plot = sedml.getOutput(2)

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time(wks)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(150/6+5)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Brain b42 (ng/mg protein)")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(1200)

curve = plot.getCurve(0)
curve.setName("butter-solubble-2")
curve.setStyle("dashed")

plot = sedml.getOutput(3)

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time(wks)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(150/6+5)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Brain Ab42 (ng/mg protein)")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(12000)

curve = plot.getCurve(0)
curve.setName("guanidine-solubble-2")
curve.setStyle("dashed")


style = sedml.createStyle()
line = style.createLineStyle()
#line.setColor("1f77b4")
line.setType(libsedml.SEDML_LINETYPE_DASH)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("dashed")



#Now fix the fact that tellurium's handling of local parameters is off:
mod1 = sedml.getModel(0)
mod1.setSource("BIOMD0000000618_url.xml")


sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("BIOMD0000000618.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["BIOMD0000000618.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000000618.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

print(sed)
