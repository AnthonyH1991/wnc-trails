# WNC Trail Conditions

A terminal-based trail conditions aggregator for Western North Carolina mountain biking. Pulls live weather data for the major riding hubs in the WNC mountains so you can quickly assess conditions before heading out.

## Coverage

| Location | Notable Trails |
|---|---|
| Brevard, NC | Pisgah National Forest, DuPont State Forest |
| Asheville, NC | Bent Creek, Kitsuma, Pump Track |
| Bryson City, NC | Tsali, Nantahala area |
| Waynesville, NC | Harmon Den, Fie Top |

## What It Shows

- **Current temp** and sky conditions
- **Wind** speed and direction
- **Overnight low** — tonight's forecasted low
- **Rain (24h)** — total precipitation in the last 24 hours
- **Freeze-thaw risk** — flagged when overnight low drops below 32°F but daytime high exceeds 35°F, a key indicator of soft, damaged trail conditions

## Usage

```bash
python3 weather_check.py
```

No API key or account needed. Uses [Open-Meteo](https://open-meteo.com), a free and open-source weather API.

## Requirements

Python 3.6+ with no third-party dependencies.

## Why Freeze-Thaw Matters

Freeze-thaw cycles are one of the most damaging conditions for mountain bike trails. When trails thaw during the day but refreeze overnight, the soil becomes soft and easily rutted. Riding during active freeze-thaw cycles causes lasting damage — this flag is a heads-up to check local trail association bulletins before riding.

- **Pisgah Area Trails**: [PMBA](https://pisgahmtb.org)
- **Tsali / Nantahala**: [Nantahala Outdoor Center](https://www.noc.com) / [SORBA WNC](https://www.sorbawnc.org)
- **Bent Creek / Kitsuma**: [SORBA WNC](https://www.sorbawnc.org)
