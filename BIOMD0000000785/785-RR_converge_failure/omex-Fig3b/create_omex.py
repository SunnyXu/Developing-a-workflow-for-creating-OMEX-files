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

r = te.loads("Sotolongo-Costa2003.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#te.saveToFile("promoted.xml", SBML)

#antimony:
antimony_str = """
// Created by libAntimony v2.13.2
function Function_for_LSC_Differentiation(p_30, v_30, L)
  (1 - p_30)*v_30*L;
end

Function_for_LSC_Differentiation is "Function_for_LSC_Differentiation"

function Function_for_PC_Differentiation(p_2_D, v_2_D, A)
  (1 - p_2_D)*v_2_D*A;
end

Function_for_PC_Differentiation is "Function_for_PC_Differentiation"

function Function_for_HSC_Self_Renewal(p_1_D, K_1, Z_1, v_1_D, S)
  p_1_D*(K_1 - Z_1)*v_1_D*S;
end

Function_for_HSC_Self_Renewal is "Function_for_HSC_Self_Renewal"

function Function_for_HSC_Differentiation(p_1_D, v_1_D, S)
  (1 - p_1_D)*v_1_D*S;
end

Function_for_HSC_Differentiation is "Function_for_HSC_Differentiation"

function Function_for_PC_Self_Renewal(p_2_D, K_2, Z_2, v_2_D, A)
  p_2_D*(K_2 - Z_2)*v_2_D*A;
end

Function_for_PC_Self_Renewal is "Function_for_PC_Self_Renewal"

function Function_for_LSC_Self_Renewal(p_30, K_2, Z_2, v_30, L)
  p_30*(K_2 - Z_2)*v_30*L;
end

Function_for_LSC_Self_Renewal is "Function_for_LSC_Self_Renewal"


model *Jiao2018___Feedback_regulation_in_a_stem_cell_model_with_acute_myeloid_leukaemia()

  // Compartments and Species:
  compartment compartment_;
  species S_HSC in compartment_, A_PC in compartment_, D_TDSC in compartment_;
  species L_LSC in compartment_, T_TDLC in compartment_;

  // Assignment Rules:
  p_1_D := p_10/(1 + g_1*D_TDSC^n);
  p_2_D := p_20/(1 + g_2*D_TDSC^n);
  v_1_D := v_10/(1 + h_1*D_TDSC^n);
  v_2_D := v_20/(1 + h_2*D_TDSC^n);
  Z_1 := S_HSC;
  Z_2 := A_PC + L_LSC;

  // Reactions:
  HSC_Self_Renewal:  => S_HSC; compartment_*Function_for_HSC_Self_Renewal(p_1_D, K_1, Z_1, v_1_D, S_HSC);
  HSC_Differentiation: S_HSC => 2 A_PC; compartment_*Function_for_HSC_Differentiation(p_1_D, v_1_D, S_HSC);
  PC_Self_Renewal:  => A_PC; compartment_*Function_for_PC_Self_Renewal(p_2_D, K_2, Z_2, v_2_D, A_PC);
  PC_Differentiation: A_PC => 2 D_TDSC; compartment_*Function_for_PC_Differentiation(p_2_D, v_2_D, A_PC);
  TDC_Apoptosis: D_TDSC => ; compartment_*d_1*D_TDSC;
  LSC_Self_Renewal:  => L_LSC; compartment_*Function_for_LSC_Self_Renewal(p_30, K_2, Z_2, v_30, L_LSC);
  LSC_Differentiation: L_LSC => 2 T_TDLC; compartment_*Function_for_LSC_Differentiation(p_30, v_30, L_LSC);
  TDL_Apoptosis: T_TDLC => ; compartment_*d_2*T_TDLC;

  // Species initializations:
  S_HSC = 10;
  A_PC = 0;
  D_TDSC = 0;
  L_LSC = 10;
  T_TDLC = 0;

  // Compartment initializations:
  compartment_ = 1;

  // Variable initializations:
  p_10 = 0.45;
  p_20 = 0.68;
  p_30 = 0.8;
  v_10 = 0.5;
  v_20 = 0.72;
  v_30 = 0.7;
  d_1 = 0.275;
  d_2 = 0.3;
  g_1 = 0.03;
  g_2 = 0.025;
  h_1 = 0.2;
  h_2 = 0.11;
  m = 1;
  n = 1;
  K_1 = 1;
  K_2 = 1;

  // Other declarations:
  var p_1_D, p_2_D, v_1_D, v_2_D, Z_1, Z_2;
  const compartment_, p_10, p_20, p_30, v_10, v_20, v_30, d_1, d_2, g_1, g_2;
  const h_1, h_2, m, n, K_1, K_2;

  // Unit definitions:
  unit substance = item;

  // Display Names:
  compartment_ is "compartment";

  // CV terms:
  compartment_ identity "http://identifiers.org/ncit/C12431"
  S_HSC identity "http://identifiers.org/ncit/C12551"
  A_PC hypernym "http://identifiers.org/ncit/C12662"
  D_TDSC hypernym "http://identifiers.org/ncit/C12551"
  D_TDSC property "http://identifiers.org/efo/EFO:0002954"
  L_LSC identity "http://identifiers.org/ncit/C41069"
  T_TDLC property "http://identifiers.org/efo/EFO:0002954"
  T_TDLC propertyBearer "http://identifiers.org/ncit/C41069"
  HSC_Self_Renewal hypernym "http://identifiers.org/ncit/C18081"
  HSC_Differentiation hypernym "http://identifiers.org/ncit/C19045"
  PC_Self_Renewal hypernym "http://identifiers.org/ncit/C18081"
  PC_Differentiation hypernym "http://identifiers.org/ncit/C19045"
  TDC_Apoptosis identity "http://identifiers.org/ncit/C17557"
  LSC_Self_Renewal hypernym "http://identifiers.org/ncit/C18081"
  LSC_Differentiation hypernym "http://identifiers.org/ncit/C19045"
  TDL_Apoptosis identity "http://identifiers.org/ncit/C17557"
end

Jiao2018___Feedback_regulation_in_a_stem_cell_model_with_acute_myeloid_leukaemia is "Jiao2018 - Feedback regulation in a stem cell model with acute myeloid leukaemia"

Jiao2018___Feedback_regulation_in_a_stem_cell_model_with_acute_myeloid_leukaemia description "http://identifiers.org/pubmed/29745850"
Jiao2018___Feedback_regulation_in_a_stem_cell_model_with_acute_myeloid_leukaemia model_entity_is "http://identifiers.org/biomodels.db/MODEL1912170002",
                                                                                                 "http://identifiers.org/biomodels.db/BIOMD0000000898"
Jiao2018___Feedback_regulation_in_a_stem_cell_model_with_acute_myeloid_leukaemia property "http://identifiers.org/ncit/C82652"
Jiao2018___Feedback_regulation_in_a_stem_cell_model_with_acute_myeloid_leukaemia property "http://identifiers.org/ncit/C3171"
Jiao2018___Feedback_regulation_in_a_stem_cell_model_with_acute_myeloid_leukaemia property "http://identifiers.org/ncit/C12551"
Jiao2018___Feedback_regulation_in_a_stem_cell_model_with_acute_myeloid_leukaemia property "http://identifiers.org/mamo/MAMO_0000046"
Jiao2018___Feedback_regulation_in_a_stem_cell_model_with_acute_myeloid_leukaemia taxon "http://identifiers.org/taxonomy/9606"
"""

#SEDML:
p_str = """
// Created by libphrasedml v1.3.0
// Models
model = model "Jiao2018.xml"

// Simulations
sim1 = simulate uniform(0, 200, 1000)
sim1.algorithm = kisao.0
sim1.algorithm.relative_tolerance = 1e-06
sim1.algorithm.absolute_tolerance = 1e-12
sim1.algorithm.kisao.216 = 0
sim1.algorithm.maximum_num_steps = 10000

// Tasks
task1 = run sim1 on model

// Outputs
plot "Figure 5" time vs A_PC, D_TDSC, L_LSC, S_HSC, T_TDLC
report "Auto-generated report for task1, including all symbols in SBML with mathematical meaning, both constant and variable." time, A_PC, D_TDSC, L_LSC, S_HSC, T_TDLC, p_10, p_20, p_30, v_10, v_20, v_30, d_1, d_2, g_1, g_2, h_1, h_2, m, n, K_1, K_2, p_1_D, p_2_D, v_1_D, v_2_D, Z_1, Z_2, compartment, HSC_Self_Renewal, HSC_Differentiation, PC_Self_Renewal, PC_Differentiation, TDC_Apoptosis, LSC_Self_Renewal, LSC_Differentiation, TDL_Apoptosis
"""

r = te.loads("Sotolongo-Costa2003.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
#phrasedml.setReferencedSBML("BIOMD0000000010_url.xml", SBML)
#sed = phrasedml.convertString(p_str)
# if sed is None:
#     print(phrasedml.getLastError())

#sedml = libsedml.readSedMLFromString(sed)
sedml = libsedml.readSedMLFromFile("D:/summer-2023/4-pick_models/22-785/file/Sotolongo-Costa2003.sedml")

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)


plot = sedml.getOutput(0)
plot.setName("Figure 3b")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("t")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(180)


yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("X")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(2.5)

curve = plot.getCurve(0)
curve.setName("Evolution of malignant cells on time without treatment")
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
line.setColor("0000FF") #blue
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_blue")


style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("FFA500") #orange
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_orange")





#Now fix the fact that tellurium's handling of local parameters is off:
mod1 = sedml.getModel(0)
mod1.setSource("Sotolongo-Costa2003.xml")
# mod2 = sedml.getModel(1)
# for ch in range(mod2.getNumChanges()):
#     change = mod2.getChange(ch)
#     change.setTarget(globalToLocalParameter(change.getTarget()))
# mod2.setSource("#kholodenko")

sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("Sotolongo-Costa2003-Fig3b.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["Sotolongo-Costa2003-Fig3b.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "Sotolongo-Costa2003-Fig3b_curated.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

#print(sed)
