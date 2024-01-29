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

r = te.loads("BIOMD0000000010_url.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
te.saveToFile("promoted.xml", SBML)

#SEDML:
p_str = """
    kholodenko = model "promoted.xml"
    kholodenko_b = model kholodenko with J0_n = 2, \
        J0_Ki= 18, \
        J0_K1= 50, \ 
        J1_KK2= 40, \ 
        J2_KK3=100, \ 
        J3_KK4=100, \
        J4_KK5=100, \ 
        J5_KK6=100, \ 
        J6_KK7=100, \ 
        J7_KK8=100, \ 
        J8_KK9=100, \ 
        J9_KK10=100, \ 
        J8_V9=1.25, \ 
        J9_V10=1.25
    
    sim0 = simulate uniform(0, 9000, 1000)
    sim1 = simulate uniform(0, 12000, 1000)
    task_fig2a = run sim0 on kholodenko
    task_fig2b = run sim1 on kholodenko_b
    plot "Figure 2A" task_fig2a.time/60 vs task_fig2a.MAPK_PP, task_fig2a.MAPK
    plot "Figure 2B" task_fig2b.time/60 vs task_fig2b.MAPK_PP, task_fig2b.MAPK
    report "Figure 2A" task_fig2a.time/60 vs task_fig2a.MAPK_PP, task_fig2a.MAPK
    report "Figure 2B" task_fig2b.time/60 vs task_fig2b.MAPK_PP, task_fig2b.MAPK
"""

r = te.loads("BIOMD0000000010_url.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#phrasedml.setReferencedSBML("BIOMD0000000010_url.xml", SBML)
sed = phrasedml.convertString(p_str)
if sed is None:
    print(phrasedml.getLastError())

sedml = libsedml.readSedMLFromString(sed)

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)

plot = sedml.getOutput(0)

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time (min)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(150)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("MAPK concentrations (nM)")
yaxis.setGrid(False)

curve = plot.getCurve(0)
# curve.setName("E (open)")
curve.setStyle("solid")
curve.setName("MAPK_PP")
curve = plot.getCurve(1)
# curve.setName("P (open)")
curve.setStyle("dashed")
curve.setName("MAPK")


plot = sedml.getOutput(1)

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Time (min)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(200)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("MAPK concentrations (nM)")
yaxis.setGrid(False)

curve = plot.getCurve(0)
# curve.setName("E (open)")
curve.setStyle("solid")
curve.setName("MAPK_PP")
curve = plot.getCurve(1)
# curve.setName("P (open)")
curve.setStyle("dashed")
curve.setName("MAPK")


style = sedml.createStyle()
line = style.createLineStyle()
#line.setColor("1f77b4")
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
mod1.setSource("BIOMD0000000010_url.xml")
mod2 = sedml.getModel(1)
for ch in range(mod2.getNumChanges()):
    change = mod2.getChange(ch)
    change.setTarget(globalToLocalParameter(change.getTarget()))
mod2.setSource("#kholodenko")

sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("BIOMD0000000010_url.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["BIOMD0000000010_url.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000000010.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

print(sed)
