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

r = te.loads("Hou2020.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#te.saveToFile("promoted.xml", SBML)

#SEDML:
# p_str = """
#     kholodenko = model "promoted.xml"
#     kholodenko_b = model kholodenko with J0_n = 2, \
#         J0_Ki= 18, \
#         J0_K1= 50, \ 
#         J1_KK2= 40, \ 
#         J2_KK3=100, \ 
#         J3_KK4=100, \
#         J4_KK5=100, \ 
#         J5_KK6=100, \ 
#         J6_KK7=100, \ 
#         J7_KK8=100, \ 
#         J8_KK9=100, \ 
#         J9_KK10=100, \ 
#         J8_V9=1.25, \ 
#         J9_V10=1.25
    
#     sim0 = simulate uniform(0, 9000, 1000)
#     sim1 = simulate uniform(0, 12000, 1000)
#     task_fig2a = run sim0 on kholodenko
#     task_fig2b = run sim1 on kholodenko_b
#     plot "Figure 2A" task_fig2a.time/60 vs task_fig2a.MAPK_PP, task_fig2a.MAPK
#     plot "Figure 2B" task_fig2b.time/60 vs task_fig2b.MAPK_PP, task_fig2b.MAPK
#     report "Figure 2A" task_fig2a.time/60 vs task_fig2a.MAPK_PP, task_fig2a.MAPK
#     report "Figure 2B" task_fig2b.time/60 vs task_fig2b.MAPK_PP, task_fig2b.MAPK
# """
#SEDML:
p_str = """
// Created by libphrasedml v1.3.0
// Models
model1 = model "BIOMD0000000618_url.xml"
model2 = model "#model1" with c_T = 92.5, c_T = 92.5

// Simulations
sim1 = simulate uniform(0, 150, 1000)

// Tasks
task1 = run sim1 on model1
task2 = run sim1 on model2

// Outputs
plot "Figure 4a" task1.time vs task1.soluble_obs
plot "Figure 4b" task1.time vs task1.insoluble_obs
plot "Figure 4c" task1.time vs task2.soluble_obs
plot "Figure 4d" task1.time vs task2.insoluble_obs
report "Auto-generated report for task1, including all symbols in SBML with mathematical meaning, both constant and variable." task1.time, task1.soluble_obs, task1.insoluble_obs, task1.M, task1.N, task1.A7, task1.A8, task1.A9, task1.A10, task1.A11, task1.A12, task1.A13, task1.A14, task1.A15, task1.A16, task1.A17, task1.A18, task1.A19, task1.A20, task1.A21, task1.A22, task1.A23, task1.A24, task1.A25, task1.A26, task1.A27, task1.A28, task1.A29, task1.A30, task1.A31, task1.A32, task1.A33, task1.A34, task1.A35, task1.A36, task1.A37, task1.A38, task1.A39, task1.A40, task1.A41, task1.A42, task1.A43, task1.A44, task1.A45, task1.A46, task1.A47, task1.A48, task1.A49, task1.A50, task1.A51, task1.A52, task1.A53, task1.A54, task1.P, task1.c_T, task1.s_T, task1.e_T, task1.k_n, task1.k_sol, task1.k_insol, task1.n_n, task1.blocking, task1.soluble, task1.insoluble, task1.R_T, task1.a_T, task1.I_net, task1.C1
"""

r = te.loads("Hou2020.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#phrasedml.setReferencedSBML("BIOMD0000000010_url.xml", SBML)
#sed = phrasedml.convertString(p_str)
# if sed is None:
#     print(phrasedml.getLastError())

#sedml = libsedml.readSedMLFromString(sed)
sedml = libsedml.readSedMLFromFile("../old_SEDML/Hou2020.sedml")

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)

plot = sedml.getOutput(0)
plot.setName("Figure 2 (A)")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Months")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(7)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Quantity")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(12000000)

curve = plot.getCurve(0)
curve.setName("susceptible individuals")
curve.setStyle("solid")

plot = sedml.getOutput(1)
plot.setName("Figure 2 (B)")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Months")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(7)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Quantity")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(4200000)

curve = plot.getCurve(0)
curve.setName("exposed individuals")
curve.setStyle("solid")

plot = sedml.getOutput(2)
plot.setName("Figure 2 (C)")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Months")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(7)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Quantity")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(6000000)

curve = plot.getCurve(0)
curve.setName("infected individuals")
curve.setStyle("solid")

plot = sedml.getOutput(3)
plot.setName("Figure 2 (D)")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Months")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(7)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Quantity")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(12000000)

curve = plot.getCurve(0)
curve.setName("removed individuals")
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
mod1.setSource("Hou2020.xml")
# mod2 = sedml.getModel(1)
# for ch in range(mod2.getNumChanges()):
#     change = mod2.getChange(ch)
#     change.setTarget(globalToLocalParameter(change.getTarget()))
# mod2.setSource("#kholodenko")

sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("Hou2020.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["Hou2020.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000000970.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

print(sed)
