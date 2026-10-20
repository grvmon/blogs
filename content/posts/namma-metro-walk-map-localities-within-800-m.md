---
title: "Namma Metro Walk Map: Localities Within 800 m of Each Station"
meta_description: "Open and under-construction Namma Metro stations in Bengaluru, with every OSM locality node inside 800 m of the station."
slug: "namma-metro-walk-map-localities-within-800-m"
date_modified: "2026-10-20"
date_published: "2026-10-20"
dataset_name: "Namma Metro stations and OSM localities within 800 m"
dataset_description: "OpenStreetMap station nodes on the Purple, Green and Yellow route relations, nodes tagged under construction, and named place nodes within 800 m. Extracted 20 Oct 2026."
dataset_distribution: "assets/data/namma-metro-800m-stations.geojson"
dataset_csv: "assets/data/namma-metro-800m-stations.csv"
include_howto: "yes"
---

# Namma Metro walk map: localities within 800 m of each station

**Short answer:** This page lists 82 Namma Metro stations that OpenStreetMap maps on the Purple, Green or Yellow route relations, and 47 stations tagged under construction. For each one it names the OSM locality nodes whose own coordinates fall within 800 m. It does not estimate a walking time.

> **Key takeaways**
> - **82 stations** sit on a Purple, Green or Yellow route relation: 36 Purple, 29 Green, 15 Yellow, plus Majestic on Purple and Green, and Rashtreeya Vidyalaya Road on Green and Yellow.
> - **47 stations** are tagged `construction=station` and carry "(u/c)" in the OSM name: 18 Pink and 29 Blue. Filled circles on the map are the operating routes. Rings are under construction.
> - **800 m is a straight-line test** on the place node's coordinates, using a haversine radius of 6,371,000 m. It is not a walking path and not a neighbourhood boundary.
> - **1,234 named place nodes** (suburb, neighbourhood, quarter, locality) were in the extract. Thirteen stations have none of them within 800 m.
> - Stations OSM tags as proposed, including later Orange and Red alignments, are not plotted. Line progress beyond these tags is on our [metro lines page](https://acrenkey.com/blogs/bengaluru-metro-lines-2026-status-of-every-line-for-homebuyers/).

The coordinates and the locality names are from OpenStreetMap, extracted on 20 Oct 2026. The copyright sits with OpenStreetMap contributors under the Open Database Licence. A locality that exists on the ground but has no place node in this extract will not appear. A place node just outside 800 m will not appear even if the neighbourhood itself reaches the station.

<div class="ak-map-wrap">
<div id="metro-map" class="ak-map" data-root="../" data-geo="../assets/data/namma-metro-800m-stations.geojson" data-legend="metro-legend" role="region" aria-label="Map of Namma Metro stations in Bengaluru"></div>
<script type="application/json" id="metro-legend">[{"id":"open","label":"Operating route","on":true},{"id":"uc","label":"Under construction","on":true}]</script>
<p class="ak-map-note">Scroll to load the map. It needs JavaScript and OpenStreetMap tiles. Filled circles are stations on an operating route relation. Rings are tagged under construction. The full locality list is in the table, which works without JavaScript.</p>
<script src="../assets/ak-map.js" defer></script>
</div>

Downloads: [GeoJSON](../assets/data/namma-metro-800m-stations.geojson), [CSV](../assets/data/namma-metro-800m-stations.csv).

## How the 800 m list was built

The extract covers 12.70° N to 13.35° N and 77.30° E to 77.90° E. Station nodes are those with `network=Namma Metro`.

**Operating route.** The node is `railway=station` and `station=subway`, and it belongs to a route relation whose `ref` is Purple, Green or Yellow, or a stop node within 80 m has the same name after a trailing parenthesis is removed and "Stn." is read as "Station". That second step is how Nadaprabhu Kempegowda Station, Majestic picks up both Purple and Green, and how Sri Balagangadharanatha Swamiji Station, Hosahalli picks up Purple. All 82 station nodes matched a route.

**Under construction.** The node name contains "(u/c)" and `construction=station`. The line is the OSM `colour` tag: pink or blue. Three nodes named Jayadeva Interchange (u/c) sat within 50 m of each other. The table keeps the one whose colour tag is pink, which is the Pink line. Nagawara has a separate Pink node and a separate Blue node, 186 m apart, so both stay.

**Localities.** Every named node tagged suburb, neighbourhood, quarter or locality in the box was tested. Distance is the haversine on a sphere of radius 6,371,000 m, and a node is listed when that distance is 800 m or less. The metres in the table are that distance rounded to the nearest metre. The place type is the OSM `place` tag, in brackets.

Halasuru, on the Purple line, has the longest list in this extract: 14 place nodes, the nearest being Dodakattappa at 170 m. Thirteen stations have an empty list. Airport City, Doddajala and KIAL Terminals are three of the under-construction stations in that group. An empty cell means the extract had no place node inside the circle. It does not mean nobody lives there.

OSM also has nodes tagged `proposed=station` for alignments that are not these operating routes and not these under-construction tags. They are left off the map so a proposed pin is not read as a station under construction. Phase 3 is covered, as a route description rather than a walk map, in our [Phase 3 guide](https://acrenkey.com/blogs/namma-metro-phase-3-route-areas-likely-to-gain-access/).

## How to check a home against this list

### Find the station the brochure names
Use the station name in the table, not the locality name in the advertisement. Majestic in OSM is Nadaprabhu Kempegowda Station, Majestic. Hosahalli is Sri Balagangadharanatha Swamiji Station, Hosahalli. Jayadeva Hospital is on the Yellow line and is an operating station. Jayadeva Interchange is a separate under-construction Pink node.

### Read the locality cell
If your neighbourhood is named there, the figure in metres is the straight-line distance from the station node to the place node. Indiranagar's Purple station, for example, has Indiranagar 1st Stage at 124 m and the Indiranagar suburb node at 594 m. Both are inside 800 m. They are two different OSM nodes.

### Do not turn 800 m into a walk time
The test does not follow footpaths, station exits or the road you would actually use. A place node 600 m away can be a longer walk once you leave by the far exit. Our [questions before buying near a metro station](https://acrenkey.com/blogs/15-questions-before-buying-near-a-metro-station/) cover the exit, the last train and the road, which this table does not.

### Check the status column before you treat the station as open
"Operating route" means the node is on a Purple, Green or Yellow relation in this extract. "Under construction" means OSM tags it `construction=station`. An under-construction station is not a station you can board. For where Pink and Blue construction stood in October 2026, use the [metro lines page](https://acrenkey.com/blogs/bengaluru-metro-lines-2026-status-of-every-line-for-homebuyers/), which cites the government answers.

### Treat a missing name as a gap in the map, not a verdict
If the locality you care about is not in the cell, look at the latitude and longitude and measure your own address against the station. The place-node layer is incomplete by nature. It is a published OSM tag, not a municipal ward list.

## Station by station

Localities are `name (place tag, metres)`. "None in this OSM place-node extract" means no named suburb, neighbourhood, quarter or locality node fell inside 800 m.

| Station | OSM status | Line | Latitude | Longitude | Place nodes within 800 m | Localities |
|---|---|---|---|---|---|---|
| Attiguppe | Operating route | Purple | 12.96189 | 77.53358 | 6 | Hampi Nagar (quarter, 268 m); Attiguppe (quarter, 490 m); Vijaya Nagar (suburb, 539 m); PF Layout (neighbourhood, 647 m); Vinayaka Layout (neighbourhood, 724 m); BCC Layout (quarter, 730 m) |
| Baiyappanahalli | Operating route | Purple | 12.99076 | 77.65236 | 3 | Ramaswamy Layout (neighbourhood, 610 m); Baiyyappanahalli (suburb, 629 m); Krishnaiahnapalya (neighbourhood, 726 m) |
| Banashankari | Operating route | Green | 12.91522 | 77.5736 | 4 | Shakambari Nagar (neighbourhood, 313 m); Teacher's Colony (neighbourhood, 654 m); Jayanagar 8th Block (quarter, 664 m); JP Nagar 1st Phase (quarter, 774 m) |
| Benniganahalli | Operating route | Purple | 12.99652 | 77.66846 | 6 | Pai Layout (neighbourhood, 425 m); Udaya Nagar (neighbourhood, 432 m); Gangappa Layout (neighbourhood, 433 m); Darga Mohalla (neighbourhood, 625 m); Benniganahalli (neighbourhood, 659 m); Putanna Garden (neighbourhood, 729 m) |
| Beratena Agrahara | Operating route | Yellow | 12.86388 | 77.6579 | 0 | None in this OSM place-node extract |
| Biocon Hebbagodi | Operating route | Yellow | 12.82903 | 77.68137 | 1 | Hebbagodi (neighbourhood, 300 m) |
| Bommanahalli | Operating route | Yellow | 12.91062 | 77.62648 | 5 | Roopena Agrahara (neighbourhood, 287 m); Bommanahalli (quarter, 335 m); N. G. R. Layout (neighbourhood, 471 m); MCHS Colony (neighbourhood, 551 m); Sector 6 (quarter, 702 m) |
| BTM Layout | Operating route | Yellow | 12.91659 | 77.60812 | 10 | BTM Layout 2nd Stage (quarter, 287 m); BTM Layout (suburb, 371 m); BTM Layout 1st Stage (quarter, 436 m); Maruthi Layout (neighbourhood, 449 m); MICO Layout (neighbourhood, 618 m); Tavarekere (neighbourhood, 624 m); Kuvempu Nagar (neighbourhood, 655 m); IAS Officers Colony (neighbourhood, 665 m); Gurappana Palya (neighbourhood, 696 m); SFHS Layout (neighbourhood, 753 m) |
| Central Silk Board | Operating route | Yellow | 12.91658 | 77.62057 | 8 | Dollar Scheme Colony (neighbourhood, 207 m); BTM 2nd Stage (neighbourhood, 333 m); Jai Bheema Nagar (neighbourhood, 502 m); N. G. R. Layout (neighbourhood, 549 m); MCHS Colony (neighbourhood, 649 m); Sidhartha Colony (neighbourhood, 725 m); Roopena Agrahara (neighbourhood, 749 m); Kuvempu Nagar (neighbourhood, 776 m) |
| Challaghatta | Operating route | Purple | 12.89735 | 77.46129 | 1 | Anchepalya (neighbourhood, 706 m) |
| Chickpete | Operating route | Green | 12.9669 | 77.57456 | 7 | Ranasingpete (neighbourhood, 238 m); Old Tharagupete (neighbourhood, 246 m); Chikkapete (suburb, 344 m); Sultanpete (neighbourhood, 346 m); Mamulpete (neighbourhood, 406 m); Sowrashtrapet (locality, 641 m); Balepet (neighbourhood, 708 m) |
| Chikkabidarakallu | Operating route | Green | 13.05236 | 77.48792 | 1 | Manjunath Nagar (neighbourhood, 676 m) |
| Cubbon Park | Operating route | Purple | 12.98096 | 77.59758 | 0 | None in this OSM place-node extract |
| Dasarahalli | Operating route | Green | 13.04326 | 77.51255 | 0 | None in this OSM place-node extract |
| Deepanjali Nagar | Operating route | Purple | 12.95206 | 77.53701 | 8 | Deepanjali Nagar (locality, 164 m); BCC Layout (locality, 415 m); Bapuji Nagar (quarter, 533 m); KHR Colony (neighbourhood, 621 m); NTY Layout (neighbourhood, 656 m); Byataranyapura (quarter, 681 m); Ganapathy Nagar (neighbourhood, 696 m); BCC Layout (quarter, 737 m) |
| Delta Electronics Bommasandra | Operating route | Yellow | 12.81939 | 77.68835 | 1 | Bommasandra (suburb, 498 m) |
| Doddakallasandra | Operating route | Green | 12.88464 | 77.55275 | 1 | Narayana Nagara (neighbourhood, 420 m) |
| Dr. B. R. Ambedkar Station, Vidhana Soudha | Operating route | Purple | 12.97874 | 77.59164 | 0 | None in this OSM place-node extract |
| Electronic City | Operating route | Yellow | 12.85651 | 77.66352 | 2 | Konappana Agrahara (neighbourhood, 646 m); Electronics City Phase 1 (quarter, 775 m) |
| Garudacharpalya | Operating route | Purple | 12.99345 | 77.70368 | 5 | Garudacharpalya (neighbourhood, 343 m); Kaveri Nagara (neighbourhood, 510 m); Devasandra Industrial Estate (neighbourhood, 533 m); ITI Industrial Estate (neighbourhood, 675 m); RHB Colony (neighbourhood, 728 m) |
| Halasuru | Operating route | Purple | 12.9765 | 77.62669 | 14 | Dodakattappa (neighbourhood, 170 m); Jogupalya (neighbourhood, 248 m); Halasuru (suburb, 267 m); Gupta Layout (neighbourhood, 410 m); Hoysala Nagar (neighbourhood, 419 m); Someshwarpura (neighbourhood, 427 m); Lakshmipuram (neighbourhood, 448 m); MV Garden (neighbourhood, 511 m); Jayaraj Nagar (neighbourhood, 519 m); Saraswathipuram (neighbourhood, 568 m); LBS Nagar (neighbourhood, 605 m); Keshavaraj Layout (neighbourhood, 623 m); Corporation Colony (neighbourhood, 713 m); Cambridge Layout (neighbourhood, 719 m) |
| Hongasandra | Operating route | Yellow | 12.9017 | 77.63199 | 2 | Mangamannapalya (neighbourhood, 460 m); GarvebhaviPalya (neighbourhood, 789 m) |
| Hoodi | Operating route | Purple | 12.9888 | 77.71133 | 2 | Hoodi (suburb, 631 m); Ashraya Layout (neighbourhood, 717 m) |
| Hopefarm Channasandra | Operating route | Purple | 12.9873 | 77.75388 | 3 | Maithri Layout (neighbourhood, 349 m); Prashanth Extension (neighbourhood, 682 m); Kadugodi Colony (neighbourhood, 698 m) |
| Hosa Road | Operating route | Yellow | 12.87075 | 77.65245 | 0 | None in this OSM place-node extract |
| Huskur Road | Operating route | Yellow | 12.83916 | 77.67737 | 1 | Electronics City Phase 2 (West) (quarter, 571 m) |
| Indiranagar | Operating route | Purple | 12.97833 | 77.63866 | 13 | Indiranagar 1st Stage (neighbourhood, 124 m); Indiranagar 2nd Stage (neighbourhood, 139 m); Old Binnamangala (neighbourhood, 342 m); Indiranagar 3rd Stage (neighbourhood, 343 m); Appareddipalaya (neighbourhood, 486 m); Subedar Garden (neighbourhood, 561 m); Motappanapalya (neighbourhood, 575 m); Defence Colony (neighbourhood, 580 m); Indiranagar (suburb, 594 m); Hutting Colony (neighbourhood, 599 m); Eshwara Layout (neighbourhood, 689 m); Binnamangala (neighbourhood, 709 m); LBS Nagar (neighbourhood, 722 m) |
| Infosys Foundation Konappana Agrahara | Operating route | Yellow | 12.84644 | 77.67119 | 3 | Electronics City Phase 2 (East) (quarter, 624 m); Electronics City Phase 1 (quarter, 764 m); Konappana Agrahara (neighbourhood, 785 m) |
| Jalahalli | Operating route | Green | 13.03941 | 77.51974 | 0 | None in this OSM place-node extract |
| Jaya Prakash Nagar | Operating route | Green | 12.90747 | 77.57313 | 3 | Ilyas Nagar (neighbourhood, 417 m); Sarakki (neighbourhood, 744 m); Shakambari Nagar (neighbourhood, 744 m) |
| Jayadeva Hospital | Operating route | Yellow | 12.91673 | 77.59997 | 5 | BHBCS Layout (neighbourhood, 187 m); SFHS Layout (neighbourhood, 339 m); Gurappana Palya (neighbourhood, 578 m); MICO Layout (neighbourhood, 587 m); JP Nagar 3rd Phase (quarter, 606 m) |
| Jayanagar | Operating route | Green | 12.92951 | 77.58014 | 7 | Jayanagar (suburb, 248 m); Jayanagar 6th Block (quarter, 250 m); Jayanagar 4th Block (quarter, 489 m); Jayanagar 7th Block (quarter, 530 m); Jayanagar 3rd Block (quarter, 577 m); Geetha Colony (neighbourhood, 580 m); Yediyuru (neighbourhood, 650 m) |
| Jnanabharathi | Operating route | Purple | 12.93542 | 77.51218 | 1 | Ideal Homes Layout (neighbourhood, 381 m) |
| Kadugodi Tree Park | Operating route | Purple | 12.98565 | 77.74701 | 2 | Prashanth Extension (neighbourhood, 314 m); Kadugodi Colony (neighbourhood, 779 m) |
| Kengeri | Operating route | Purple | 12.90791 | 77.47658 | 0 | None in this OSM place-node extract |
| Kengeri Bus Terminal | Operating route | Purple | 12.91479 | 77.48777 | 2 | Vijayashree Layout (neighbourhood, 437 m); BDA Jnanabharathi Residential Enclave (neighbourhood, 585 m) |
| Konanakunte Cross | Operating route | Green | 12.88897 | 77.56267 | 0 | None in this OSM place-node extract |
| Krantivira Sangolli Rayanna Railway Station | Operating route | Purple | 12.97588 | 77.56538 | 1 | Nagamma Nagar (neighbourhood, 779 m) |
| Krishna Rajendra Market | Operating route | Green | 12.96088 | 77.57466 | 2 | Kalasipalyam (quarter, 380 m); Ranasingpete (neighbourhood, 779 m) |
| Krishnarajapura | Operating route | Purple | 12.9999 | 77.67767 | 3 | Darga Mohalla (neighbourhood, 489 m); Udaya Nagar (neighbourhood, 689 m); A Narayanapura (neighbourhood, 799 m) |
| Kudlu Gate | Operating route | Yellow | 12.88993 | 77.63922 | 1 | GarvebhaviPalya (neighbourhood, 761 m) |
| Kundalahalli | Operating route | Purple | 12.97759 | 77.71556 | 3 | Channama Layout (neighbourhood, 357 m); Green Domain Layout (neighbourhood, 533 m); Sitaramapalya (quarter, 548 m) |
| Lalbagh | Operating route | Green | 12.94653 | 77.58002 | 4 | Kankanpalya (neighbourhood, 652 m); Basavanagudi (suburb, 724 m); Mavalli (neighbourhood, 734 m); Jayanagar 2nd Block (quarter, 789 m) |
| Madavara | Operating route | Green | 13.05742 | 77.47281 | 1 | Madhavara (suburb, 470 m) |
| Magadi Road | Operating route | Purple | 12.97563 | 77.55535 | 3 | Rajajinagar 6th Block (neighbourhood, 347 m); Kempapura Agrahara (suburb, 557 m); Rajajinagar 4M Block (neighbourhood, 769 m) |
| Mahakavi Kuvempu Road | Operating route | Green | 12.99853 | 77.5569 | 7 | Gayatri Nagar (neighbourhood, 284 m); Mariappanapalya (neighbourhood, 297 m); Rajajinagar 2nd Block (neighbourhood, 581 m); Ketamaranahalli (neighbourhood, 601 m); Subrahmanya Nagar (quarter, 608 m); Jooganahalli (neighbourhood, 650 m); Maruthi Extension (neighbourhood, 679 m) |
| Mahalakshmi | Operating route | Green | 13.00805 | 77.54881 | 7 | Rajajinagara 1st R Block (neighbourhood, 94 m); Rajajinagara 1st N Block (neighbourhood, 496 m); Mahalakshmi Layout (suburb, 575 m); Rajajinagar 1st Block (neighbourhood, 603 m); Nagapura (neighbourhood, 691 m); Ashokapuram (neighbourhood, 762 m); Subramanya Nagar 2nd Stage (neighbourhood, 781 m) |
| Mahatma Gandhi Road | Operating route | Purple | 12.97553 | 77.60679 | 2 | Tasker Town (neighbourhood, 526 m); Ashok Nagar (quarter, 727 m) |
| Manjunathanagara | Operating route | Green | 13.05009 | 77.49445 | 2 | Manjunath Nagar (neighbourhood, 441 m); Muniswamappa Layout (neighbourhood, 798 m) |
| Mantri Square Sampige Road | Operating route | Green | 12.99046 | 77.57073 | 5 | Valluvarpuram (neighbourhood, 576 m); Seshadripuram (quarter, 584 m); Nehru Nagar (neighbourhood, 652 m); Sriramapuram (quarter, 752 m); Kumara Park West (neighbourhood, 782 m) |
| Mysore Road | Operating route | Purple | 12.94672 | 77.53016 | 2 | KHR Colony (neighbourhood, 574 m); Pantarapalya (neighbourhood, 690 m) |
| Nadaprabhu Kempegowda Station, Majestic | Operating route | Purple, Green | 12.97571 | 77.57288 | 5 | Sowrashtrapet (locality, 355 m); Balepet (neighbourhood, 439 m); Sultanpete (neighbourhood, 651 m); Chikkapete (suburb, 726 m); Gandhinagar (suburb, 792 m) |
| Nagasandra | Operating route | Green | 13.04795 | 77.50014 | 2 | Rukmini Nagara (neighbourhood, 645 m); Nagasandra (suburb, 777 m) |
| Nallurahalli | Operating route | Purple | 12.97664 | 77.72488 | 1 | EPIP Zone (suburb, 174 m) |
| National College | Operating route | Green | 12.95053 | 77.57369 | 3 | VV Puram (quarter, 395 m); Shankarapuram (neighbourhood, 447 m); Gandhi Bazaar (neighbourhood, 620 m) |
| Pantharapalya - Nayandahalli | Operating route | Purple | 12.94167 | 77.52512 | 3 | Pantarapalya (neighbourhood, 392 m); Nayandahalli (neighbourhood, 461 m); Pramodha Layout (neighbourhood, 678 m) |
| Pattanagere | Operating route | Purple | 12.9243 | 77.49828 | 1 | Dubasi Palya (neighbourhood, 605 m) |
| Pattandur Agrahara | Operating route | Purple | 12.98764 | 77.73777 | 0 | None in this OSM place-node extract |
| Peenya | Operating route | Green | 13.03302 | 77.5332 | 1 | Peenya (suburb, 637 m) |
| Peenya Industry | Operating route | Green | 13.03632 | 77.52549 | 1 | Peenya (suburb, 425 m) |
| Ragigudda | Operating route | Yellow | 12.91708 | 77.5883 | 7 | DK Naik Nagar (neighbourhood, 114 m); Marenahalli (quarter, 387 m); Jayanagar 9th Block (quarter, 466 m); LIC Colony (neighbourhood, 534 m); Jayanagar 5th Block (quarter, 603 m); JP Nagar 2nd Phase (quarter, 632 m); KSRTC Layout (neighbourhood, 734 m) |
| Rajajinagar | Operating route | Green | 13.00052 | 77.54966 | 10 | Ketamaranahalli (neighbourhood, 254 m); West of Chord Road 2nd Stage (neighbourhood, 297 m); Rajajinagar 1st Block (neighbourhood, 332 m); Mahalakshmipuram (quarter, 401 m); Nagapura (neighbourhood, 419 m); Rajajinagara 1st N Block (neighbourhood, 592 m); Mariappanapalya (neighbourhood, 637 m); Indiranagar (neighbourhood, 668 m); Manjunath Nagar (neighbourhood, 751 m); Rajajinagar 2nd Block (neighbourhood, 762 m) |
| Rajarajeshwari Nagar | Operating route | Purple | 12.9366 | 77.51968 | 2 | Ideal Homes Layout (neighbourhood, 728 m); Javaranadoddi (neighbourhood, 738 m) |
| Rashtreeya Vidyalaya Road | Operating route | Green, Yellow | 12.92158 | 77.5802 | 4 | Jayanagar 8th Block (quarter, 347 m); Jayanagar 5th Block (quarter, 409 m); Jayanagar 7th Block (quarter, 519 m); Jayanagar 4th Block (quarter, 661 m) |
| Sandal Soap Factory | Operating route | Green | 13.01465 | 77.55398 | 2 | Ashokapuram (neighbourhood, 691 m); Milk Colony (neighbourhood, 754 m) |
| Seetharampalya | Operating route | Purple | 12.98086 | 77.70879 | 2 | Channama Layout (neighbourhood, 463 m); Ashraya Layout (neighbourhood, 660 m) |
| Silk Institute | Operating route | Green | 12.86173 | 77.52995 | 0 | None in this OSM place-node extract |
| Singasandra | Operating route | Yellow | 12.88082 | 77.64485 | 3 | Singasandra (quarter, 452 m); Wellington Paradise Layout (neighbourhood, 506 m); AECS Layout, A block (neighbourhood, 638 m) |
| Singayyanapalya | Operating route | Purple | 12.99654 | 77.69272 | 8 | B Chikkanna Layout (neighbourhood, 483 m); RHB Colony (neighbourhood, 549 m); Maheshwari Nagar (neighbourhood, 571 m); ITI Industrial Estate (neighbourhood, 610 m); Mahadevapura (suburb, 673 m); Kamdhenu Nagar (neighbourhood, 681 m); Saraswathi Nagar (neighbourhood, 716 m); Justice Bheemiah Layout (neighbourhood, 736 m) |
| Sir M. Visvesvaraya Stn., Central College | Operating route | Purple | 12.97452 | 77.58422 | 2 | Gandhinagar (suburb, 540 m); Cubbonpet (neighbourhood, 678 m) |
| South End Circle | Operating route | Green | 12.93826 | 77.58006 | 4 | Jayanagar 2nd Block (quarter, 334 m); Jayanagar 3rd Block (quarter, 586 m); Kankanpalya (neighbourhood, 605 m); Basavanagudi (suburb, 626 m) |
| Sri Balagangadharanatha Swamiji Station, Hosahalli | Operating route | Purple | 12.97429 | 77.54562 | 4 | Dasarahalli (neighbourhood, 556 m); Cholourpalya (neighbourhood, 586 m); RPC Layout (neighbourhood, 593 m); Hosahalli (neighbourhood, 658 m) |
| Sri Sathya Sai Hospital | Operating route | Purple | 12.98119 | 77.72754 | 2 | EPIP Zone (suburb, 458 m); Pattanduru Agrahara (suburb, 706 m) |
| Srirampura | Operating route | Green | 12.99653 | 77.5632 | 5 | Maruthi Extension (neighbourhood, 125 m); Prakash Nagar (neighbourhood, 185 m); Valluvarpuram (neighbourhood, 583 m); Gayatri Nagar (neighbourhood, 598 m); Sriramapuram (quarter, 619 m) |
| Swami Vivekananda Road | Operating route | Purple | 12.98593 | 77.6449 | 8 | New Baiyyappanahalli Extension (neighbourhood, 157 m); Ramaswamy Layout (neighbourhood, 398 m); Binnamangala (neighbourhood, 410 m); Hutting Colony (neighbourhood, 529 m); Michaelpalya (neighbourhood, 568 m); BM Kaval (neighbourhood, 603 m); Subedar Garden (neighbourhood, 675 m); Old Binnamangala (neighbourhood, 794 m) |
| Thalaghattapura | Operating route | Green | 12.87141 | 77.5384 | 3 | Thalaghattapura (neighbourhood, 345 m); Judicial Layout (neighbourhood, 616 m); Ganigarapalya (neighbourhood, 752 m) |
| Trinity | Operating route | Purple | 12.97302 | 77.61702 | 5 | Craig Park Layout (neighbourhood, 223 m); Hanumanthappa Layout (neighbourhood, 374 m); Yellappa Chetty Layout (neighbourhood, 524 m); Someshwarpura (neighbourhood, 699 m); Corporation Quarters (neighbourhood, 725 m) |
| Vajarahalli | Operating route | Green | 12.87744 | 77.54474 | 1 | Vajrahalli (quarter, 314 m) |
| Vijayanagar | Operating route | Purple | 12.97096 | 77.5374 | 10 | M C Layout (neighbourhood, 323 m); Binny Layout (neighbourhood, 358 m); Vijaya Nagar (suburb, 551 m); Central Excise Layout (neighbourhood, 578 m); PF Layout (neighbourhood, 596 m); Hosahalli (neighbourhood, 619 m); Thimanahalli (neighbourhood, 660 m); Govindaraj Nagara (quarter, 704 m); NHCS Layout (neighbourhood, 707 m); Marenahalli (neighbourhood, 772 m) |
| Whitefield (Kadugodi) | Operating route | Purple | 12.99574 | 77.75795 | 1 | Kadugodi (suburb, 454 m) |
| Yelachenahalli | Operating route | Green | 12.89605 | 77.57012 | 2 | Yelachenahalli (neighbourhood, 214 m); Eshwara Layout (neighbourhood, 793 m) |
| Yeshwantpur | Operating route | Green | 13.02327 | 77.54988 | 1 | Yeswanthpur (suburb, 368 m) |
| Agara Lake | Under construction | Blue | 12.92068 | 77.64373 | 4 | Agara (neighbourhood, 484 m); Sector 4 (quarter, 720 m); Jakkasandra (neighbourhood, 779 m); Sector 1 (quarter, 795 m) |
| Airport City | Under construction | Blue | 13.19835 | 77.68699 | 0 | None in this OSM place-node extract |
| Bagalur Cross | Under construction | Blue | 13.11936 | 77.60982 | 1 | Palanahalli (neighbourhood, 624 m) |
| Bagmane DRDO Sports Complex | Under construction | Blue | 12.98592 | 77.69076 | 5 | Shivaganga Layout (neighbourhood, 408 m); Mahadevapura (suburb, 602 m); Saraswathi Nagar (neighbourhood, 629 m); Maheshwari Nagar (neighbourhood, 652 m); B Chikkanna Layout (neighbourhood, 732 m) |
| Cantonment | Under construction | Pink | 12.99179 | 77.60622 | 3 | Cleveland Town (quarter, 635 m); Benson Town (quarter, 676 m); Shivajinagar (suburb, 702 m) |
| Central Silk Board | Under construction | Blue | 12.9174 | 77.62347 | 8 | MCHS Colony (neighbourhood, 383 m); Dollar Scheme Colony (neighbourhood, 434 m); N. G. R. Layout (neighbourhood, 616 m); BTM 2nd Stage (neighbourhood, 619 m); Sidhartha Colony (neighbourhood, 716 m); Jai Bheema Nagar (neighbourhood, 739 m); Roopena Agrahara (neighbourhood, 753 m); Koramangala 2nd Block (neighbourhood, 779 m) |
| Dairy Circle | Under construction | Pink | 12.94122 | 77.60243 | 4 | Lakkasandra (quarter, 370 m); Eramma Layout (neighbourhood, 493 m); Chinnayanapalya (neighbourhood, 762 m); Adugodi (quarter, 766 m) |
| Doddajala | Under construction | Blue | 13.18838 | 77.64463 | 0 | None in this OSM place-node extract |
| Doddanakundi | Under construction | Blue | 12.97561 | 77.69703 | 7 | Doddanekundi (quarter, 481 m); Ambedkar Colony (neighbourhood, 561 m); Wasa Layout (neighbourhood, 570 m); Shamanna Reddy Layout (neighbourhood, 698 m); Karthik Nagar (quarter, 750 m); Ferns Habitat (neighbourhood, 757 m); LRDE Layout (neighbourhood, 789 m) |
| Embassy Tech Village Kadubeesanahalli | Under construction | Blue | 12.93221 | 77.68755 | 2 | Kariyammana Agrahara (neighbourhood, 550 m); Devarabeesanahalli (quarter, 631 m) |
| HBR Layout | Under construction | Blue | 13.03252 | 77.62982 | 5 | HBR Layout (suburb, 197 m); HBR Layout 4th Block (quarter, 212 m); Grace Town (neighbourhood, 512 m); HBR Layout 3rd Block (quarter, 537 m); HBR Layout 5th Block (quarter, 561 m) |
| Hebbal | Under construction | Blue | 13.04395 | 77.59316 | 2 | Arkavathy Layout 22nd Block (locality, 584 m); Hebbal (suburb, 652 m) |
| Horamavu | Under construction | Blue | 13.01739 | 77.65956 | 1 | Vijaya Bank Colony (neighbourhood, 205 m) |
| HRBR Layout | Under construction | Blue | 13.02257 | 77.64737 | 7 | Nanjappa Garden (neighbourhood, 343 m); HRBR Layout 1st Block (quarter, 384 m); Bank Avenue Colony (neighbourhood, 588 m); CNR Layout (neighbourhood, 629 m); Malappa Layout (neighbourhood, 647 m); Babusabpalya (neighbourhood, 725 m); Kalyan Nagar (suburb, 763 m) |
| HSR Layout | Under construction | Blue | 12.91646 | 77.63315 | 7 | Sector 5 (quarter, 274 m); Sector 6 (quarter, 283 m); Teacher's Colony (neighbourhood, 283 m); Venkatpura (neighbourhood, 693 m); MCHS Colony (neighbourhood, 712 m); MCHS Colony (neighbourhood, 731 m); Sector 7 (quarter, 748 m) |
| Hulimavu | Under construction | Pink | 12.88084 | 77.59585 | 1 | Arekere (quarter, 709 m) |
| Ibbaluru | Under construction | Blue | 12.92103 | 77.66315 | 2 | Iblur (quarter, 170 m); Ambalipura (neighbourhood, 599 m) |
| IIMB | Under construction | Pink | 12.89582 | 77.59962 | 2 | Panduranga Nagar (neighbourhood, 486 m); Govinda Reddy Layout (neighbourhood, 706 m) |
| ISRO | Under construction | Blue | 12.96898 | 77.70112 | 5 | LRDE Layout (neighbourhood, 118 m); Karthik Nagar (quarter, 163 m); Wasa Layout (neighbourhood, 369 m); Doddanekundi (quarter, 566 m); Ambedkar Colony (neighbourhood, 677 m) |
| Jakkur Cross | Under construction | Blue | 13.07005 | 77.59312 | 1 | Byatarayanapura (neighbourhood, 398 m) |
| Jayadeva Interchange | Under construction | Pink | 12.91693 | 77.59993 | 5 | BHBCS Layout (neighbourhood, 209 m); SFHS Layout (neighbourhood, 360 m); Gurappana Palya (neighbourhood, 563 m); MICO Layout (neighbourhood, 606 m); JP Nagar 3rd Phase (quarter, 624 m) |
| JP Nagar 4th Phase | Under construction | Pink | 12.90985 | 77.60009 | 7 | JP Nagar 3rd Phase (quarter, 344 m); NS Palya (neighbourhood, 383 m); SFHS Layout (neighbourhood, 507 m); MICO Layout (neighbourhood, 531 m); BHBCS Layout (neighbourhood, 596 m); JP Nagar 4th Phase (quarter, 637 m); KSRTC Layout (neighbourhood, 789 m) |
| Kadugundanahalli | Under construction | Pink | 13.02996 | 77.62073 | 3 | Rashad Nagar (neighbourhood, 379 m); Govindapura (neighbourhood, 472 m); Shampura (neighbourhood, 784 m) |
| Kalena Agrahara | Under construction | Pink | 12.87148 | 77.59368 | 2 | Nobo Nagar (neighbourhood, 483 m); Kalena Agrahara (neighbourhood, 686 m) |
| Kalyan Nagar | Under construction | Blue | 13.02621 | 77.63807 | 7 | HRBR Layout 2nd Block (quarter, 322 m); Palm Grove (neighbourhood, 366 m); HRBR Layout 3rd Block (quarter, 386 m); Kalyan Nagar (suburb, 515 m); Chelekere (neighbourhood, 552 m); Meghanapalya (neighbourhood, 582 m); Grace Town (neighbourhood, 643 m) |
| Kasturinagara | Under construction | Blue | 13.00803 | 77.66263 | 4 | B Channasandra (neighbourhood, 331 m); Kasturi Nagar (quarter, 466 m); Doctors Layout (neighbourhood, 567 m); Kasturi Nagar 2nd Stage (neighbourhood, 738 m) |
| Kempapura | Under construction | Blue | 13.0437 | 77.60516 | 4 | Vishwanath Nagenahalli (quarter, 577 m); Jogappa Layout (neighbourhood, 663 m); Coffee Board Layout (neighbourhood, 743 m); Kanaka Nagar (neighbourhood, 774 m) |
| KIAL Terminals | Under construction | Blue | 13.19818 | 77.71291 | 0 | None in this OSM place-node extract |
| Kodibisanahalli | Under construction | Blue | 12.94521 | 77.69811 | 1 | Kaadubeesanahalli (quarter, 647 m) |
| Kodigehalli | Under construction | Blue | 13.05674 | 77.59368 | 1 | Amruthnagar (neighbourhood, 481 m) |
| Krishnarajapuram | Under construction | Blue | 13.00008 | 77.67737 | 2 | Darga Mohalla (neighbourhood, 458 m); Udaya Nagar (neighbourhood, 675 m) |
| Lakkasandra | Under construction | Pink | 12.94949 | 77.60304 | 7 | Chinnayanapalya (neighbourhood, 289 m); JK Pura (neighbourhood, 329 m); Vinayaka Nagara (neighbourhood, 412 m); Eramma Layout (neighbourhood, 428 m); Gajendra Nagara (neighbourhood, 615 m); Wilson Garden (quarter, 676 m); Lakkasandra (quarter, 784 m) |
| Langford Town | Under construction | Pink | 12.95623 | 77.60586 | 6 | Langford Town (neighbourhood, 303 m); Bethel Layout (neighbourhood, 385 m); Gajendra Nagara (neighbourhood, 670 m); Pudupadacheri (neighbourhood, 708 m); JK Pura (neighbourhood, 775 m); Anepalya (neighbourhood, 798 m) |
| Mahatma Gandhi Road | Under construction | Pink | 12.97624 | 77.60838 | 3 | Tasker Town (neighbourhood, 518 m); Commercial Street Market (neighbourhood, 697 m); Ashok Nagar (quarter, 762 m) |
| Marathahalli | Under construction | Blue | 12.95796 | 77.70133 | 12 | Ramanjaneya Layout (locality, 175 m); Ashwath Nagar (neighbourhood, 197 m); Hemanth Nagar (locality, 338 m); Ananda Nagara (neighbourhood, 353 m); Marathahalli (suburb, 436 m); Ayappa Layout (locality, 466 m); Chinnappanahalli (neighbourhood, 497 m); P R Layout (neighbourhood, 587 m); Sanjay Nagar (neighbourhood, 591 m); Vivekananda Layout (locality, 615 m); MSR Layout (neighbourhood, 674 m); Gandhi Nagar (neighbourhood, 742 m) |
| Nagawara | Under construction | Pink | 13.04122 | 77.62502 | 3 | Nagavara (suburb, 444 m); Telecom Layout 10th Block (neighbourhood, 509 m); HBR Layout 5th Block (quarter, 584 m) |
| Nagawara | Under construction | Blue | 13.03956 | 77.62477 | 3 | Nagavara (suburb, 266 m); HBR Layout 5th Block (quarter, 495 m); Telecom Layout 10th Block (neighbourhood, 566 m) |
| Pottery Town | Under construction | Pink | 13.00065 | 77.60943 | 8 | Pottery Town (neighbourhood, 180 m); Williams Town (neighbourhood, 334 m); SK Garden (neighbourhood, 509 m); Frazer Town (suburb, 572 m); Sagayapura (neighbourhood, 671 m); ITI Layout (neighbourhood, 700 m); Benson Town (quarter, 724 m); Cleveland Town (quarter, 772 m) |
| Prestige Bellandur | Under construction | Blue | 12.9278 | 77.68036 | 1 | Bellanduru (suburb, 392 m) |
| Rashtriya Military School Metro Station | Under construction | Pink | 12.96528 | 77.60695 | 7 | Arab Lines (neighbourhood, 94 m); Ashok Nagar (quarter, 525 m); Xavier Layout (neighbourhood, 557 m); Richmond Town (suburb, 612 m); Yellagondanpalya (neighbourhood, 676 m); Anglo-Indian Quarters (neighbourhood, 788 m); Victoria Layout (quarter, 794 m) |
| Saraswathi Nagar | Under construction | Blue | 12.99371 | 77.6855 | 7 | Kamdhenu Nagar (neighbourhood, 278 m); Saraswathi Nagar (neighbourhood, 458 m); B. Narayanapura (quarter, 488 m); Mahadevapura (suburb, 534 m); Maheshwari Nagar (neighbourhood, 608 m); B Chikkanna Layout (neighbourhood, 623 m); Shivaganga Layout (neighbourhood, 676 m) |
| Shivajinagar | Under construction | Pink | 12.98385 | 77.60204 | 3 | Shivajinagar (suburb, 414 m); Tasker Town (neighbourhood, 580 m); Commercial Street Market (neighbourhood, 731 m) |
| Tannery Road | Under construction | Pink | 13.00959 | 77.61395 | 6 | Periyar Nagar (neighbourhood, 204 m); Pillana Garden (neighbourhood, 381 m); Sagayapura (neighbourhood, 471 m); New Bagalur Layout (neighbourhood, 521 m); Postal and Telecom Colony (neighbourhood, 525 m); Richards Town (quarter, 684 m) |
| Tavarekere | Under construction | Pink | 12.9295 | 77.6005 | 6 | Rajanna Layout (locality, 415 m); Bismillah Nagar (neighbourhood, 471 m); NAL Layout (neighbourhood, 489 m); Tilak Nagar (neighbourhood, 662 m); Balaji Layout (neighbourhood, 769 m); RBI Colony (locality, 778 m) |
| Veerannapalya | Under construction | Blue | 13.041 | 77.61805 | 3 | Virannapalya (neighbourhood, 512 m); Nagavara (suburb, 719 m); Govindapura (neighbourhood, 789 m) |
| Venkateshapura | Under construction | Pink | 13.01731 | 77.61802 | 5 | Kushal Nagar (neighbourhood, 355 m); Kadugondanahalli (quarter, 537 m); Postal and Telecom Colony (neighbourhood, 543 m); HRBR Layout 1st Block (quarter, 753 m); Pillana Garden (neighbourhood, 765 m) |
| Yelahanka | Under construction | Blue | 13.10185 | 77.60021 | 2 | Yelahanka (suburb, 437 m); Gandhinagar (neighbourhood, 635 m) |

## Frequently asked questions

### Is 800 m a walking distance?

It is a straight-line distance from the station node to the place node, on a sphere of radius 6,371,000 m. It is not the length of a footpath and not a time.

### How many stations are on the map?

Eighty-two on Purple, Green or Yellow route relations, and 47 tagged under construction. Proposed Orange and Red nodes in the same OSM extract are not included.

### Why does one station name appear twice?

Nagawara has a Pink under-construction node and a Blue under-construction node, 186 m apart, so both are listed. Jayadeva Hospital (Yellow, operating) and Jayadeva Interchange (Pink, under construction) are different nodes.

### What if my area is not in the locality cell?

The cell only contains OSM place nodes inside 800 m. A real neighbourhood with no such node, or a node just beyond 800 m, will be missing. That is a gap in the extract, not a finding that the area is far from the station.

### Which line is a station on?

For operating stations, the line is the route relation: Purple, Green, Yellow, or both where the station is on two. For under-construction stations, the line is the colour tag on the node.

### Does a station inside 800 m change the guidance value?

This page does not calculate a price or a guidance value. The 2023 guidance-value notification does not have a station-distance column. Our [note on guidance value near metro roads](https://acrenkey.com/insights/metro-uplift-in-bengaluru-guidance-value-near-bmrcl-stations/) is about road rows in that gazette, not about this 800 m list.

## Talk it through with acre&key

If you are choosing between two stations, bring the locality names from this table and acre&key will read them with the rest of the papers: the exit you would actually use, the line's status, and the approval file.

## Sources

Checked 20 Oct 2026.

1. OpenStreetMap contributors, station nodes, route relations and place nodes, extracted 20 Oct 2026. Copyright: https://www.openstreetmap.org/copyright
2. Open Database Licence for that database: https://opendatacommons.org/licenses/odbl/1-0/
3. The operating route relations used are the OSM relations named Purple, Green and Yellow with `network=Namma Metro`. Under-construction nodes are those with `construction=station` and "(u/c)" in the name.
4. For government status of lines still being built, see our metro lines guide and the sources on that page: https://acrenkey.com/blogs/bengaluru-metro-lines-2026-status-of-every-line-for-homebuyers/

## Suggested images

1. Hero and card, 1200x675 WebP, at assets/img/namma-metro-walk-map-localities-within-800-m.webp. Alt: "Map of Namma Metro stations in Bengaluru with localities inside an 800 metre circle"
