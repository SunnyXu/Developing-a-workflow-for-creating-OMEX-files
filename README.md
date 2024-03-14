# Curating models from Biomodels: Developing a workflow for creating OMEX files

## Introduction

The reproducibility of computational biology models can be greatly facilitated by widely adopted standards and public repositories. We examined 50 models from the BioModels Database and attempted to validate the original curation and correct some of them if necessary. For each model, we reproduced these published results using Tellurium. Once reproduced we manually created a new set of files, with the model information stored by the Systems Biology Markup Language (SBML), and simulation instructions stored by the Simulation Experiment Description Markup Language (SED-ML), and everything included in an Open Modeling EXchange (OMEX) file, which could be used with a variety of simulators to reproduce the same results. On the one hand, the validation procedure of 50 models developed a manual workflow that we would use to build an automatic platform to help users more easily curate and verify models in the future. On the other hand, these exercises allowed us to find the limitations and possible enhancement of the current curation and tooling to verify and curate models.

## Citing

If you use any of the codes, please cite the GitHub website (https://github.com/sys-bio/Developing-a-workflow-for-creating-OMEX-files).
