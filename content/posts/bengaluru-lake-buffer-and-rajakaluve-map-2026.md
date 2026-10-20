---
title: "Bengaluru Lake Buffer and Rajakaluve Map (2026)"
meta_description: "Bengaluru lake buffer map: KSRSAC tanks, BBMP lake points and primary and secondary drains, the 2026 buffer table, and how to check one plot."
primary_keyword: "bengaluru lake buffer map"
slug: "bengaluru-lake-buffer-and-rajakaluve-map-2026"
date_modified: "2026-10-20"
date_published: "2026-10-20"
dataset_name: "Bengaluru tanks, lake points and stormwater-drain bands"
dataset_description: "KSRSAC tank polygons and primary and secondary drain lines published via OpenCity, BBMP lake points, and bands drawn 50 m and 25 m from those drain lines. Revenue-area lake buffers are not drawn."
dataset_distribution: "assets/data/bengaluru-lake-buffer-map.geojson"
dataset_csv: "assets/data/bengaluru-bbmp-lakes.csv"
dataset_csv_2: "assets/data/bengaluru-ksrsac-named-tanks.csv"
include_howto: "yes"
---

# Bengaluru lake buffer and rajakaluve map for homebuyers (2026)

**Short answer:** The map below draws KSRSAC tank outlines and BBMP lake points, plus primary and secondary stormwater drains with a 50 m and a 25 m band. It does not draw a lake buffer. Under Karnataka Act 19 of 2026 the lake buffer is 0 m to 30 m from the revenue boundary, and the width depends on the tank's area in the revenue record, which these map files do not carry.

> **Key takeaways**
> - **Lake buffer in force:** Karnataka Act 19 of 2026, gazette dated 18 Feb 2026, sets the buffer from the tank's revenue boundary by area: 0 m, 1 m, 3 m, 6 m, 12 m, 24 m or 30 m.
> - **Drain buffer after the 2019 judgment:** the Supreme Court set aside the NGT's citywide wider buffers of 4 May 2016, except the direction against respondent Nos. 9 and 10. The judgment records the RMP-2015 drain buffers as 50 m, 25 m and 15 m from the middle of primary, secondary and tertiary drains.
> - **What is drawn:** 1,356 KSRSAC tank polygons (173 named), 207 BBMP lake points, 163 primary drain features and 870 secondary drain features.
> - **What is not drawn:** a lake buffer. The Act uses revenue area. The shape-area field in the KSRSAC file is not that figure, so it is not used here.
> - A lawyer has to apply the buffer to a specific survey number. This page is a screen for the city, not a measurement of your plot.

The files behind the map are public. Tanks and drains come from KSRSAC layers republished by OpenCity. The lake points come from a BBMP list. The coloured bands are a geometry we calculated from those drain lines and from the widths recorded in the Supreme Court judgment. They are not a surveyed revenue boundary.

<div class="ak-map-wrap">
<div id="lake-map" class="ak-map" data-root="../" data-geo="../assets/data/bengaluru-lake-buffer-map.geojson" data-legend="lake-legend" role="region" aria-label="Map of tanks, drains and drain bands in Bengaluru"></div>
<script type="application/json" id="lake-legend">[{"id":"primary-buffer","label":"50 m primary band","on":true},{"id":"secondary-buffer","label":"25 m secondary band","on":true},{"id":"tank","label":"KSRSAC tank","on":true},{"id":"tank-island","label":"Tank island","on":false},{"id":"primary","label":"Primary drain","on":true},{"id":"secondary","label":"Secondary drain","on":true},{"id":"bbmp-lake","label":"BBMP lake point","on":true}]</script>
<p class="ak-map-note">Scroll to load the map. It needs JavaScript and OpenStreetMap tiles. Without JavaScript, use the tables and the GeoJSON download. Zoom with the buttons. The layer control sits at the top right.</p>
<script src="../assets/ak-map.js" defer></script>
</div>

Downloads: [GeoJSON](../assets/data/bengaluru-lake-buffer-map.geojson), [BBMP lake points (CSV)](../assets/data/bengaluru-bbmp-lakes.csv), [named KSRSAC tanks (CSV)](../assets/data/bengaluru-ksrsac-named-tanks.csv).

## What each layer is

| Layer | Count in the file | What the file actually is |
|---|---|---|
| KSRSAC tanks | 1,356 polygons | Bengaluru Urban tanks layer. 31 of them have LULC_Desc_2 set to Island. 173 polygons have a name. |
| BBMP lake points | 207 rows | Point list. 205 rows have a latitude and longitude. Mangammanahalli lake and Kenchanapura lake have a blank coordinate in the file, so they are in the table and not on the map. |
| Primary drains | 163 features | KSRSAC primary stormwater drains for the former BBMP area. |
| Secondary drains | 870 features | KSRSAC secondary stormwater drains for the same area. |
| Primary band | 1 dissolved polygon | 50 m either side of the primary lines, measured in UTM zone 43N, then simplified. |
| Secondary band | 1 dissolved polygon | 25 m either side of the secondary lines, on the same method. |

Primary features store a field named SHAPE_Leng. The sum of that field, rounded to two decimal places, is 328,464.92. On the first feature the stored value is 7,536.37574677, and the same line measures 7,536.38 m in UTM zone 43N, which is why the field is read as metres. Secondary features store Shape_Leng. That sum, rounded the same way, is 438,813.98.

Tertiary drains are not on this map. The OpenCity file for them is a separate KML of about 25 MB. The judgment records a 15 m tertiary buffer from the middle. The file is linked from the [stormwater drains dataset](https://data.opencity.in/dataset/bengaluru-stormwater-drains-maps).

Some KSRSAC names are repeated on different polygons, including Hoskote Kere and Thattekere. The table keeps the object id so those rows stay distinct. The centroid is the representative point of the simplified outline, not a revenue-survey stone.

## Which buffer applies after the Supreme Court and the 2026 Act?

Two different rules are in play, and they were set by different instruments.

**Lakes and tanks.** Karnataka Act 19 of 2026 amends section 12 of the Karnataka Tank Conservation and Development Authority Act, 2014. It was published in the Karnataka Gazette Extraordinary on 18 Feb 2026, received the Governor's assent on 16 Feb 2026, and came into force at once. The substituted section 12(3) bars construction and commercial, recreational or industrial activity inside the buffer in the table, measured from the revenue boundary of the tank. The exception is approved public utilities (roads, bridges, electrical lines, water-supply lines, underground drainage, a jack well or pump house, an STP, an ISPS, a wet well, an aqueduct and allied works) with the Authority's prior approval, and without blocking inflow or outflow. A further clause says the state pollution board's siting guidelines for new industries prevail over that clause for those industries.

| Tank area | Buffer from the revenue boundary |
|---|---|
| Up to 0.05 acre | 0 m |
| Above 0.05 acre to 0.10 acre | 1 m |
| Above 0.10 acre to 1 acre | 3 m |
| Above 1 acre to 10 acres | 6 m |
| Above 10 acres to 25 acres | 12 m |
| Above 25 acres to 100 acres | 24 m |
| Above 100 acres | 30 m |

Source: the table in Karnataka Act 19 of 2026. The [gazette copy on OpenCity](https://data.opencity.in/dataset/2a2c0701-853e-4db3-b1d4-06ee8674c628/resource/ffff8ed9-228d-42a2-a596-3b4c06a8d726/download/lake-tank-buffer.pdf) and the [bill as passed](https://kla.kar.nic.in/council/house/bills/156/33E.pdf) carry the same table.

**Drains.** On 5 Mar 2019, in Mantri Techzone Pvt. Ltd. v. Forward Foundation, the Supreme Court set aside direction No. (1) of the National Green Tribunal's order of 4 May 2016, except the direction issued against respondent Nos. 9 and 10. That NGT direction had required 75 m from the periphery of lakes, 50 m from the edge of primary rajakaluves, 35 m from the edge of secondary rajakaluves and 25 m from the edge of tertiary rajakaluves, as a general rule. The judgment records what RMP-2015 itself provided: 50 m from the middle of a primary rajakaluve, 25 m from the middle of a secondary, and 15 m from the middle of a tertiary, set against a 30 m lake buffer in the master plan.

The 2026 Act rewrites the tank buffer. Its text does not rewrite the drain buffers. The bands on this map follow the RMP widths as the judgment records them: 50 m and 25 m either side of the mapped line, which is the "from the middle" reading. A line on a map is not the surveyed edge of a drain. If a building sits near the band, the approved plan and a lawyer decide whether the measurement is from the middle or the edge.

The NGT took suo motu notice of the state's move to reduce lake buffers and issued notices on 8 Aug 2025, before Act 19 of 2026 was notified ([The Indian Express](https://indianexpress.com/article/cities/bangalore/ngt-takes-suo-motu-cognisance-of-buffer-zone-reduction-around-lakes-karnataka-10213014/)). In the sources read for this page, that report does not show a citywide stay of the Act. A later order can still change the answer for one lake. Ask a lawyer to check the lake you are buying beside.

Our [lake and rajakaluve checklist](https://acrenkey.com/blogs/flood-risk-lake-buffers-and-rajakaluve-checks-before-you-buy/) walks through the same rules with worked examples. The [flood-prone points page](https://acrenkey.com/blogs/bengaluru-flood-prone-areas-map-from-ksndmc-data/) is a different list: road points that flood, not a buffer line.

## Why the map does not colour a lake buffer

Act 19 of 2026 measures the lake buffer from the revenue boundary, and the width depends on area in acres from the revenue record. The KSRSAC polygon is a mapped tank outline. The BBMP row is a point. Neither file contains the revenue area or the revenue boundary.

The KSRSAC file does contain a shape-area number. Using that number to pick a row in the Act's table would treat a mapped outline as the revenue extent. This page does not do that. A lake can still be looked up by name, and the area has to come from the RTC.

For a named tank, the practical path is: find it on the map, note the name and the object id, then pull the survey extent from [Bhoomi](https://landrecords.karnataka.gov.in/) and the lake survey map on [Revenue Maps Online](https://landrecords.karnataka.gov.in/service3/). The same portal has rajakaluve survey details.

## How to check a plot or project

Use the map to see whether a tank or a primary or secondary drain is near the site. Then leave the map. The steps below are the ones that produce a document a lawyer can read.

### Find the tank or drain on this map
Search the BBMP table or the named-tank table for the water body you were shown. If it is there, note the latitude and longitude, or the object id. If the site is in an area with no named tank, turn the drain layers on and see whether a primary or secondary line passes the block. A miss on this map is not a clearance. The files do not cover every drain outside the former BBMP extent, and unnamed tanks are drawn but not listed by name.

### Get the revenue area and the revenue boundary
Ask for the tank's survey number and the area in acres from the RTC. The buffer row in the 2026 table is meaningless without that area. The distance that matters is from the revenue boundary, not from the water's edge on a phone map.

### Read the buffer off the 2026 table
Match the acre figure to one row. Write down the metres. If the plan was approved before 18 Feb 2026, ask which buffer the approval used. The master plan figure recorded in the 2019 judgment was 30 m around lakes. The Act now uses the size table. Which one binds an older approval is a legal question, not a map question.

### Ask for the drain on the approved plan
For a rajakaluve, ask the builder or the seller to mark the primary, secondary or tertiary drain and the buffer line on the sanctioned plan. Compare that sheet with the primary and secondary lines here. This map's band is 50 m or 25 m from the KSRSAC line. The plan may measure from the edge. Those are different lines.

### Pull the survey sheets
Lake survey maps and rajakaluve survey details are on Revenue Maps Online, by district, taluk, hobli and village. A layout brochure is not one of those sheets.

### Walk the site after heavy rain
The buffer is a building line. It does not say whether the basement took water last monsoon. Look at the ramp, the plinth and the road you would actually use. Our [flood-points page](https://acrenkey.com/blogs/bengaluru-flood-prone-areas-map-from-ksndmc-data/) is the list of vulnerable spots, where a spot has been published.

### Stop if nobody can show the boundary
If there is no RTC area, no survey sheet and no buffer line on the sanctioned plan, do not treat the colour on this map as a yes. The [legal checks guide](https://acrenkey.com/blogs/bengaluru-property-legal-checks-from-title-to-oc/) is the longer paper list. The buffer question still goes to a property lawyer before any token.

## BBMP lake points

The name in the source file sometimes ends with a zone, written with an older English name of the city. This table splits that suffix off. The zone column is Central, North, South, East, North Additional, or East taluk. Fifty-five rows had such a suffix. The other 152 did not, so the zone cell is empty. The CSV column `source_name` keeps the field exactly as stored.

One hundred and thirty-eight coordinate strings in the file had lost the N or E letter to a bad character. Those were read as north or east because every latitude in the file is 12 or 13 degrees and every longitude is 77 or 78 degrees. Strings that still had the letter were read from the letter. Mangammanahalli lake and Kenchanapura lake have no coordinate in the file.

| Sl. no. | Lake name | Zone in the source field | Latitude | Longitude |
|---|---|---|---|---|
| 1 | Ulsoor | Central | 12.982806 | 77.619306 |
| 2 | Kelagina kere / Byrasnadra |  | 12.978444 | 77.662056 |
| 3 | Kaggadasapura Lake |  | 12.9815 | 77.670472 |
| 4 | Melina kere byrasandra (DRDO) |  | 12.97925 | 77.655389 |
| 5 | B. Channasandra Lake |  | 13.006389 | 77.661722 |
| 6 | Channasandra Lake |  | 13.012111 | 77.65325 |
| 7 | Malagala (Balaiahna Lake) | North | 12.978167 | 77.527917 |
| 8 | Nayadahalli Lake | South | 12.940139 | 77.521083 |
| 9 | Sankey tank | Central | 13.0105 | 77.573917 |
| 10 | Gowdana Palya Lake |  | 12.907639 | 77.556278 |
| 11 | Yediyur Lake | South | 12.933361 | 77.576694 |
| 12 | Deepanjali lake | South | 12.949942 | 77.531292 |
| 13 | Kempambudhi Lake | North | 12.952306 | 77.559889 |
| 14 | Mesthripalya lake |  | 12.931611 | 77.625139 |
| 15 | Byrasandra lake / Chikkapete lake |  | 12.930083 | 77.595639 |
| 16 | Dasarahalli (Chokkasandra) Lake | North | 13.040667 | 77.511417 |
| 17 | Kamgondanahalli Kere | North | 13.067583 | 77.524778 |
| 18 | Bagalgunte Lake |  | 13.058222 | 77.500083 |
| 19 | Narasappanahalli Kere |  | 13.020778 | 77.494 |
| 20 | Abbigere Kere |  | 13.082139 | 77.529861 |
| 21 | Nelagedaranahalli lake |  | 13.0215 | 77.495778 |
| 22 | Mallasandra gudde lake |  | 13.014786 | 77.785331 |
| 23 | Halage vaderahalli Lake | South | 12.924167 | 77.514806 |
| 24 | J.P Park | North | 13.035083 | 77.550306 |
| 25 | Mallathahalli lake | North | 12.965056 | 77.494083 |
| 27 | Srigandadakaval |  | 12.984 | 77.500944 |
| 28 | Nagarabhavi Lake |  | 12.96519 | 77.508471 |
| 29 | Hosakerehalli lake |  | 12.927444 | 77.532861 |
| 30 | Herohalli Lake | North | 12.988583 | 77.489694 |
| 31 | Lingadeeranahalli (handrahalli) Lake | North | 13.002806 | 77.483528 |
| 32 | Handrahalli kere | North | 13.171389 | 77.538611 |
| 33 | Kodigehalli lake | North | 13.153889 | 77.491389 |
| 34 | Jogi kere | South | 12.863111 | 77.538389 |
| 35 | Ullala lake | North | 12.960972 | 77.480361 |
| 36 | H Gollahalli kere | South | 13.016389 | 77.743333 |
| 37 | Bayyapanapalya Kunte | South | 12.890833 | 77.710278 |
| 38 | Vishwaneedum Lake |  | 13.238889 | 77.619444 |
| 39 | Talghatapura Lake |  | 12.8825 | 77.7725 |
| 40 | Doddabidarakallu /Nagasandra kere |  | 13.043722 | 77.494778 |
| 41 | Gubbalalu Lake |  | 12.876111 | 77.540556 |
| 42 | Varahasandra Lake |  | 12.879556 | 77.492972 |
| 43 | Mangammanahalli lake |  |  |  |
| 44 | Lingadeeranahalli |  | 12.872139 | 77.514028 |
| 45 | Konasandra Lake |  | 13.019722 | 77.7375 |
| 46 | Chikkagowdanapaly lake |  | 13.11 | 77.524167 |
| 47 | Dubasipalay lake (Valagerahalli) |  | 13.163333 | 77.654722 |
| 48 | Mylasandra (Sunnakallu palya) lake |  | 12.852167 | 77.616111 |
| 49 | Busegowdana lake |  | 12.906417 | 77.495833 |
| 50 | Kengeri Lake |  | 12.916361 | 77.486778 |
| 51 | Dorekere |  | 12.902833 | 77.550139 |
| 52 | Uttarahalli Lake / Bandgalore South |  | 12.907833 | 77.541167 |
| 53 | Singasandra | South | 12.882389 | 77.645278 |
| 54 | Parappana Agrahara | South | 12.879028 | 77.660833 |
| 55 | Kudlu Chikka kere / Anekal taluk |  | 13.039444 | 77.738333 |
| 56 | Kudlu doddakere / Anekal |  | 13.300278 | 77.6725 |
| 57 | Kodige Singasandra Lake |  | 13.076389 | 77.782778 |
| 58 | Basapura Lake-1 | South | 12.926389 | 77.891944 |
| 59 | Annappanakere / Yelchenahalli Lake |  | 12.899167 | 77.565111 |
| 60 | Kalena Agrahara Lake |  | 12.865417 | 77.589667 |
| 61 | Bheemana Katte |  | 12.915167 | 77.528667 |
| 62 | Begur Lake |  | 12.874722 | 77.629972 |
| 63 | Gottigere |  | 12.852722 | 77.589444 |
| 64 | Subramanyapura lake |  | 12.896222 | 77.542806 |
| 65 | Anjanapura Lake / Alahalli |  | 12.867083 | 77.565722 |
| 66 | Puttenahalli/ Byraweshwara nagara Chunchaghatta kere |  | 12.88775 | 77.575194 |
| 67 | Kothanuru lake |  | 12.873556 | 77.57975 |
| 68 | Basapura Lake-2 | South | 12.868583 | 77.643889 |
| 69 | Basavanapura Lake |  | 12.844556 | 77.589167 |
| 70 | Chikka Begur Lake |  | 12.884833 | 77.638778 |
| 71 | Hulimavu Lake |  | 12.870333 | 77.603361 |
| 72 | Konappana Agrahara lake |  | 12.878361 | 77.669167 |
| 73 | Kammanahalli Lake (Meenakshi Lake) |  | 12.854889 | 77.603528 |
| 74 | Vasanthapura kere |  | 12.89125 | 77.556778 |
| 75 | Devarakere |  | 12.897611 | 77.55425 |
| 76 | Yelenahalli Lake |  | 12.866583 | 77.614111 |
| 77 | Doddakallasandra Lake |  | 12.891389 | 77.568417 |
| 78 | Chowdeshwari layout Lake |  | 12.866194 | 77.661111 |
| 79 | Nyanappanahalli Lake |  | 12.87175 | 77.614639 |
| 80 | Subedaranakere |  | 12.52525 | 77.61325 |
| 81 | Chikkammanahalli Lake |  | 12.849167 | 77.602611 |
| 82 | Konanakunte Lake |  | 12.882 | 77.560972 |
| 83 | Swarnakunte gudda kere |  | 12.849167 | 77.602611 |
| 84 | Kembathahalli lake |  | 12.858056 | 77.57725 |
| 85 | Gattigerepalya (Sompura) lake |  | 12.874417 | 77.498417 |
| 86 | Arekere lake |  | 12.882722 | 77.598944 |
| 87 | Subbarayana lake |  | 13.065278 | 77.613889 |
| 88 | Kalyanikunte (Near Saibaba Temple) |  | 13.076111 | 77.621944 |
| 89 | Puttenahalli Lake (Next to Brigade Millenium) | South | 12.890222 | 77.587639 |
| 90 | Mangammana Palya Kaere |  | 12.902083 | 77.639139 |
| 91 | Ibblur Lake |  | 12.922111 | 77.666583 |
| 92 | Sarakki/Jaraganahalli/Puttenahalli Lake |  | 12.898833 | 77.579444 |
| 93 | Haralakunte Lake (Somasandrakere) |  | 13.149444 | 77.883611 |
| 94 | Venkogirao kere |  | 12.922611 | 77.641806 |
| 95 | Garveybhavipalya Lake |  | 12.89625 | 77.637056 |
| 96 | Madivala lake |  | 12.908167 | 77.617861 |
| 97 | Ambalipura Kelagina kere |  | 12.916944 | 77.664972 |
| 98 | Amblipura melina kere | East | 12.913306 | 77.663 |
| 99 | Kaigondanahalli Lake | East | 12.912611 | 77.6725 |
| 100 | Doddakanenahalli kere | East | 12.911722 | 77.693139 |
| 101 | Kasavanahalli lake | East | 12.904444 | 77.667778 |
| 102 | Haraluru kere | East | 12.895972 | 77.662611 |
| 103 | Sowl kere | East | 12.918333 | 77.679417 |
| 104 | Devarabeesanahalli Lake |  | 12.923 | 77.686889 |
| 105 | Junnasandra lake |  | 12.901944 | 77.680472 |
| 106 | Bhoganahalli Lake |  | 12.922778 | 77.699167 |
| 107 | Gunjur Palya kere |  | 12.920083 | 77.723028 |
| 108 | Gunjur mouji kere |  | 12.916806 | 77.739889 |
| 109 | Panathur lake |  | 12.931306 | 77.707028 |
| 110 | Chikkabelandur Lake |  | 12.912389 | 77.719111 |
| 111 | Gunjuru Karmelaram lake |  | 12.91775 | 77.710778 |
| 112 | Panthur lake |  | 12.9325 | 77.717139 |
| 113 | Munnekolalu kere | East | 12.960667 | 77.708333 |
| 114 | Chinnappanahalli | East | 12.965556 | 77.7075 |
| 115 | Kundalahalli Lake |  | 12.970444 | 77.719694 |
| 116 | Doddanekundi lake |  | 12.976083 | 77.685889 |
| 117 | Shilavanthana kere | East | 12.964389 | 77.742278 |
| 118 | Siddapura Lake |  | 12.958417 | 77.725389 |
| 119 | Nalluralli tank |  | 12.974472 | 77.73525 |
| 120 | Pattandur agrahara lake |  | 12.976028 | 77.745444 |
| 121 | Pattandur agrahara |  | 12.980139 | 77.73825 |
| 122 | Mahadevapura Lake |  | 12.98675 | 77.692611 |
| 123 | Mahadevapura Lake /East taluk |  | 12.987472 | 77.6925 |
| 124 | Vibhuthipura kere |  | 12.967444 | 77.676639 |
| 125 | Sitaram Palya |  | 12.981889 | 77.71275 |
| 126 | Garudachar Palya (Goshala) |  | 12.986778 | 77.697917 |
| 127 | Garudachar Palya Lake |  | 12.982361 | 77.713167 |
| 128 | Sadaramangala Lake |  | 12.999417 | 77.727528 |
| 129 | Hoodi kere |  | 12.999694 | 77.716556 |
| 130 | Hoodi Giddanakere |  | 12.986778 | 77.722278 |
| 131 | Jimkenahalli Lake |  | 13.026889 | 77.687 |
| 132 | Vijanapura kere | East | 13.009139 | 77.676556 |
| 133 | Sigehalli | East | 13.017361 | 77.713306 |
| 134 | Devsandra kere | East | 13.004861 | 77.694139 |
| 135 | Kowdenhalli lake | East | 13.012056 | 77.685194 |
| 136 | Challakere Lake /East taluk |  | 13.026361 | 77.644806 |
| 137 | Kalkere | East taluk | 13.047 | 77.6615 |
| 138 | Horamavu Lake |  | 13.023611 | 77.666583 |
| 139 | Hormavu Agara Lake |  | 13.036194 | 77.657833 |
| 140 | Nagareshwara-Nagenahalli Lake |  | 13.074889 | 77.642444 |
| 141 | Rampura kere |  | 13.047083 | 77.684889 |
| 143 | Bhattarahalli Lake |  | 13.024806 | 77.709056 |
| 144 | Vengaihna kere /K.R.Puram Tank |  | 13.243611 | 77.949722 |
| 145 | Gangashetty Lake |  | 13.004556 | 77.695389 |
| 146 | B. Narayanapura Lake |  | 12.996167 | 77.682556 |
| 147 | Cikkabasavana pura Lake |  | 13.009556 | 77.71175 |
| 148 | Kattigenahalli Kere-31 | North Additional | 13.114639 | 77.628472 |
| 149 | Thirumenahalli | North Additional | 13.092861 | 77.628444 |
| 150 | Agrahara Lake | North Additional | 13.089528 | 77.625194 |
| 151 | Kogilu lake | North Additional | 13.109639 | 77.6185 |
| 152 | Narasipura-20 | North Additional | 13.153056 | 77.686111 |
| 153 | Chokkanahalli lake |  | 13.084556 | 77.629333 |
| 154 | Jakkur lake (Sampigehalli Lake) |  | 13.085528 | 77.61125 |
| 155 | Narasipura-26 | North Additional | 13.234444 | 77.618333 |
| 156 | Doddabommasandra lake | North Additional | 13.064694 | 77.564028 |
| 157 | Kattigenahalli Kere-136 (Palanahalli lake) | North Additional | 13.115861 | 77.616472 |
| 158 | Rachenahalli lake | North Additional | 13.061694 | 77.614861 |
| 159 | Singapura Lake |  | 13.085222 | 77.538583 |
| 160 | Srinivasapura Kere |  | 13.105056 | 77.6265 |
| 161 | Venkatehpura Lake |  | 13.077694 | 77.623583 |
| 162 | Amruthahalli lake |  | 13.062028 | 77.599111 |
| 163 | Hebbala lake |  | 13.046778 | 77.586278 |
| 164 | Nagavara |  | 13.04525 | 77.609278 |
| 165 | Yelahanka kere | North Additional | 13.112917 | 77.594694 |
| 166 | Veerasagara lake | North Additional | 13.102139 | 77.556361 |
| 167 | Attur Lake | North Additional | 13.11125 | 77.561972 |
| 168 | Ramagondanahalli | North Additional | 13.116389 | 77.555167 |
| 169 | Allasandra lake | North Additional | 13.091611 | 77.586222 |
| 170 | Avalahalli | North Additional | 12.8655 | 77.566222 |
| 171 | Harohalli lake | North Additional | 12.989139 | 77.489722 |
| 172 | Bettahalli lake |  | 13.012444 | 77.454556 |
| 173 | Vaderahalli |  | 13.094111 | 77.5405 |
| 174 | Shivanahalli Lake |  | 13.09125 | 77.594722 |
| 175 | Puttenahalli lake |  | 13.111528 | 77.576972 |
| 176 | Bellahalli |  | 13.103944 | 77.643778 |
| 177 | Lakshmipura lake |  | 13.086222 | 77.530722 |
| 178 | Soolikere |  | 12.9515 | 77.459611 |
| 179 | Kannali lake |  | 12.966444 | 77.460389 |
| 180 | Kenchanapura lake |  |  |  |
| 181 | Sompura Lake |  | 12.874611 | 77.498 |
| 182 | Gandhinagar Hosakerehalli |  | 12.923278 | 77.480556 |
| 183 | Medi agrahara lake |  | 13.100028 | 77.5275 |
| 184 | Bhimana kuppe |  | 13.069722 | 77.455278 |
| 185 | Madavara lake |  | 13.051778 | 77.479361 |
| 186 | Chikkabasthi lake ( ramsandra lake) |  | 12.946786 | 77.47171 |
| 187 | Kannur |  | 13.099778 | 77.651444 |
| 188 | Chikkagubbi |  | 13.087389 | 77.664611 |
| 189 | Doddagubbi |  | 13.075417 | 77.674611 |
| 190 | Yarappanahalli |  | 13.087917 | 77.683222 |
| 191 | Kadusonnappanahalli |  | 13.102806 | 77.669222 |
| 192 | Vijanapura Lake |  | 13.02125 | 77.685222 |
| 193 | Konena Agrahara lake |  | 12.959 | 77.658611 |
| 194 | Byatagunte Playa |  | 13.006778 | 77.637361 |
| 195 | Lingarajapura Lake |  | 13.007361 | 77.632111 |
| 196 | Geddalahalli |  | 13.12 | 77.345028 |
| 197 | Belakahalli |  | 12.907222 | 77.602472 |
| 198 | Arehalli 2 & 3 (Small tanks) |  | 12.913957 | 77.534073 |
| 199 | Doresani palya |  | 12.903361 | 77.596972 |
| 200 | Chikkalsandra Lake |  | 12.9155 | 77.9155 |
| 201 | Ittmadu |  | 12.919972 | 77.547056 |
| 202 | Thavarekare |  | 12.929083 | 77.612417 |
| 204 | Karisandra lake |  | 12.919083 | 77.571861 |
| 205 | Bovimaranahalli |  | 13.165556 | 77.627222 |
| 206 | Gundopanth lake |  | 12.991944 | 77.733333 |
| 207 | Kamakshi palya |  | 12.995278 | 77.731667 |
| 208 | Anche ramana kere (Gangondanahalli) |  | 13.082778 | 77.652222 |
| 209 | Sanigoruvahalli |  | 13.111389 | 77.703889 |
| 210 | Shivanahalli (Agrahara Dasarahalli) |  | 13.241389 | 77.703333 |

## Named tanks in the KSRSAC layer

One hundred and seventy-three polygons have a name. The other tank polygons are on the map and in the GeoJSON, without a name to list. Centroid latitude and longitude are the representative point of the simplified outline.

| Object id | Name in the file | LULC description | Centroid latitude | Centroid longitude |
|---|---|---|---|---|
| 1243 | Agara Kere | Tank | 12.83438 | 77.48725 |
| 1000 | Arekere Lake | Tank | 12.88286 | 77.59844 |
| 663 | B Narayanapura Childrens Park & Walkers Track | Tank | 12.99685 | 77.68271 |
| 1144 | Bagalagunte Lake | Tank | 13.05976 | 77.49864 |
| 951 | BBMP Park Koramangala 4th B Block | Tank | 12.93179 | 77.62675 |
| 998 | BBMP Park Koramangala 4th B Block | Tank | 12.93222 | 77.6259 |
| 751 | BEL Lake | Tank | 13.05632 | 77.56437 |
| 644 | Bellandur Lake | Tank | 12.93724 | 77.67494 |
| 945 | Bellandur Lake | Tank | 12.9374 | 77.66606 |
| 664 | Bengaluru | Tank | 13.01161 | 77.70485 |
| 740 | Bengaluru | Island | 13.06209 | 77.59786 |
| 752 | Bengaluru | Tank | 13.04907 | 77.58164 |
| 781 | Bengaluru | Tank | 13.04848 | 77.58235 |
| 808 | Bengaluru | Tank | 13.08451 | 77.62814 |
| 815 | Bengaluru | Tank | 13.0783 | 77.62327 |
| 816 | Bengaluru | Island | 13.06274 | 77.61378 |
| 817 | Bengaluru | Tank | 13.09314 | 77.62789 |
| 825 | Bengaluru | Tank | 13.08951 | 77.62485 |
| 843 | Bengaluru | Island | 13.08368 | 77.61053 |
| 844 | Bengaluru | Island | 13.08363 | 77.61013 |
| 845 | Bengaluru | Island | 13.08696 | 77.61044 |
| 1279 | Bengaluru | Tank | 13.087 | 77.61077 |
| 1281 | Bengaluru | Tank | 13.06175 | 77.59799 |
| 1224 | Bhimmanakuppe Govt. Lake (Hunasemaradapalya Kere) | Tank | 12.91759 | 77.44694 |
| 1195 | Byandahalli Lake | Tank | 13.00658 | 77.44577 |
| 997 | Byrasandra Lake | Tank | 12.93057 | 77.59537 |
| 1215 | ChikkaKere (Chikkabasthi) | Tank | 12.94698 | 77.47111 |
| 801 | Chokkanahalli lake | Tank | 13.08462 | 77.62916 |
| 788 | Dasanayakanahalli Lake | Tank | 13.11444 | 77.6924 |
| 1239 | Devagere Kere (Veerannakere) | Tank | 12.85409 | 77.46267 |
| 648 | Devarabisana Halli Lake | Tank | 12.92389 | 77.68665 |
| 656 | Devasandra Lake | Tank | 13.00513 | 77.69365 |
| 657 | Devasandra Lake | Tank | 13.00136 | 77.70326 |
| 803 | Doddabommasandra Lake | Tank | 13.06517 | 77.56292 |
| 652 | Doddanekundi Lake | Tank | 12.97209 | 77.69093 |
| 653 | Doddanekundi Lake | Tank | 12.97094 | 77.68658 |
| 660 | Doddanekundi Lake | Tank | 12.97528 | 77.68824 |
| 1157 | Dubasipalya Kere | Tank | 12.93005 | 77.49484 |
| 1192 | Gangondanahalli Kere | Tank | 13.01896 | 77.47408 |
| 1237 | Gollahalli Govt. Lake (H Gollahalli  Lake ) | Tank | 12.87412 | 77.48302 |
| 1227 | Govt. MaggeKere | Tank | 12.88472 | 77.44581 |
| 755 | Halasuru Lake | Island | 12.98204 | 77.61765 |
| 756 | Halasuru Lake | Island | 12.98682 | 77.62104 |
| 757 | Halasuru Lake | Island | 12.98691 | 77.6218 |
| 758 | Halasuru Lake | Island | 12.98314 | 77.62072 |
| 761 | Halasuru Lake | Island | 12.98136 | 77.6194 |
| 762 | Halasuru Lake | Island | 12.985 | 77.62051 |
| 1293 | Halasuru Lake | Tank | 12.98214 | 77.6193 |
| 1186 | Harokyathanahalli Lake 3 | Tank | 13.05218 | 77.44438 |
| 440 | Hesarghatta | Tank | 13.1455 | 77.48578 |
| 12 | Hesarghatta Tank | Tank | 13.16423 | 77.48778 |
| 14 | Hesarghatta Tank | Tank | 13.15543 | 77.4882 |
| 448 | Hesarghatta Tank | Tank | 13.17141 | 77.49334 |
| 479 | Hesarghatta Tank | Tank | 13.15239 | 77.49173 |
| 914 | Hesarghatta Tank | Tank | 13.144 | 77.4916 |
| 670 | Hoodi Lake | Tank | 12.99987 | 77.71658 |
| 745 | Horamavu Lake | Tank | 13.02463 | 77.66714 |
| 1026 | Hosakerehalli Lake | Tank | 12.92553 | 77.53557 |
| 1153 | Hosakerehalli Lake | Tank | 12.9263 | 77.53325 |
| 17 | Hoskote Kere | Tank | 13.11268 | 77.7634 |
| 18 | Hoskote Kere | Tank | 13.10644 | 77.76064 |
| 19 | Hoskote Kere | Tank | 13.11285 | 77.76452 |
| 20 | Hoskote Kere | Tank | 13.11169 | 77.7596 |
| 21 | Hoskote Kere | Tank | 13.11261 | 77.75996 |
| 24 | Hoskote Kere | Tank | 13.11059 | 77.76214 |
| 26 | Hoskote Kere | Tank | 13.11549 | 77.76065 |
| 31 | Hoskote Kere | Tank | 13.10558 | 77.76442 |
| 533 | Hoskote Kere | Tank | 13.09419 | 77.76439 |
| 534 | Hoskote Kere | Tank | 13.0906 | 77.76441 |
| 535 | Hoskote Kere | Tank | 13.08886 | 77.75921 |
| 536 | Hoskote Kere | Tank | 13.09703 | 77.76533 |
| 537 | Hoskote Kere | Tank | 13.09427 | 77.76108 |
| 538 | Hoskote Kere | Tank | 13.08507 | 77.75953 |
| 539 | Hoskote Kere | Tank | 13.08437 | 77.75888 |
| 1318 | Hoskote Kere | Tank | 13.07988 | 77.76298 |
| 52 | Hoskote Tank | Tank | 13.07555 | 77.76863 |
| 1163 | Idly Lake | Tank | 12.90358 | 77.50659 |
| 1187 | K G. Lakkenahalli Lake | Tank | 13.01655 | 77.46151 |
| 774 | Kacharakkana Halli Lake | Tank | 13.01907 | 77.62693 |
| 1193 | Kachohalli Lake 1 | Tank | 13.00025 | 77.46607 |
| 661 | Kaggadasapura Lake | Tank | 12.97715 | 77.67336 |
| 666 | Kaggadasapura Lake | Tank | 12.98158 | 77.67341 |
| 743 | Kalkere Lake | Tank | 13.04734 | 77.66291 |
| 746 | Kalkere Lake | Tank | 13.04944 | 77.6665 |
| 1226 | Kambhipura Govt. Karabu Kere-2 | Tank | 12.88768 | 77.468 |
| 1230 | Kambhipura Govt. Kharabu Kere | Tank | 12.89014 | 77.45812 |
| 1196 | Kannalli Lake 1 | Tank | 12.96988 | 77.46168 |
| 1212 | Kannalli Lake 1 | Tank | 12.96669 | 77.46163 |
| 783 | Kannuru Lake | Tank | 13.10026 | 77.65117 |
| 1027 | Kempambudhi Kere | Tank | 12.95182 | 77.56014 |
| 1205 | Kenchanapura Govt. Lake | Tank | 12.95564 | 77.44922 |
| 1298 | Kengeri Lake | Tank | 12.91716 | 77.48913 |
| 1199 | Kodigehalli Acchegowdana Katte | Tank | 12.983 | 77.46598 |
| 1197 | Kodigehalli Kere | Tank | 12.97681 | 77.4679 |
| 1210 | Kommaghatta Govt. Lake | Tank | 12.9315 | 77.46899 |
| 1211 | Kommaghatta Govt. Lake | Tank | 12.93058 | 77.46765 |
| 654 | Kowdenahalli Lake ITI | Tank | 13.01169 | 77.68537 |
| 1240 | Kumbalagodu Gollahalli Govt. Lake | Tank | 12.84032 | 77.44769 |
| 1242 | Kumbalagodu Gollahalli Govt. Lake | Tank | 12.8374 | 77.44657 |
| 655 | L M Nagar Lake | Tank | 13.00991 | 77.67676 |
| 651 | Lake of swathanthra nagar | Tank | 13.01029 | 77.71316 |
| 1185 | Lakshmipura Lake | Tank | 13.03322 | 77.46831 |
| 994 | Lalbagh Lake | Tank | 12.94686 | 77.58658 |
| 996 | Lalbagh Lake | Tank | 12.94639 | 77.58352 |
| 1188 | Machohalli Lake (Machohalli Chikkere) | Tank | 13.01469 | 77.45373 |
| 1194 | Machohalli Lake (Machohalli Chikkere) | Tank | 13.01224 | 77.45453 |
| 1191 | Madavara Kere /Anchepalya Lake | Tank | 13.05007 | 77.47937 |
| 1004 | Madiwala Lake(BTM Lake) | Tank | 12.90081 | 77.61365 |
| 1294 | Madiwala Lake(BTM Lake) | Tank | 12.90823 | 77.61781 |
| 782 | Mahadevanakodaganahalli Lake | Tank | 13.13708 | 77.68489 |
| 784 | Mahadevanakodaganahalli Lake | Tank | 13.13994 | 77.69039 |
| 790 | Mahadevanakodaganahalli Lake | Tank | 13.1364 | 77.68299 |
| 791 | Mahadevanakodaganahalli Lake | Tank | 13.14203 | 77.68909 |
| 792 | Mahadevanakodaganahalli Lake | Tank | 13.1417 | 77.69576 |
| 793 | Mahadevanakodaganahalli Lake | Tank | 13.13613 | 77.6853 |
| 794 | Mahadevanakodaganahalli Lake | Tank | 13.13802 | 77.68454 |
| 1278 | Mahadevanakodaganahalli Lake | Tank | 13.14085 | 77.6883 |
| 672 | Mahadevapura Lake Park | Tank | 12.98768 | 77.69228 |
| 675 | Mahadevapura Lake Park | Tank | 12.98489 | 77.69416 |
| 671 | Maheswaramma Temple Road Park | Tank | 12.99094 | 77.69592 |
| 1154 | Mallathahalli Lake ಮಲ್ಲತ್ತಹಳ್ಳಿ ಕೆರೆ | Tank | 12.96509 | 77.49479 |
| 1214 | Manganahalli Lake 2 | Tank | 12.95705 | 77.46978 |
| 789 | Marenahali Lake (MowjeKere) | Tank | 13.11181 | 77.67947 |
| 646 | Munnekolala Lake Park | Tank | 12.96075 | 77.70817 |
| 775 | Nagavara Lake | Tank | 13.045 | 77.60696 |
| 804 | Narsipura Lake | Tank | 13.07326 | 77.55734 |
| 806 | Narsipura Lake | Tank | 13.07203 | 77.55863 |
| 645 | Panathur Lake | Tank | 12.9308 | 77.70834 |
| 649 | Panathur Lake | Tank | 12.93176 | 77.70693 |
| 1002 | Puttenahalli Lake | Tank | 12.89033 | 77.58734 |
| 1003 | Puttenahalli Lake | Tank | 12.88946 | 77.58781 |
| 1206 | Ramasandra (Hire Kere) | Tank | 12.95226 | 77.45543 |
| 1207 | Ramasandra (Hire Kere) | Tank | 12.95671 | 77.46 |
| 1219 | Ramasandra (Hire Kere) | Tank | 12.95079 | 77.45861 |
| 1220 | Ramasandra (Hire Kere) | Tank | 12.95538 | 77.461 |
| 1221 | Ramasandra (Hire Kere) | Tank | 12.95033 | 77.4556 |
| 1001 | Sarakki Lake | Tank | 12.89984 | 77.58076 |
| 1295 | Sarakki Lake | Tank | 12.89922 | 77.57885 |
| 658 | Seetharamapalya Lake | Tank | 12.98439 | 77.71357 |
| 659 | Seetharamapalya Lake | Tank | 12.98293 | 77.7129 |
| 1198 | Sheegehalli Lake | Tank | 12.97699 | 77.44989 |
| 1143 | Shettihalli Lake, Jalahalli West | Tank | 13.05913 | 77.51808 |
| 809 | SHIRDI LAKE | Tank | 13.08546 | 77.53871 |
| 802 | Singapura lake | Tank | 13.08227 | 77.5363 |
| 805 | Sovereign lake | Tank | 13.09429 | 77.5419 |
| 1160 | Sunkalpalya Lake | Tank | 12.90669 | 77.49585 |
| 188 | Thattekere | Tank | 12.70625 | 77.60943 |
| 189 | Thattekere | Tank | 12.71424 | 77.6153 |
| 190 | Thattekere | Tank | 12.71602 | 77.61599 |
| 191 | Thattekere | Tank | 12.71969 | 77.61646 |
| 192 | Thattekere | Tank | 12.7199 | 77.62401 |
| 193 | Thattekere | Tank | 12.72133 | 77.6211 |
| 195 | Thattekere | Tank | 12.70709 | 77.63494 |
| 196 | Thattekere | Tank | 12.71252 | 77.62973 |
| 197 | Thattekere | Tank | 12.71847 | 77.62893 |
| 198 | Thattekere | Tank | 12.72154 | 77.62504 |
| 199 | Thattekere | Tank | 12.72234 | 77.62734 |
| 200 | Thattekere | Tank | 12.72497 | 77.62836 |
| 797 | Thirumenahalli Lake | Tank | 13.09284 | 77.62905 |
| 807 | Veerasagara Lake | Tank | 13.10235 | 77.5568 |
| 643 | Vibhutipura Kere | Tank | 12.96654 | 77.67746 |
| 662 | Vibhutipura Kere | Tank | 12.96783 | 77.67626 |
| 665 | Vibhutipura Kere | Tank | 12.96914 | 77.68161 |
| 810 | Vidyaranyapura Lake and Park | Tank | 13.07661 | 77.55497 |
| 813 | Vidyaranyapura Lake and Park | Tank | 13.07574 | 77.55413 |
| 667 | Yeklgata Lake | Tank | 12.98666 | 77.6981 |
| 922 | Yelahanka Lake | Tank | 13.12136 | 77.58696 |
| 925 | Yelahanka Lake | Tank | 13.11131 | 77.59988 |
| 926 | Yelahanka Lake | Tank | 13.1158 | 77.58743 |
| 934 | Yelahanka Lake | Island | 13.11411 | 77.59406 |
| 935 | Yelahanka Lake | Island | 13.11594 | 77.58858 |
| 936 | Yelahanka Lake | Island | 13.11556 | 77.58866 |
| 1283 | Yelahanka Lake | Tank | 13.11295 | 77.59427 |

## Frequently asked questions

### Does this map show the legal lake buffer?

No. The legal lake buffer under Act 19 of 2026 depends on the tank's revenue area and is measured from the revenue boundary. Those two things are not in the KSRSAC or BBMP files used here, so no lake buffer is drawn.

### What do the coloured bands along drains mean?

They are 50 m either side of the mapped primary line and 25 m either side of the mapped secondary line. Those are the RMP-2015 widths from the middle, as the Supreme Court recorded them on 5 Mar 2019. They are not a survey of the drain's edge.

### Did the Supreme Court keep the NGT's 75 m lake buffer for the whole city?

No. The judgment of 5 Mar 2019 set aside the NGT's general direction of 4 May 2016, including the 75 m lake buffer and the wider drain buffers, except the direction issued against respondent Nos. 9 and 10 in that case.

### Which lake buffer applies in 2026?

The table in Karnataka Act 19 of 2026, from 0 m to 30 m by tank area, measured from the revenue boundary. The Act came into force on 18 Feb 2026. The NGT had already issued notices on the proposal to reduce buffers. Whether any later order affects one lake is something to ask a lawyer.

### Why are two BBMP lakes missing from the map?

Mangammanahalli lake and Kenchanapura lake have a blank latitude and longitude in the source file. They are in the table. They are not given a guessed position.

### Can I use this map in place of a survey?

No. Use it to see that a tank or a drain is in the neighbourhood, then pull the RTC, the lake survey map and the sanctioned plan. A lawyer applies the buffer to the survey number.

## Talk it through with acre&key

If you have a survey number and a sanctioned plan, acre&key can sit with you and read them against this map before you decide whether to go further.

**Lawyer note:** Buffer widths, the revenue boundary, and whether an older approval still stands are legal questions. This page is general information, not advice on a particular plot or project. Consult a property lawyer before you pay, sign or register.

## Sources

Checked 20 Oct 2026.

1. Karnataka Act 19 of 2026, Karnataka Tank Conservation and Development Authority (Amendment) Act, 2025, Gazette Extraordinary, 18 Feb 2026 (copy hosted by OpenCity): https://data.opencity.in/dataset/2a2c0701-853e-4db3-b1d4-06ee8674c628/resource/ffff8ed9-228d-42a2-a596-3b4c06a8d726/download/lake-tank-buffer.pdf
2. The same amendment as passed by the legislature: https://kla.kar.nic.in/council/house/bills/156/33E.pdf
3. Supreme Court judgment, 5 Mar 2019, Mantri Techzone Pvt. Ltd. v. Forward Foundation: https://api.sci.gov.in/supremecourt/2016/16740/16740_2016_Judgement_05-Mar-2019.pdf
4. The Indian Express, NGT notices on the buffer reduction, 8 Aug 2025: https://indianexpress.com/article/cities/bangalore/ngt-takes-suo-motu-cognisance-of-buffer-zone-reduction-around-lakes-karnataka-10213014/
5. KSRSAC tanks for Bengaluru Urban, via OpenCity: https://data.opencity.in/dataset/lakes-and-ponds-in-bengaluru-district
6. KSRSAC primary and secondary stormwater drains, via OpenCity: https://data.opencity.in/dataset/bengaluru-stormwater-drains-maps
7. BBMP lake points, via OpenCity, source portal https://lms.bbmpgov.in/lake : https://data.opencity.in/dataset/bbmp-lakes
8. Bhoomi land records: https://landrecords.karnataka.gov.in/
9. Survey Settlement and Land Records, Revenue Maps Online: https://landrecords.karnataka.gov.in/service3/
10. OpenStreetMap tile copyright: https://www.openstreetmap.org/copyright

## Suggested images

1. Hero and card, 1200x675 WebP, at assets/img/bengaluru-lake-buffer-and-rajakaluve-map-2026.webp. Alt: "Map of Bengaluru tanks and stormwater drains with buffer bands along primary and secondary drains"
