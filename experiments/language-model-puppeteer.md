---
title: Language Model Puppeteer
slug: language-model-puppeteer
status: In Progress
date: 2026-10
researchers: 2
description: Can internal activation interventions move one language model between answering confidently and abstaining when uncertain, without expressing that policy in the prompt?
tags:
  - Activation Steering
  - LLMs
  - Interpretability
technical:
  Model: Qwen2.5-0.5B-Instruct
  Layers: 24
  Hidden size: 896
  Method: Activation steering
---

## Question

Can internal activation interventions move the same language model between two behavioral policies—answering confidently and abstaining when uncertain—without communicating the policy through the prompt?

## Hypothesis

Answering and abstaining may correspond to distinguishable internal representations that can be measured across layers. Whether a useful steering direction exists remains an open question.

## Setup

- **Model:** Qwen2.5-0.5B-Instruct
- **Architecture:** 24 transformer layers, hidden size 896
- **Dataset:** To be specified as the evaluation set is finalized
- **Environment:** To be documented with the experiment run configuration
- **Parameters:** To be recorded alongside each run

## Method

We will extract hidden representations for answer and abstain behavior, compare them layer by layer, and identify potentially useful representation differences. Candidate steering directions will then be constructed and tested. Comparisons will include the unmodified model, prompt-based policy instructions, and activation steering.

## Results

Results will be added as the experiment progresses. No steering result has been established yet.

## Observations

Observations will be recorded as runs are completed.

## Failures / Limitations

The evaluation set, run environment, and parameters are not yet documented. These details are needed to interpret and reproduce future measurements.

## Current conclusion

The experiment is in progress. There is not yet evidence to conclude that activation steering moves the model between these policies.

## Next

Finalize the evaluation set and run configuration, extract answer and abstain representations, then compare layer-wise differences before testing candidate steering directions.
