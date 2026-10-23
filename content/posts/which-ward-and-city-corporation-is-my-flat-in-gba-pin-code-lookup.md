---
title: "Which Corporation Is My Area in Bangalore? GBA Ward Lookup"
meta_description: "Which corporation is my area in Bangalore GBA? Find your city corporation and ward; our pin-code overlay shows a third of pin codes span two or more."
slug: "which-ward-and-city-corporation-is-my-flat-in-gba-pin-code-lookup"
canonical: "https://acrenkey.com/blogs/which-ward-and-city-corporation-is-my-flat-in-gba-pin-code-lookup/"
lives: "blog"
primary_keyword: "which corporation is my area bangalore gba"
secondary_keywords:
  - "gba five corporations list"
  - "which ward am i in bengaluru"
  - "pin code to ward bengaluru"
  - "gba ward list 369"
  - "know your new corporation"
dataset: "which-ward-and-city-corporation-is-my-flat-in-gba-pin-code-lookup.csv"
date_modified: "2026-10-19"
status: "DRAFT FOR REVIEW. Do not publish."
---

# Which corporation is my area in Bengaluru (GBA)? Ward and pin-code lookup

**Short answer:** To find which corporation your area is in under the GBA, drop a pin on your building in GBA's official ward map, not just your pin code. Bengaluru has five city corporations and 369 wards. In our overlay, 31 of the 94 city pin codes spanned two or more corporations, and a typical pin code covered five wards.

> **Key takeaways**
> - **Five corporations, 369 wards:** Central 63, North 72, South 72, East 50, West 112 (final delimitation notified 19 Nov 2025, as reported).
> - **A pin code isn't enough.** One in three city pin codes crosses a corporation line, and only 4 of 94 sit inside a single ward.
> - **Use the official map**, then confirm on paper: your tax receipt or e-Khata.
> - **Corporation decides your khata and tax office**, not your registration office or water supply.
> - **Outside GBA limits** (much of the east's fringe), records are on e-Swathu or the state's municipal e-Aasthi system instead.

For years the answer to "which corporation?" was simply BBMP. Now it's one of five, and it trips people up in small ways: a tax receipt that says one thing, a khata office that says another. This page shows how to find your corporation and ward without guessing, with a pin-code lookup table we built from the official ward map.

![Map of Bengaluru's five GBA city corporations with ward boundaries and pin-code outlines](/img/blog/gba-corporations-pincodes-map.png)

## What are the five GBA city corporations?

BBMP was replaced by five city corporations under the Greater Bengaluru Governance Act 2024. The final ward delimitation, with 369 wards, was notified on 19 Nov 2025 ([The Hindu](https://www.thehindu.com/news/national/karnataka/karnataka-govt-notifies-369-wards-delimitation-for-five-bengaluru-corporations/article70300300.ece), news). Sources differ on when the switch took effect: The Hindu says BBMP ceased on 2 Sep 2025, while OpenCity says GBA took over from October 2025. Go by the corporation named on your current records.

| Corporation | Wards | Area of ward polygons (approx.) | Avg area per ward | Avg people per ward* |
|---|---|---|---|---|
| Central | 63 | 78 sq km | 1.2 sq km | 23,129 |
| North | 72 | 160 sq km | 2.2 sq km | 24,901 |
| South | 72 | 152 sq km | 2.1 sq km | 22,608 |
| East | 50 | 163 sq km | 3.3 sq km | 17,108 |
| West | 112 | 163 sq km | 1.5 sq km | 23,835 |
| **Total** | **369** | **716 sq km** | **1.9 sq km** | **22,772** |

Ward counts: [The Hindu](https://www.thehindu.com/news/cities/bangalore/karnataka-notifies-reservation-for-369-wards-of-new-bengaluru-corporations-questions-persist-over-quotas/article70718764.ece) (news), matching the ward file. Areas and population: acre&key calculation from the 369-ward KML published by [OpenCity](https://data.opencity.in/dataset/gba-wards-delimitation-2025). *Population is the field in the ward file (8.40 million in total). The file doesn't state the census year, so treat it as the delimitation base, not today's population.

East has the fewest wards but the largest average ward, about 3.3 sq km. Its wards are bigger and less dense on paper, which fits a corporation that includes much of the fast-growing outer east.

## How do you find your corporation and ward?

1. **Open GBA's official [GIS viewer](https://bbmp.gov.in/gisviewer/index.html)**, which shows ward and corporation boundaries. (It's hosted on the old bbmp.gov.in domain and can be slow; try again if it doesn't load.)
2. **Find your building** and note the ward number, ward name and corporation.
3. **Or use the KML file:** download "Final Wards Map - 369 Wards KML" (December 2025 version, with ward name changes from 1 Dec 2025) from [OpenCity](https://data.opencity.in/dataset/gba-wards-delimitation-2025), open it in Google Earth, and drop a pin on your building. OpenCity is a non-government mirror, so treat the GIS viewer and the notification as the authority.
4. **Confirm on paper:** your latest property tax receipt or e-Khata should name the same corporation.

News reports in 2025 also pointed to a "Know Your New Corporation" search on the same domain ([Hindustan Times](https://www.hindustantimes.com/cities/bengaluru-news/how-to-check-your-new-bengaluru-corporation-under-gba-full-list-of-wards-and-link-here-101756966982784.html), news). It didn't load when we tried it, so we can't vouch for whether it reflects the final 369-ward map.

## Why isn't a pin code enough?

Pin codes were drawn for delivering post, not running a city. To measure how much they cross ward and corporation lines, we overlaid India Post pin-code boundaries ([OpenCity, Pincode Maps of Cities: Bengaluru](https://data.opencity.in/dataset/pincode-maps-of-cities)) on the 369-ward map and measured the share of each pin code's area in each ward.

| Finding (pin codes at least half inside GBA wards) | Result |
|---|---|
| City pin codes in the map | 110 |
| At least half inside GBA ward boundaries | 94 |
| Span two or more corporations (5%+ of area each) | 31 (33%) |
| Wards per pin code (5%+ of area), median | 5 |
| Most wards in one pin code | 10 |
| Pin codes inside a single ward | 4 |

So a pin code tells you the neighbourhood, and often not even the corporation.

### Worked example 1: Whitefield, 560066

| Measure | Result |
|---|---|
| Area of the pin code | about 43.8 sq km |
| Share inside GBA ward boundaries | 72% |
| Largest single ward (Hagaduru) | 13.2% of the area |
| Next four | Kundalahalli 12.9%, Varthur 11.6%, Whitefield 10.1%, S.M Krishna Ward 9.6% |

If you guessed the ward from the pin code alone, picking the largest ward, you'd be right for only about 13% of the area, and wrong for about 87%. And about 28% of this pin code's area sits outside GBA ward boundaries altogether, so some addresses with it may not be under a city corporation at all.

### Worked example 2: C V Raman Nagar belt, 560093

| Corporation | Share of the pin code's area |
|---|---|
| East (Mahadevapura 30.3%, Sangama 11.4%, others) | 58% |
| Central (Kaggadasapura 22.5%, G.M Palya 13.4%) | 42% |

Even the corporation is close to a coin toss here: assuming "East" from the pin code would be wrong for about 42% of the area.

## Pin codes in and around East Bengaluru

These are the pin codes with at least 5% of their area in the East corporation. The full table for all 110 pin codes is in the CSV published with this page.

| Pin code | Inside GBA | Corporation split | Wards (5%+) | Largest wards |
|---|---|---|---|---|
| 560008 | all | Central 95%, East 5% | 8 | Kodihalli, Agaram, Jogpalya |
| 560016 | 94% | East 94% | 9 | Bhattarahalli, A Narayanapura, Kotthur |
| 560017 | all | East 91%, Central 9% | 6 | Vibhootipura, Vignananagara, Yamalur |
| 560035 | 90% | East 68%, South 21% | 4 | Gunjur, Panathur, Shivanasamudra |
| 560036 | all | all East | 6 | Basavanapura, Anandapura, Krishnanagar |
| 560037 | all | all East | 7 | Panathur, Yamalur, Ashwath Nagar |
| 560043 | 94% | East 75%, North 15%, Central 4% | 8 | Horamavu, Kalkere, Babusab Palya |
| 560048 | all | all East | 6 | Kaveri Nagara, Dodda Nekkundi, Bharath Aikya |
| 560066 | 72% | East 72% | 5 | Hagaduru, Kundalahalli, Varthur |
| 560067 | 73% | East 73% | 4 | Belathur, Kadugodi, Hoodi |
| 560075 | all | Central 81%, East 19% | 4 | Jeevan Bhimanagar, New Thippasandra, Indiranagar |
| 560077 | 89% | North 45%, East 44% | 4 | K Narayanapura, Kogilu, Thanisandra |
| 560087 | 99% | East 99% | 2 | Varthur, Gunjur |
| 560093 | all | East 58%, Central 42% | 6 | Mahadevapura, Kaggadasapura, G.M Palya |
| 560103 | 62% | East 25%, South 22%, Central 14% | 4 | Agaram, Yamalur, Kasavanahalli |

"Inside GBA" is the share of the pin code's mapped area inside ward polygons. Lakes and other areas left out of ward polygons count as outside, which is likely why lake-heavy pin codes such as 560103 (Bellandur) score lower. The two maps come from different sources, so slivers along edges are expected; we ignore anything under 5%.

## The pin, pin-drop, paper test (our framework)

| Step | What it tells you | Good enough for |
|---|---|---|
| **Pin code** | The neighbourhood | Shortlisting areas |
| **Pin-drop** on the official ward map | Ward and corporation for that exact building | Planning visits, checking which office to approach |
| **Paper**: tax receipt, e-Khata, sale deed schedule | What the records actually say | Paying, signing, registering |

If the pin-drop and the paper disagree, stop and ask why before paying. It can be a boundary change, an old receipt or a records error. Each needs a different fix.

## What does your corporation change, and what doesn't it?

**It changes:**
- **Khata and property tax.** GBA's e-Khata services moved to e-Aasthi 2.0, launched on 22 Sep 2026. About 11 lakh of more than 35 lakh properties had a final e-Khata at that point. Our [A-khata, B-khata and e-Khata guide](https://acrenkey.com/blogs/a-khata-vs-b-khata-vs-e-khata-what-bengaluru-buyers-must-know/) has the details, and [GBA replaces BBMP](https://acrenkey.com/insights/gba-replaces-bbmp-what-new-city-corporations-mean-for-buyers/) explains the wider change.
- **Which ward office** handles your complaints and local works.

**It doesn't change:**
- **Your sub-registrar office.** Registration is run by the Department of Stamps and Registration; see [Kaveri 2.0 registration steps](https://answers.acrenkey.com/kaveri-2-property-registration-steps/).
- **Your water supply.** BWSSB runs water across the city corporations; see our [water questions guide](https://acrenkey.com/blogs/water-bengaluru-bwssb-borewell-tanker-questions-to-ask/).
- **Your flood risk.** That depends on lakes, drains and terrain; see the [flood-prone areas map](https://acrenkey.com/blogs/bengaluru-flood-prone-areas-map-from-ksndmc-data/).

### Worked example 3: the stamp duty doesn't change either

Illustrative. A ₹90 lakh resale flat registered in any of the five corporations pays the same Karnataka charges: 5% duty (₹4,50,000), 10% cess on duty (₹45,000), the GBA surcharge of 2% of duty (₹9,000) and 2% registration (₹1,80,000), a total of **₹6,84,000** or 7.6%. The corporation affects where your khata and tax are handled, not what you pay at registration.

## What about areas outside GBA limits?

A lot of East Bengaluru's growth sits just outside the city corporations, in panchayat or municipal areas. There, records are Form 9 and Form 11 on e-Swathu for panchayats ([e-Swathu FAQ](https://eswathu.karnataka.gov.in/PublicFAQ.aspx)) or the state's [e-Aasthi](https://eaasthi.karnataka.gov.in/) urban property system for towns. Our answer on [checking whether a property is under the city or a panchayat](https://answers.acrenkey.com/check-bbmp-or-panchayat-east-bangalore/) covers how to tell, and [living in Hoskote](https://acrenkey.com/blogs/living-in-hoskote-property-rates-metro-water-flood-risk/) is an example of a town outside GBA.

## What mistakes do people make?

- **Assuming the pin code gives the corporation.**
- **Trusting an old BBMP receipt** without checking the current e-Khata.
- **Thinking the corporation sets the sub-registrar office.**
- **Ignoring the edge.** Buildings near a ward or GBA boundary need a careful pin-drop.

## Frequently asked questions

### What are the five city corporations in Bengaluru?

Bengaluru Central, North, South, East and West, set up under the Greater Bengaluru Governance Act 2024 in place of BBMP. The final ward delimitation was notified on 19 November 2025 with 369 wards: Central 63, North 72, South 72, East 50 and West 112.

### How do I know which GBA corporation my area is in?

Find your building on GBA's official GIS viewer, which shows ward and corporation boundaries, or drop a pin on it in the 369-ward KML file. Then confirm the corporation against your latest property tax receipt or e-Khata record before paying or signing anything.

### Can one pin code fall under two corporations?

Yes, often. In our overlay of India Post pin-code boundaries on the 369-ward map, 31 of 94 city pin codes had at least 5% of their area in two or more corporations. In 560093, for example, about 58% of the area is in East and 42% in Central.

### How many wards does a pin code cover in Bengaluru?

Typically about five. Across the 94 pin codes at least half inside GBA ward boundaries, the median number of wards covering 5% or more of the area was five, the highest was ten, and only four pin codes sat inside a single ward.

### How many wards are there under GBA?

369, under the final delimitation notified on 19 November 2025. The draft had 368, and one ward was added to West in the final notification. West has the most wards at 112, and East the fewest at 50.

### Does my corporation change my stamp duty?

No. Stamp duty, cess, the 2% GBA surcharge on duty and the 2% registration fee are the same across all five corporations, 7.6% in total for a resale flat. Your corporation decides where your khata and property tax are handled.

### Does my corporation decide my sub-registrar office?

No. Registration is run by the Department of Stamps and Registration, which has its own sub-registrar jurisdictions. On Kaveri 2.0 you enter the property details online and then book a slot at a sub-registrar office.

### Is Whitefield in the East corporation?

Most of pin code 560066 that falls inside GBA is in the East corporation, spread across wards including Hagaduru, Kundalahalli, Varthur and Whitefield. But about 28% of the pin code's area lies outside GBA ward boundaries, so check your exact building.

## Method notes

- Ward boundaries: OpenCity's "gba-369-wards-december-2025.kml" (369 wards, with corporation, ward ID and name fields), based on the 19 Nov 2025 notification with December 2025 name changes.
- Pin codes: OpenCity's "Pincode Map - Bengaluru" (India Post boundaries, 110 polygons).
- Method: polygon intersection in Python (shapely); shares are of each pin code's mapped area. Thresholds: 5% for counting a ward or corporation, 50% for counting a pin code as "inside GBA". Areas use a flat approximation at Bengaluru's latitude.
- Limits: area isn't population or property count, the two maps don't align perfectly, and boundaries can change. Use the official viewer for any decision.

## Talk it through with acre&key

If you'd like help confirming a property's corporation, ward and records before you book, book a consultation with acre&key.

**Lawyer note:** The khata and records points here are general information, not legal advice. Have a property lawyer confirm the records for your property before paying, signing or registering.

## Sources

Checked 19 Oct 2026.

1. GBA GIS viewer (ward and corporation boundaries): https://bbmp.gov.in/gisviewer/index.html
2. OpenCity, GBA wards delimitation 2025 (369-ward KML, December 2025): https://data.opencity.in/dataset/gba-wards-delimitation-2025
3. OpenCity, Pincode Maps of Cities (Bengaluru; India Post): https://data.opencity.in/dataset/pincode-maps-of-cities
4. The Hindu, 369 wards notified, 19 Nov 2025 (news): https://www.thehindu.com/news/national/karnataka/karnataka-govt-notifies-369-wards-delimitation-for-five-bengaluru-corporations/article70300300.ece
5. The Hindu, ward reservation and wards per corporation, Mar 2026 (news): https://www.thehindu.com/news/cities/bangalore/karnataka-notifies-reservation-for-369-wards-of-new-bengaluru-corporations-questions-persist-over-quotas/article70718764.ece
6. Hindustan Times, "Know Your New Corporation" lookup, 2025 (news): https://www.hindustantimes.com/cities/bengaluru-news/how-to-check-your-new-bengaluru-corporation-under-gba-full-list-of-wards-and-link-here-101756966982784.html
7. e-Swathu public FAQ: https://eswathu.karnataka.gov.in/PublicFAQ.aspx
8. e-Aasthi, Urban Property Management System: https://eaasthi.karnataka.gov.in/
9. Dataset: which-ward-and-city-corporation-is-my-flat-in-gba-pin-code-lookup.csv (acre&key overlay, 19 Oct 2026)

## Suggested images

1. `gba-corporations-pincodes-map.png`: five corporations with pin-code outlines. Alt: "Map of Bengaluru's five GBA city corporations with ward boundaries and pin-code outlines"
2. `pincode-560093-split.png`: one pin code split across East and Central. Alt: "Pin code 560093 split between the East and Central GBA corporations by area"
3. `pin-pindrop-paper.png`: three-step test. Alt: "Pin, pin-drop, paper: three steps to confirm a Bengaluru property's ward and corporation"

## Structured data (JSON-LD)

```json
{
 "@context": "https://schema.org",
 "@graph": [
  {
   "@type": "Article",
   "@id": "https://acrenkey.com/blogs/which-ward-and-city-corporation-is-my-flat-in-gba-pin-code-lookup/#article",
   "headline": "Which city corporation and ward is my Bengaluru property in?",
   "description": "Find your GBA city corporation and ward in Bengaluru. Our pin-code overlay shows a third of city pin codes span two or more corporations. Steps and table.",
   "author": {
    "@id": "https://acrenkey.com/#organization"
   },
   "publisher": {
    "@id": "https://acrenkey.com/#organization"
   },
   "dateModified": "2026-10-19",
   "inLanguage": "en-IN",
   "mainEntityOfPage": "https://acrenkey.com/blogs/which-ward-and-city-corporation-is-my-flat-in-gba-pin-code-lookup/",
   "url": "https://acrenkey.com/blogs/which-ward-and-city-corporation-is-my-flat-in-gba-pin-code-lookup/",
   "image": "https://acrenkey.com/img/blog/gba-corporations-pincodes-map.png"
  },
  {
   "@type": "Organization",
   "@id": "https://acrenkey.com/#organization",
   "name": "acre&key",
   "legalName": "Acrenkey Realty LLP",
   "url": "https://acrenkey.com"
  },
  {
   "@type": "FAQPage",
   "@id": "https://acrenkey.com/blogs/which-ward-and-city-corporation-is-my-flat-in-gba-pin-code-lookup/#faq",
   "mainEntity": [
    {
     "@type": "Question",
     "name": "What are the five city corporations in Bengaluru?",
     "acceptedAnswer": {
      "@type": "Answer",
      "text": "Bengaluru Central, North, South, East and West, set up under the Greater Bengaluru Governance Act 2024 in place of BBMP. The final ward delimitation was notified on 19 November 2025 with 369 wards: Central 63, North 72, South 72, East 50 and West 112."
     }
    },
    {
     "@type": "Question",
     "name": "How do I know which GBA corporation my area is in?",
     "acceptedAnswer": {
      "@type": "Answer",
      "text": "Find your building on GBA's official GIS viewer, which shows ward and corporation boundaries, or drop a pin on it in the 369-ward KML file. Then confirm the corporation against your latest property tax receipt or e-Khata record before paying or signing anything."
     }
    },
    {
     "@type": "Question",
     "name": "Can one pin code fall under two corporations?",
     "acceptedAnswer": {
      "@type": "Answer",
      "text": "Yes, often. In our overlay of India Post pin-code boundaries on the 369-ward map, 31 of 94 city pin codes had at least 5% of their area in two or more corporations. In 560093, for example, about 58% of the area is in East and 42% in Central."
     }
    },
    {
     "@type": "Question",
     "name": "How many wards does a pin code cover in Bengaluru?",
     "acceptedAnswer": {
      "@type": "Answer",
      "text": "Typically about five. Across the 94 pin codes at least half inside GBA ward boundaries, the median number of wards covering 5% or more of the area was five, the highest was ten, and only four pin codes sat inside a single ward."
     }
    },
    {
     "@type": "Question",
     "name": "How many wards are there under GBA?",
     "acceptedAnswer": {
      "@type": "Answer",
      "text": "369, under the final delimitation notified on 19 November 2025. The draft had 368, and one ward was added to West in the final notification. West has the most wards at 112, and East the fewest at 50."
     }
    },
    {
     "@type": "Question",
     "name": "Does my corporation change my stamp duty?",
     "acceptedAnswer": {
      "@type": "Answer",
      "text": "No. Stamp duty, cess, the 2% GBA surcharge on duty and the 2% registration fee are the same across all five corporations, 7.6% in total for a resale flat. Your corporation decides where your khata and property tax are handled."
     }
    },
    {
     "@type": "Question",
     "name": "Does my corporation decide my sub-registrar office?",
     "acceptedAnswer": {
      "@type": "Answer",
      "text": "No. Registration is run by the Department of Stamps and Registration, which has its own sub-registrar jurisdictions. On Kaveri 2.0 you enter the property details online and then book a slot at a sub-registrar office."
     }
    },
    {
     "@type": "Question",
     "name": "Is Whitefield in the East corporation?",
     "acceptedAnswer": {
      "@type": "Answer",
      "text": "Most of pin code 560066 that falls inside GBA is in the East corporation, spread across wards including Hagaduru, Kundalahalli, Varthur and Whitefield. But about 28% of the pin code's area lies outside GBA ward boundaries, so check your exact building."
     }
    }
   ]
  },
  {
   "@type": "BreadcrumbList",
   "itemListElement": [
    {
     "@type": "ListItem",
     "position": 1,
     "name": "Home",
     "item": "https://acrenkey.com/"
    },
    {
     "@type": "ListItem",
     "position": 2,
     "name": "Blog",
     "item": "https://acrenkey.com/blogs/"
    },
    {
     "@type": "ListItem",
     "position": 3,
     "name": "Which city corporation and ward is my Bengaluru property in?",
     "item": "https://acrenkey.com/blogs/which-ward-and-city-corporation-is-my-flat-in-gba-pin-code-lookup/"
    }
   ]
  }
 ]
}
```
