# ✍️ Writing Studio — Typography Analyzer

Part of **BlackRoad Studio** — production creative tools.

Analyze readability, generate type scales, check WCAG contrast, and suggest font pairings — pure Python, zero dependencies.

## Features

- **Flesch Reading Ease** — sentence/syllable analysis, grade level scoring
- **Type scale generator** — modular scale with any ratio (golden ratio default: 1.618)
- **WCAG contrast checker** — AA / AAA grades for fg/bg pairs
- **Line-height recommendations** — WCAG 1.4.12 compliance
- **Measure (line-length) checker** — 45–75 character sweet-spot
- **Font pairing suggestions** — rule-based category contrast
- **CSS / Tailwind exports** — `@import`, `font-family`, CSS vars
- **SQLite font library** — save, query, delete fonts

## Quick start

```bash
# Analyze text readability
python src/typography_analyzer.py readability "Your text here" --size 16 --lh 1.6

# Generate type scale (golden ratio)
python src/typography_analyzer.py scale --base 1.0 --ratio 1.618 --css

# Check WCAG contrast
python src/typography_analyzer.py contrast '#1e293b' '#f8fafc'

# Add a font
python src/typography_analyzer.py add-font "Inter" sans-serif --weights 400,600,700 --gid Inter

# Suggest pairings
python src/typography_analyzer.py pair <font-id>
```

## Common ratios

| Name | Ratio | Effect |
|---|---|---|
| Minor Second | 1.067 | Subtle scale |
| Major Second | 1.125 | Gentle |
| Minor Third | 1.2 | Comfortable |
| Major Third | 1.25 | Clear hierarchy |
| Perfect Fourth | 1.333 | Traditional |
| Golden Ratio | **1.618** | Harmonious |

## Tests

```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=src
```

---

**Proprietary Software — BlackRoad OS, Inc.**

This software is proprietary to BlackRoad OS, Inc. Source code is publicly visible for transparency and collaboration. Commercial use, forking, and redistribution are prohibited without written authorization.

**BlackRoad OS — Pave Tomorrow.**

*Copyright 2024-2026 BlackRoad OS, Inc. All Rights Reserved.*
