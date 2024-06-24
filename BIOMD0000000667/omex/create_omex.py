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

r = te.loads("BIOMD0000000667_url.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#te.saveToFile("promoted.xml", SBML)



r = te.loads("BIOMD0000000667_url.xml")
SBML = r.getParamPromotedSBML(r.getSBML())


#sedml = libsedml.readSedMLFromString(sed)
sedml = libsedml.readSedMLFromFile("../old_SEDML/MODEL0848279215.sedml")

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)

plot = sedml.getOutput(0)

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time(min)")
xaxis.setGrid(False)
xaxis.setMin(0)
#xaxis.setMax(6000)
xaxis.setMax(6000/60)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("ERK-PP [molecules/cell]")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(15000000)

curve = plot.getCurve(0)
curve.setName("[ERK-PP]t")
curve.setStyle("solid")



style = sedml.createStyle()
line = style.createLineStyle()
#line.setColor("1f77b4")
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid")



#Now fix the fact that tellurium's handling of local parameters is off:
mod1 = sedml.getModel(0)
mod1.setSource("BIOMD0000000667_url.xml")


sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("BIOMD0000000667.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["BIOMD0000000667.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000000667.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

print(sed)
