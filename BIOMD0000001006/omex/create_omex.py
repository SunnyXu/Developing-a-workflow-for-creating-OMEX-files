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

r = te.loads("Ciliberto2005.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
te.saveToFile("promoted.xml", SBML)



r = te.loads("Ciliberto2005.xml")
SBML = r.getParamPromotedSBML(r.getSBML())

sedml = libsedml.readSedMLFromFile("../old_SEDML/Ciliberto2005.sedml")


sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)

plot = sedml.getOutput(0)
plot.setName("Figure 2A")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time (min)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(1200)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
#yaxis.setName("MAPK concentrations (nM)")
yaxis.setGrid(False)
yaxis.setMax(1.6)

curve = plot.getCurve(0)
curve.setStyle("dashed")
curve.setName("MDM2")
curve = plot.getCurve(1)
# curve.setName("P (open)")
curve.setStyle("solid")
curve.setName("p53")


plot = sedml.getOutput(1)
plot.setName("Figure 2B")
xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time (min)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(1200)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
#yaxis.setName("MAPK concentrations (nM)")
yaxis.setGrid(False)

curve = plot.getCurve(0)
# curve.setName("E (open)")
curve.setStyle("solid")
curve.setName("MDM2")
curve = plot.getCurve(1)
# curve.setName("P (open)")
curve.setStyle("dashed")
curve.setName("MDM2P")

plot = sedml.getOutput(2)
plot.setName("Figure 2C-1")
xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time (min)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(1200)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
#yaxis.setName("MAPK concentrations (nM)")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(2)

curve = plot.getCurve(0)
# curve.setName("E (open)")
curve.setStyle("solid")
curve.setName("DNA")


plot = sedml.getOutput(3)
plot.setName("Figure 2C-2")
xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time (min)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(1200)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
#yaxis.setName("MAPK concentrations (nM)")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(0.025)

curve = plot.getCurve(0)
# curve.setName("E (open)")
curve.setStyle("dashed")
curve.setName("$k_{d2}$")


style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("1f77b4")
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid")

style2 = style.clone()
style2.getLineStyle().setType(libsedml.SEDML_LINETYPE_DASH)
style2.setId("dashed")
sedml.addStyle(style2)

#Now fix the fact that tellurium's handling of local parameters is off:
mod1 = sedml.getModel(0)
mod1.setSource("Ciliberto2005.xml")


sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("Ciliberto2005.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["Ciliberto2005.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000001006.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

#print(sed)
