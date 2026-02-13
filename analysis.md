# Validity Analysis Tracker

## Status Key
- [ ] = Not started
- [~] = YAML created, awaiting evaluation
- [x] = Evaluation complete

## Ground-Truth Benchmarks (Validation)

| # | Benchmark | Target Region | MAE | Status |
|---|-----------|--------------|-----|--------|
| 1 | HELM | Southeast Asia | 0.00 | [x] Perfect match |
| 2 | SEA-HELM | Southeast Asia | 0.67 | [x] All within 1 pt |
| 3 | IberBench | Iberian | 0.00 | [x] Perfect match |

**Overall validation MAE: 0.22** (threshold: ≤ 1.0) -- PASS

## Batch 1: Translation-Based Benchmarks (High Priority)

| # | Benchmark | Target Region | Scores (IO/IC/IF/OO/OC/OF) | Avg | Status |
|---|-----------|--------------|----------------------------|-----|--------|
| 4 | MMLU | Southeast Asia | 2/1/1/2/2/2 | 1.7 | [x] |
| 5 | XNLI | Southeast Asia | 3/2/3/4/2/3 | 2.8 | [x] |
| 6 | XCOPA | Latin America (Indigenous) | 2/1/2/3/1/2 | 1.8 | [x] |
| 7 | AmericasNLI | Latin America (Indigenous) | 2/1/1/2/1/1 | 1.3 | [x] |
| 8 | PAWS-X | Southeast Asia | 2/1/1/3/1/2 | 1.7 | [x] |
| 9 | Belebele | Sub-Saharan Africa | 3/2/2/3/2/2 | 2.3 | [x] |
| 10 | FLORES-200 | Sub-Saharan Africa | 3/2/3/2/2/3 | 2.5 | [x] |

**Batch 1 average: 2.0** -- Translation-based benchmarks show systematic validity concerns, especially on Input Content and Output Content.

## Batch 2: Regional Exam-Based Benchmarks (High Priority)

| # | Benchmark | Target Region | Scores (IO/IC/IF/OO/OC/OF) | Avg | Status |
|---|-----------|--------------|----------------------------|-----|--------|
| 11 | C-Eval | East Asia (broader) | 1/1/2/2/1/3 | 1.7 | [x] |
| 12 | CMMLU | East Asia (broader) | 1/1/2/2/1/3 | 1.7 | [x] |
| 13 | KMMLU | East Asia (broader) | 3/2/3/3/4/4 | 3.2 | [x] |
| 14 | ArabicMMLU | MENA | 3/3/3/3/3/3 | 3.0 | [x] |
| 15 | IndoMMLU | Southeast Asia | 2/2/2/2/3/3 | 2.3 | [x] |
| 16 | INCLUDE | Sub-Saharan Africa | 3/3/2/3/3/2 | 2.7 | [x] |
| 17 | M3Exam | Southeast Asia | 2/3/3/3/3/3 | 2.8 | [x] |
| 18 | GAOKAO-Bench | East Asia | 1/1/2/2/1/2 | 1.5 | [x] |
| 19 | EXAMS | Sub-Saharan Africa | 2/3/2/2/2/2 | 2.2 | [x] |

**Batch 2 average: 2.3** -- China-centric exams (C-Eval, CMMLU, GAOKAO-Bench) score lowest when assessed for broader East Asian validity.

## Batch 3: Ground-Up Regional Benchmarks (Medium Priority)

| # | Benchmark | Target Region | Scores (IO/IC/IF/OO/OC/OF) | Avg | Status |
|---|-----------|--------------|----------------------------|-----|--------|
| 20 | MasakhaNER | Sub-Saharan Africa | 4/4/3/3/4/3 | 3.5 | [x] |
| 21 | AfriSenti | Sub-Saharan Africa | 4/5/3/3/4/3 | 3.7 | [x] |
| 22 | AfriQA | Sub-Saharan Africa | 4/4/3/3/3/3 | 3.3 | [x] |
| 23 | IrokoBench | Sub-Saharan Africa | 4/3/3/3/3/3 | 3.2 | [x] |

**Batch 3 average: 3.4** -- Ground-up African benchmarks score highest among non-ground-truth benchmarks, confirming the value of building within-region.

## Batch 4: Cultural Knowledge & Values (Medium Priority)

| # | Benchmark | Target Region | Scores (IO/IC/IF/OO/OC/OF) | Avg | Status |
|---|-----------|--------------|----------------------------|-----|--------|
| 24 | CulturalBench | Sub-Saharan Africa | 4/3/2/3/3/2 | 2.8 | [x] |
| 25 | BLEnD | Sub-Saharan Africa | 3/3/2/3/2/2 | 2.5 | [x] |
| 26 | CValues | East Asia (China) | 2/2/3/2/1/4 | 2.3 | [x] |
| 27 | TaarofBench | Iran/Persian | 3/4/3/4/4/3 | 3.5 | [x] |
| 28 | KoBBQ | East Asia (Korea) | 3/2/2/3/2/4 | 2.7 | [x] |

**Batch 4 average: 2.8** -- Narrowly-focused cultural benchmarks (TaarofBench) score well for their target culture; broader ones face coverage challenges.

## Batch 5: Domain-Specific Benchmarks (Medium Priority)

| # | Benchmark | Target Region | Scores (IO/IC/IF/OO/OC/OF) | Avg | Status |
|---|-----------|--------------|----------------------------|-----|--------|
| 29 | MedQA | Sub-Saharan Africa | 1/1/3/1/1/2 | 1.5 | [x] |
| 30 | AfriMedQA | Sub-Saharan Africa | 5/5/4/5/5/3 | 4.5 | [x] |
| 31 | LegalBench | Latin America (Indigenous) | 1/1/2/1/1/2 | 1.3 | [x] |
| 32 | LEXTREME | Sub-Saharan Africa | 2/1/2/2/1/2 | 1.7 | [x] |

**Batch 5 average: 2.3** -- Stark contrast between ground-up AfriMedQA (4.5) and ported domain benchmarks (MedQA 1.5, LegalBench 1.3).

## Region Files

| Region | File | Status |
|--------|------|--------|
| Southeast Asia | regions/southeast_asia.yaml | [x] |
| Iberian | regions/iberian.yaml | [x] |
| Sub-Saharan Africa | regions/sub_saharan_africa.yaml | [x] |
| East Asia | regions/east_asia.yaml | [x] |
| MENA | regions/mena.yaml | [x] |
| Latin America (Indigenous) | regions/latin_america_indigenous.yaml | [x] |
| Iran/Persian | regions/iran_persian.yaml | [x] |

## Summary Statistics

- **Total benchmarks analyzed: 32** (3 ground-truth + 29 new)
- **Ground-truth validation MAE: 0.22** (PASS)
- **All evaluations complete**
- **7 region context files created**

## Key Findings

### By Porting Strategy (average validity score)
| Strategy | Count | Avg Score | Range |
|----------|-------|-----------|-------|
| Ground-up (for target region) | 10 | **3.6** | 2.5-4.5 |
| Adapted | 1 | 2.7 | -- |
| Regional exams (single country) | 9 | 2.3 | 1.5-3.2 |
| Translation | 5 | 2.0 | 1.3-2.8 |
| None/baseline (Western) | 3 | 1.6 | 1.3-1.7 |

### Worst-Scoring Benchmarks (avg < 2.0)
| Benchmark | Region | Avg | Primary Concern |
|-----------|--------|-----|-----------------|
| AmericasNLI | Latin Am. Indigenous | 1.3 | Complete cultural/linguistic mismatch |
| LegalBench | Latin Am. Indigenous | 1.3 | US-specific legal framework |
| MedQA | Sub-Saharan Africa | 1.5 | US/Western medical knowledge |
| GAOKAO-Bench | East Asia broader | 1.5 | China-only exam system |
| C-Eval | East Asia broader | 1.7 | China-specific content/labels |
| CMMLU | East Asia broader | 1.7 | China-specific content/labels |
| HELM | Southeast Asia | 1.7 | Western-centric across all dims |
| LEXTREME | Sub-Saharan Africa | 1.7 | EU-specific legal framework |
| MMLU | Southeast Asia | 1.7 | Western-centric knowledge |
| PAWS-X | Southeast Asia | 1.7 | Zero SEA language coverage |

### Best-Scoring Benchmarks (avg >= 3.5)
| Benchmark | Region | Avg | Key Strength |
|-----------|--------|-----|-------------|
| AfriMedQA | Sub-Saharan Africa | 4.5 | Ground-up by African medical professionals |
| IberBench | Iberian | 3.7 | Regional ground-up, multilingual |
| SEA-HELM | Southeast Asia | 3.7 | Region-specific design for SEA |
| AfriSenti | Sub-Saharan Africa | 3.7 | Ground-up African sentiment |
| MasakhaNER | Sub-Saharan Africa | 3.5 | Ground-up African NER |
| TaarofBench | Iran/Persian | 3.5 | Deep cultural alignment |

### Most Common Validity Gaps (across all 32 benchmarks)
1. **Output Content** (avg 2.3) -- Labels rarely validated by regional annotators
2. **Input Content** (avg 2.4) -- Cultural sensitivity of instances often misaligned
3. **Input Form** (avg 2.3) -- Script/modality mismatches with target populations
4. **Output Form** (avg 2.6) -- Text-only evaluation vs. speech-interface needs
5. **Output Ontology** (avg 2.6) -- Taxonomies encoding source-culture values
6. **Input Ontology** (avg 2.6) -- Missing regionally-relevant test categories

## Generated Artifacts

- `results/*.json` -- 32 evaluation result files
- `results/*_report.md` -- 32 detailed markdown reports
- `results/all_radar.png` -- Combined radar chart (all 32 benchmarks)
- `results/comparison_radar.png` -- Comparison chart (SEA benchmarks)
- `results/summary.csv` -- Spreadsheet for human review (with empty human_score/human_notes columns)
