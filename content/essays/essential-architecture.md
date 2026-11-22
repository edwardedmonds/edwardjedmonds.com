---
title: "Essential Architecture"
seo_title: "Essential Architecture: Structure, Fuel, and Membranes"
subtitle: "Structure, fuel, and the maintenance of biological membranes"
date: 2025-12-22
lastmod: 2026-11-22
description: "How polyunsaturated fatty acids serve structural and metabolic roles—from membrane deformability and the Lands cycle to oxidation and thyroid signaling."
tags: ["lipids", "essential fatty acids", "metabolism"]
series: "efa"
series_order: 3
toc: true
math: false
aliases: ["/essential-architecture.html"]
draft: false
---

## Building Materials and Fuel

[Thyroid Hormone as the Guardian of Form]({{< relref "essays/thyroid-hormone-guardian-of-form" >}}) separated two things that are easily run together: an intact structural lipid doing its work in a membrane, and the products that form when that lipid is oxidatively damaged. A peroxidation product acting on an enzyme describes degradation, and it says little about what the undamaged phospholipid contributes. This essay asks the question that follows. If polyunsaturated fatty acids (PUFAs) are structural materials, how much of what an organism eats is actually used that way, how are those materials kept in place, and what happens when supply, remodeling, and protection fall out of step?

Building materials and fuel are not the same thing.

The distinction is a spectrum of primary roles, not a pair of boxes. Glucose and saturated and monounsaturated fats carry most of the bulk ATP load, and essential amino acids and essential fatty acids are the substrates tissues cannot make for themselves. But saturated chains are also structural: most membrane glycerophospholipids carry a saturated or monounsaturated chain at the *sn*-1 position, and cholesterol is a structural component of the plasma membrane {{< cite "harayama2018" >}}. Even the essential fatty acids are not purely structural, as the next section shows. The useful question is therefore what a given molecule is mainly for in a given tissue, and what is lost when it is diverted from that role.

## Two Kinds of Polyunsaturated Fat

"PUFA" covers molecules that behave quite differently. The C20–C22 members with four or more double bonds, chiefly arachidonic acid (AA, 20:4n-6) and docosahexaenoic acid (DHA, 22:6n-3), are conserved. They are placed in phospholipids, held there, and in the brain delivered by a dedicated transporter: Mfsd2a imports DHA across the blood-brain barrier in the form of lysophosphatidylcholine {{< cite "nguyen2014" >}}. When DHA is catabolized, its chain-shortening begins in peroxisomes rather than mitochondria {{< cite "poirier2006" "wanders2006" >}}.

The C18 precursors, linoleic acid (LA, 18:2n-6) and α-linolenic acid (ALA, 18:3n-3), are dual-purpose. They are essential, because they cannot be synthesized, and they serve as structural and signaling substrates, yet they are also oxidized readily. Tracer studies in humans found that ALA is the most rapidly β-oxidized of the dietary C18 fatty acids, with LA oxidized faster than palmitate or stearate {{< cite "delany2000" >}}, and rat work shows the same hierarchy {{< cite "leyton1987" >}}. Much of that carbon does not leave as CO₂. It is recycled into newly synthesized cholesterol and saturated and monounsaturated fatty acids through *de novo* lipogenesis {{< cite "cunnane2003" >}}. The mitochondrial auxiliary enzyme 2,4-dienoyl-CoA reductase (DECR1) is needed to complete oxidation of unsaturated chains {{< cite "miinalainen2009" >}}. The brain follows the pattern: roughly 86% of unesterified LA entering the rat brain is β-oxidized {{< cite "demar2006" "taha2020" >}}, while DHA is imported and kept.

This means that a blanket claim that PUFAs are "not used as fuel" is wrong for the C18 essential fatty acids, and a claim that they are "burned" misdescribes the long-chain ones. The conserved long-chain species are the structural core. The C18 precursors are the supply line, and some of their flux inevitably goes to energy and carbon recycling. That is a normal property of an essential nutrient. It also means supply must exceed what oxidation takes.

## What Polyunsaturated Chains Do to a Membrane

Chain unsaturation changes how phospholipids pack. Increasing unsaturation raises membrane fluidity {{< cite "yang2011" >}}, and organisms adjust it to temperature, a process known as homeoviscous adaptation {{< cite "hazel1995" >}}. DHA-containing bilayers are thinner and more flexible than saturated or monounsaturated ones, and DHA's conformational flexibility allows it to interact with membrane proteins in ways that more rigid chains do not {{< cite "stillwell2003" >}}. In photoreceptor disk membranes, DHA-rich lipids are associated with the conformational transitions of rhodopsin {{< cite "grossfield2006" >}}.

The property that matters most is probably dynamic deformability rather than mechanical strength. Polyunsaturated phospholipids lower the energetic cost of bending a bilayer, and they facilitate the membrane deformation and fission driven by endocytic proteins such as dynamin and endophilin {{< cite "pinot2014" >}}. That makes them suited to places where membranes constantly change shape: synaptic vesicle cycling, endocytosis, and protein conformational changes.

The brain illustrates this. DHA makes up roughly 10–20% of total brain fatty acids, and 20–35% of the fatty acids in neuronal and synaptic phosphatidylethanolamine (PE) and phosphatidylserine (PS) {{< cite "svennerholm1968" "bazinet2014" >}}. Its share of total brain lipid is lower, because the lipid mass also includes cholesterol and sphingolipids that carry almost none. The mitochondrial inner membrane is a second example. It is low in cholesterol and rich in PE and cardiolipin, and cardiolipin in heart and skeletal muscle is dominated by linoleate, with tetralinoleoyl-cardiolipin as the main species {{< cite "schlame2002" "schlame2017" >}}. Brain cardiolipin is more heterogeneous, with oleate, arachidonate, and DHA contributing {{< cite "oemer2020" >}}. Dietary DHA can also remodel cardiac mitochondrial phospholipids and, in a heart-failure model, delayed calcium-induced opening of the permeability transition pore {{< cite "khairallah2010" >}}. So the structural PUFA of the mitochondrial inner membrane depends on tissue: linoleate in heart and muscle, with DHA more prominent in neural and retinal PE and PS. How cardiolipin remodeling fails is taken up in [When Architecture Fails]({{< relref "essays/when-architecture-fails" >}}).

## The Lands Cycle

A membrane's acyl composition is not set at synthesis. It is revised continuously by the Lands cycle, first described as a deacylation-reacylation route for phosphatidylcholine {{< cite "lands1958" >}}. A phospholipase A₂ removes the fatty acid at the *sn*-2 position, leaving a lysophospholipid, and an acyl-CoA-dependent lysophospholipid acyltransferase (an LPCAT or related LPLAT) installs a new chain in its place {{< cite "harayama2018" "wang2019" >}}. Different acyltransferases prefer different acyl-CoAs, which is how a cell can enrich *sn*-2 positions in AA or DHA while keeping *sn*-1 positions saturated or monounsaturated. The consequences are physiological. In cells lacking LPCAT3, polyunsaturated phospholipid content falls and membrane properties change {{< cite "rong2013" >}}.

Remodeling serves several purposes at once. It tunes fluidity, repairs oxidized or damaged chains, and releases AA for signaling when phospholipase is activated. Cardiolipin is remodeled differently: tafazzin transfers acyl groups between phospholipids and cardiolipin by CoA-independent transacylation, and does not use the acyl-CoA route {{< cite "schlame2017" >}}. The Lands cycle is therefore the general maintenance system, and cardiolipin remodeling is a specialized variant of it.

The cycle has an economic implication. Maintenance requires a supply of the right acyl-CoAs and acyltransferase capacity, and it competes with oxidation for the same fatty acid pool. A membrane can be remodeled only as fast as the structural fatty acids are available at the place and time they are needed.

## Two Ways the Architecture Fails

Two failure modes should be kept apart because they are different chemistry. The first is depletion, or catabolic diversion. Structural fatty acids are used up, mobilized, or oxidized faster than they are supplied and remodeled into membranes, and the membrane acyl composition drifts away from what the tissue needs. The enzymes responsible are ordinary ones: β-oxidation, lipases, and phospholipases operating on a pool that is too small for the job.

The second is peroxidation *in situ*, the non-enzymatic free-radical chain reaction in which an oxygen-centered radical abstracts hydrogen from a polyunsaturated chain already inside a phospholipid. This produces lipid hydroperoxides and, among its breakdown products, aldehydes such as 4-hydroxynonenal (4-HNE), which forms adducts with proteins {{< cite "esterbauer1991" "yin2011" >}}. 4-HNE inhibits cytochrome c oxidase, and conjugation with glutathione protects it {{< cite "chen1998" >}}. The enzymatic β-oxidation of a fatty acid for energy does not produce 4-HNE. The two processes share the word "oxidation" and little else. One is an enzyme-controlled pathway that ends in acetyl-CoA, and the other is uncontrolled damage to lipids in place.

The two failures can compound. A membrane depleted of its structural species is a poorer membrane, and one carrying more oxidizable chains than its antioxidant defenses can protect is a more vulnerable one. Neither needs to be present for the other to occur, and treating them as one is the source of much confusion about PUFAs.

## Four Drivers of Mismatch

At least four conditions can push a tissue toward structural or oxidative mismatch, and they work through different mechanisms.

The most direct is inadequate supply. Burr and Burr showed that rats fed a fat-free diet developed a deficiency syndrome that fat containing the essential fatty acids cured {{< cite "burr1930" >}}, and Holman's later work established the biochemical signature of deficiency {{< cite "holman1960" >}}. The human case was demonstrated in adults on continuous fat-free glucose–amino acid infusions, who developed biochemical deficiency within weeks despite abundant calories and intact fat stores {{< cite "wene1975" >}}, whereas removing glucose allowed insulin to fall, stored linoleate to mobilize, and deficiency to be avoided {{< cite "stegink1977" >}}. Supply failing to meet structural need is the simplest mismatch.

The second is chronic inflammatory or oxidative stress. The Ca²⁺-dependent cytosolic phospholipase A₂ (cPLA₂) and the calcium-independent iPLA₂ release *sn*-2 fatty acids and are activated by inflammatory signals, cytokines, and oxidative stress {{< cite "leslie2015" >}}. In moderation this serves repair and signaling. Sustained activation draws on the same pool that remodeling needs, and reacylation has to keep up {{< cite "wang2019" >}}.

The third is a hypercatabolic or fasting state. Fasting mobilizes adipose fatty acids and induces PPARα-driven fatty acid oxidation in the liver {{< cite "kersten1999" >}}. Thyroid hormone has long been tied to this territory, with effects on lipid metabolism and desaturase activity {{< cite "faas1982" "hoch1988" >}}. In states where oxidation and mobilization are high and intake is low, the oxidizable C18 precursors are drawn down alongside everything else, and the supply line to the long-chain structural species narrows.

The fourth runs in the opposite direction: more PUFA than structural and antioxidant capacity can handle. The relevant quantity is the amount in a membrane relative to the defenses protecting it. Dietary linoleic acid has risen substantially in the modern food supply and accumulates in adipose tissue in proportion to intake {{< cite "guyenet2015" >}}, and oxidized linoleic acid metabolites have been proposed as mediators of harm {{< cite "ramsden2012" >}}. Hibernators illustrate that tissue PUFA content has an upper bound, which is shaped by temperature and oxidative load {{< cite "frank1995" >}}. Glutathione peroxidase 4 (GPX4) is the defense that keeps membrane phospholipid peroxides in check, and when it fails, peroxidation of polyunsaturated phospholipids drives ferroptotic cell death {{< cite "carlson2016" >}}. The inference I draw is that adequacy is a window, with deficiency on one side and an excess of oxidizable chains over protective capacity on the other. The width of the window depends on the antioxidant system.

These four are not independent. A hypercatabolic state with poor intake combines the first and third, and chronic inflammation with a high-PUFA, low-antioxidant tissue combines the second and fourth. This is my synthesis of established mechanisms, not an experimentally validated classification.

## Back to Form

The bridge to thyroid hormone is the one *Guardian of Form* described. T3 regulates mitochondrial biogenesis, respiratory function, and substrate handling {{< cite "sagliocchi2024" >}}, and it influences lipid metabolism and membrane composition, including desaturase activity {{< cite "faas1982" "hoch1988" >}}. It raises the throughput and the demand for maintenance together. What it does not do is supply the structural substrates. Higher thyroid activity on top of inadequate essential fatty acid supply, a stressed phospholipase system, or limited antioxidant capacity widens the gap between what membranes need and what they receive.

The practical reading is modest. Adequate essential fatty acid intake is a precondition for membrane maintenance, and nothing here argues against it. But supply alone does not ensure that membranes are well kept. Mobilization, remodeling capacity, and antioxidant defense all have to work, and excess PUFA beyond what those systems can protect is a separate way for the system to go wrong. What happens when the maintenance of one specialized membrane lipid, cardiolipin, fails is a case study in its own right, and it is the subject of [When Architecture Fails]({{< relref "essays/when-architecture-fails" >}}).

{{< references >}}
