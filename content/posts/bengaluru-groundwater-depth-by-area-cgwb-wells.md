---
title: "Bengaluru Groundwater Depth by Area: CGWB Well Data"
meta_description: "Pre-monsoon depth to water at 64 CGWB monitoring wells in Bengaluru Urban and Rural, May 2014, 2024 and 2025, with a map and CSV for buyers."
slug: "bengaluru-groundwater-depth-by-area-cgwb-wells"
date_modified: "2026-10-21"
date_published: "2026-10-21"
dataset_name: "Bengaluru CGWB monitoring wells: pre-monsoon depth to water level"
dataset_description: "Central Ground Water Board pre-monsoon (May) depth to water level, in metres below ground level, for 64 monitoring wells in Bengaluru Urban and Bengaluru Rural districts that reported in May 2024 or May 2025, with May 2014 and May 2019 readings where the same well reported. Extracted 21 Oct 2026."
dataset_distribution: "assets/data/bengaluru-groundwater-depth-by-area-cgwb-wells.geojson"
dataset_csv: "assets/data/bengaluru-groundwater-depth-by-area-cgwb-wells.csv"
include_howto: "yes"
---

# Bengaluru groundwater depth by area: what the CGWB wells show

**Short answer:** In May 2024, before the monsoon, the Central Ground Water Board (CGWB) measured water at a median depth of 5.93 m below ground across 29 monitoring wells in the Bangalore City block, and 17.61 m across 31 wells in the rest of Bengaluru Urban and Bengaluru Rural. Twelve of the 60 wells measured that month read 30 m or deeper. The deepest was Kengal, Nelamangala, at 122.69 m.

> **Key takeaways**
> - **64 CGWB wells** in Bengaluru Urban and Bengaluru Rural reported a pre-monsoon reading in May 2024 or May 2025: 60 in May 2024 and 20 in May 2025.
> - **May 2024 spread:** 19 wells under 5 m, 17 between 5 and 15 m, 12 between 15 and 30 m, and 12 at 30 m or deeper.
> - **City block vs the fringe:** the median was 5.93 m in the Bangalore City block and 17.61 m outside it. Readings of 80 m or more came from Kengal (122.69 m), Immadihally (97.5 m), the GSI piezometer (82.5 m) and Bhaktipura, Anekal (81.73 m).
> - **Ten years on:** of 39 wells read in both May 2014 and May 2024, 24 had water nearer the surface in 2024 and 15 had it deeper.
> - **This is not borewell yield.** A water level in a CGWB monitoring well tells you how far down the water stood on one day. It does not tell you how much a borewell on your plot will give, or for how long.

These figures come from the CGWB ground water level monitoring network, as republished in the "Pre and Post Monsoon Depth to Water Level, CGWB" layer on the Esri India Living Atlas. We extracted every Bengaluru Urban and Bengaluru Rural record on 21 Oct 2026 and kept the pre-monsoon (May) readings, because May is when the water table is usually at its lowest. A well appears below only if it reported in May 2024 or May 2025.

<div class="ak-map-wrap">
<div id="groundwater-map" class="ak-map" data-root="../" data-geo="../assets/data/bengaluru-groundwater-depth-by-area-cgwb-wells.geojson" data-legend="groundwater-legend" role="region" aria-label="Map of CGWB groundwater monitoring wells in Bengaluru shaded by depth to water"></div>
<script type="application/json" id="groundwater-legend">[{"id":"gw-a","label":"Under 5 m","on":true},{"id":"gw-b","label":"5 to 15 m","on":true},{"id":"gw-c","label":"15 to 30 m","on":true},{"id":"gw-d","label":"30 m or deeper","on":true}]</script>
<p class="ak-map-note">Scroll to load the map. It needs JavaScript and OpenStreetMap tiles. Lighter circles mean water nearer the surface, darker circles mean deeper water, using the May 2024 reading (May 2025 for the four wells with no 2024 reading). Every well is also in the table, which works without JavaScript.</p>
<script src="../assets/ak-map.js?v=2" defer></script>
</div>

Downloads: [GeoJSON](../assets/data/bengaluru-groundwater-depth-by-area-cgwb-wells.geojson), [CSV](../assets/data/bengaluru-groundwater-depth-by-area-cgwb-wells.csv).

## What the number means

**Depth to water level** is the distance from the ground surface down to the water standing in the well, in metres below ground level (mbgl). A bigger number means water is further down. CGWB reads its network four times a year. This page uses the pre-monsoon round, which CGWB took on 25 May 2014, 27 May 2019, 10 May 2024 and 30 May 2025 in this data.

**The wells are CGWB's, not private borewells.** The network mixes open dug wells and purpose-built piezometers. Names such as "Gsi Pz" and "Thalaghattapurapz" are piezometers. A piezometer can tap a deeper aquifer than a dug well a few hundred metres away, which is one reason two nearby readings can differ by tens of metres.

**Names and coordinates are as CGWB publishes them.** A few labels do not match the place you might expect from the name. For example, the well labelled Jigani sits at 12.9111° N, 77.5678° E, inside the city block. We have not renamed or moved any well.

## How to read the well nearest a home

### Find the nearest well on the map
Open the map and tap the circle closest to the address. The popup gives the CGWB name, the block and the May reading. The nearest well may be several kilometres away. Bengaluru has 64 wells in this set, not one per neighbourhood.

### Look at more than one year
Compare May 2014, May 2024 and May 2025 in the table. A well that reads 3 m one year and 4 m the next is behaving steadily. A well that jumps from 40 m to 120 m between two readings needs a second source before you draw any conclusion from it.

### Ask the seller for their own borewell record
For a house or a plot with a borewell, ask for the drilling depth, the year it was drilled, and whether it has gone dry. In a flat, ask the association how many borewells the building runs, how many tankers it bought last summer, and whether it has a BWSSB connection. Our [water questions for buyers](https://acrenkey.com/blogs/water-bengaluru-bwssb-borewell-tanker-questions-to-ask/) list these in full.

### Check piped supply before you rely on groundwater
Where BWSSB Cauvery water reaches, groundwater matters less to day-to-day supply. See our [Cauvery Stage 5 coverage guide](https://acrenkey.com/blogs/cauvery-stage-5-coverage-which-areas-get-bwssb-water/) for which areas the newest stage serves.

## Patterns in the 2024 readings

**Shallow water under the old city.** Fourteen of the 29 Bangalore City wells read under 5 m in May 2024: among them Vasanthnagara (2.00 m), Malleswaram (2.95 m), Byrasandra (3.40 m), HSR Layout (2.38 m) and Rajajinagara (2.50 m).

**Deep readings at the edges and on higher ground.** Five city-block wells read 30 m or deeper: Immadihally (97.5 m), Gsi Pz (82.5 m), IIm Bannerughatta (44.82 m), Varathur (31.68 m) and Singasandra (31.65 m). Outside the city block, Kengal and Doddabele in Nelamangala, Bhaktipura in Anekal and Hanumanapalya in Nelamangala all read over 50 m.

**A mixed ten-year picture.** Of the 39 wells read in both May 2014 and May 2024, 24 had water nearer the surface in 2024. Dodballapur (40.49 m to 20.55 m) and Kanasavadi (47.17 m to 29.18 m) moved the most in that direction. The Gsi Pz piezometer went the other way, from 11.85 m to 82.5 m. A single May reading is affected by that year's rain, so treat one year's change with care.

## Well by well

Depths are metres below ground level in the pre-monsoon (May) round. "–" means CGWB has no reading for that well in that round in this data. In the last column a minus sign means water was nearer the surface in 2024 than in 2014.

### Bengaluru Urban district

| CGWB station | Block | May 2014 (m) | May 2024 (m) | May 2025 (m) | 2014 to 2024 |
|---|---|---|---|---|---|
| Anekal (Rural) | Anekal | 25.05 | 19.47 | – | -5.58 m |
| Begihalli | Anekal | 1.95 | 1.25 | 0.12 | -0.70 m |
| Bhaktipura | Anekal | – | 81.73 | – | – |
| Haragadde | Anekal | 9.14 | 3.02 | 1.10 | -6.12 m |
| Adugodi | Bangalore City | 3.98 | 4.50 | – | +0.52 m |
| Bangalore | Bangalore City | 3.48 | 0.87 | 1.21 | -2.61 m |
| Basavanagudi | Bangalore City | 5.47 | 4.98 | 2.93 | -0.49 m |
| Beguru | Bangalore City | 5.30 | – | 9.11 | – |
| Bhattarahalli | Bangalore City | – | 15.26 | – | – |
| Byrasandra | Bangalore City | 2.96 | 3.40 | 1.78 | +0.44 m |
| Chennamankere Achkattu | Bangalore City | 2.83 | 3.80 | 1.47 | +0.97 m |
| Gollahalli | Bangalore City | 1.76 | – | 0.80 | – |
| Gottigere | Bangalore City | 2.11 | 2.34 | – | +0.23 m |
| Gsi Pz | Bangalore City | 11.85 | 82.50 | – | +70.65 m |
| Hsr Layout | Bangalore City | – | 2.38 | 1.20 | – |
| IIm Bannerughatta | Bangalore City | – | 44.82 | – | – |
| Immadihally | Bangalore City | – | 97.50 | – | – |
| Indiranagar | Bangalore City | 8.98 | 13.70 | – | +4.72 m |
| Jayanagar | Bangalore City | 11.19 | 12.06 | – | +0.87 m |
| Jayanagara | Bangalore City | 10.83 | 6.57 | 2.11 | -4.26 m |
| Jigani | Bangalore City | – | 3.12 | 1.59 | – |
| Kodigehalli | Bangalore City | 4.24 | 4.16 | 3.43 | -0.08 m |
| Lalbagh Garden | Bangalore City | 4.95 | 8.14 | – | +3.19 m |
| Malleswaram | Bangalore City | 4.27 | 2.95 | 4.45 | -1.32 m |
| Nimhans | Bangalore City | – | 22.70 | – | – |
| Rajajinagara | Bangalore City | 2.02 | 2.50 | 4.18 | +0.48 m |
| Sadaramangala | Bangalore City | – | 7.85 | – | – |
| Seva Kshetra Hospital Banshankari II | Bangalore City | – | 1.40 | 7.01 | – |
| Singasandra | Bangalore City | 31.34 | 31.65 | – | +0.31 m |
| Thalaghattapurapz | Bangalore City | 18.65 | 9.28 | – | -9.37 m |
| Ulsoor | Bangalore City | – | – | 2.67 | – |
| Varathur | Bangalore City | 32.23 | 31.68 | – | -0.55 m |
| Vasanthnagara | Bangalore City | 0.14 | 2.00 | 0.86 | +1.86 m |
| Vasanthpura | Bangalore City | 6.06 | 5.93 | 4.21 | -0.13 m |
| Wilson Garden | Bangalore City | 1.28 | 4.78 | 3.73 | +3.50 m |
| Yelahanka | Bangalore City | 30.85 | 18.31 | – | -12.54 m |
| Kannamangala | Bengaluru East | – | 34.17 | – | – |
| Kodathi | Bengaluru East | – | 24.82 | – | – |
| Dasanapura | Bengaluru North | 19.00 | 28.31 | – | +9.31 m |
| Bang Uni Ars Us | Bengaluru South | – | 42.08 | – | – |
| Chandasipalya | Bengaluru South | 9.33 | – | 4.46 | – |
| Hesaraghatta | Yelahanka | – | 14.95 | – | – |

### Bengaluru Rural district

| CGWB station | Block | May 2014 (m) | May 2024 (m) | May 2025 (m) | 2014 to 2024 |
|---|---|---|---|---|---|
| Avathi | Devanhalli | 13.60 | 7.24 | – | -6.36 m |
| Beerasandra | Devanhalli | – | 7.13 | – | – |
| Devenahalli | Devanhalli | 22.28 | 12.55 | – | -9.73 m |
| Devenahalli | Devanhalli | 23.76 | 17.61 | – | -6.15 m |
| Kodagurki | Devanhalli | 6.77 | 3.87 | – | -2.90 m |
| Vishwanathapura | Devanhalli | 5.78 | 5.25 | – | -0.53 m |
| Vishwanathapura | Devanhalli | – | 20.02 | – | – |
| Dodballapur | Dodballapur | 10.74 | 3.83 | – | -6.91 m |
| Dodballapur | Dodballapur | 40.49 | 20.55 | – | -19.94 m |
| Gollahalli | Dodballapur | – | 5.58 | – | – |
| Kanasavadi | Dodballapur | 47.17 | 29.18 | – | -17.99 m |
| Madhure | Dodballapur | – | 37.65 | – | – |
| Siddenaykanahalli | Dodballapur | – | 8.86 | – | – |
| Hosakote | Hoskote | 33.62 | 26.71 | – | -6.91 m |
| Doddabele | Nelamangala | – | 56.42 | – | – |
| Gangenapura | Nelamangala | 5.58 | 5.35 | – | -0.23 m |
| Hanumanapalya | Nelamangala | – | 56.47 | – | – |
| Kengal | Nelamangala | – | 122.69 | – | – |
| Mahadevapura | Nelamangala | 5.47 | 5.83 | – | +0.36 m |
| Shivagange | Nelamangala | 10.00 | 8.30 | – | -1.70 m |
| Shivagange | Nelamangala | 13.85 | 4.20 | – | -9.65 m |
| Yentiganahalli | Nelamangala | 19.19 | 20.62 | – | +1.43 m |

## Frequently asked questions

### Does a shallow reading mean a borewell will give water?

No. The reading is the water level in one CGWB monitoring well on one day in May. Borewell yield depends on the rock and fractures under your plot, the depth drilled and how many other borewells draw from the same aquifer.

### Why are there only 64 wells for the whole of Bengaluru?

These are the wells in CGWB's national monitoring network for Bengaluru Urban and Bengaluru Rural that reported in May 2024 or May 2025. The state groundwater directorate and BWSSB keep other records that are not in this set.

### Why do two nearby wells read so differently?

They may tap different layers. A dug well shows the shallow water table. A piezometer can be cased down to a deeper aquifer. Local recharge from a tank or a park can also keep one well shallow while another a short distance away reads deep.

### Which month do the figures refer to?

The pre-monsoon round: 25 May 2014, 27 May 2019, 10 May 2024 and 30 May 2025 in this data. Post-monsoon readings, taken after the rains, are usually shallower and are not used here.

### Can I use this to choose between two areas?

Use it as one input. If both areas get BWSSB Cauvery water, the well readings matter less. If a building runs mostly on borewells and tankers, a deep, falling reading nearby is a reason to ask harder questions about summer supply.

## Talk it through with acre&key

If a home you are considering depends on borewells, bring the nearest well from this table and acre&key will go through the water questions with you: the building's borewell record, its tanker bills and its BWSSB connection.

## Sources

Checked 21 Oct 2026.

1. Central Ground Water Board, Ministry of Jal Shakti, ground water level monitoring: https://www.cgwb.gov.in/ground-water-level-monitoring
2. CGWB pre- and post-monsoon depth to water level, 1994 to 2026, as republished in the Esri India Living Atlas layer "Pre_Post_Monsoon_DTWL_CGWB_2014_2024" (fields: state, district, block, village, latitude, longitude, season date, depth to water level in mbgl). Bengaluru Urban and Bengaluru Rural records extracted 21 Oct 2026: https://livingatlas.esri.in/server1/rest/services/Water/Pre_Post_Monsoon_DTWL_CGWB_2014_2024/MapServer/0
3. India-WRIS, the national water resources information system where CGWB station data is also published: https://indiawris.gov.in/
4. Map tiles: OpenStreetMap contributors: https://www.openstreetmap.org/copyright
5. Hero photograph: "Water in the borewell", Wikimedia Commons, released into the public domain: https://commons.wikimedia.org/wiki/File:Water_in_the_borewell.JPG

## Suggested images

1. Hero and card, 1200x675 WebP, at assets/img/bengaluru-groundwater-depth-by-area-cgwb-wells.webp. Alt: "Water pouring from a green hand pump into a metal bucket"
