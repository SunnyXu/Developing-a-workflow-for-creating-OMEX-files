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

r = te.loads("BIOMD0000000552_url.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#te.saveToFile("promoted.xml", SBML)


r = te.loads("BIOMD0000000552_url.xml")
SBML = r.getParamPromotedSBML(r.getSBML())

sed = phrasedml.convertString("""
// Created by libphrasedml v1.3.0
// Models
mod_k2_33 = model "BIOMD0000000552_url.xml"
mod_k2_28 = model mod_k2_33 with k2=0.28
mod_k2_26 = model mod_k2_33 with k2=0.26
mod_k2_24 = model mod_k2_33 with k2=0.24
mod_k2_22 = model mod_k2_33 with k2=0.22

// Simulations
sim1 = simulate uniform(0, 150, 1000)
sim1.algorithm = kisao.360
sim1.algorithm.relative_tolerance = 1e-06
sim1.algorithm.absolute_tolerance = 1e-12
sim1.algorithm.216 = 0
sim1.algorithm.maximum_num_steps = 10000

// Tasks
t33 = run sim1 on mod_k2_33
t28 = run sim1 on mod_k2_28
t26 = run sim1 on mod_k2_26
t24 = run sim1 on mod_k2_24
t22 = run sim1 on mod_k2_22

// Outputs
plot "Figure 1" t33.time vs t33.aRel, t28.aRel, t26.aRel, t24.aRel, t22.aRel
report "Auto-generated report for task1, including all symbols in SBML with mathematical meaning, both constant and variable." t33.time, t33.aRel, t33.a, t33.b, t33.k1, t33.k2, t33.k3, t33.k4, t33.Brain, t33.Loss_of_intracellular_choline, t33.Abeta_formation_from_APP, t33.Effect_of_extracellular_ACh, t33.Decrease_in_the_extracellular_concentration_of_beta_amyloid, t28.aRel, t28.a, t28.b, t28.k1, t28.k2, t28.k3, t28.k4, t28.Brain, t28.Loss_of_intracellular_choline, t28.Abeta_formation_from_APP, t28.Effect_of_extracellular_ACh, t28.Decrease_in_the_extracellular_concentration_of_beta_amyloid, t26.aRel, t26.a, t26.b, t26.k1, t26.k2, t26.k3, t26.k4, t26.Brain, t26.Loss_of_intracellular_choline, t26.Abeta_formation_from_APP, t26.Effect_of_extracellular_ACh, t26.Decrease_in_the_extracellular_concentration_of_beta_amyloid, t24.aRel, t24.a, t24.b, t24.k1, t24.k2, t24.k3, t24.k4, t24.Brain, t24.Loss_of_intracellular_choline, t24.Abeta_formation_from_APP, t24.Effect_of_extracellular_ACh, t24.Decrease_in_the_extracellular_concentration_of_beta_amyloid, t22.aRel, t22.a, t22.b, t22.k1, t22.k2, t22.k3, t22.k4, t22.Brain, t22.Loss_of_intracellular_choline, t22.Abeta_formation_from_APP, t22.Effect_of_extracellular_ACh, t22.Decrease_in_the_extracellular_concentration_of_beta_amyloid
""")

sedml = libsedml.readSedMLFromString(sed)

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)

plot = sedml.getOutput(0)

plot.setName("Figure 1 Acetlcholine")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("Age (Years)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(150)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Relative Concentration of Acetylcholine")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(1.)


curve = plot.getCurve(0)
curve.setName("$k_2=0.33$")

curve = plot.getCurve(1)
curve.setName("$k_2=0.28$")

curve = plot.getCurve(2)
curve.setName("$k_2=0.26$")

curve = plot.getCurve(3)
curve.setName("$k_2=0.24$")

curve = plot.getCurve(4)
curve.setName("$k_2=0.22$")





#Now fix the fact that tellurium's handling of local parameters is off:
mod1 = sedml.getModel(0)
mod1.setSource("BIOMD0000000552_url.xml")


sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("Ehrenstein2000.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["Ehrenstein2000.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000000552.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

# print(sed)
