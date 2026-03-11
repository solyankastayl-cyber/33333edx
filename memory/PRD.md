# TA Engine PRD - PHASE 13.3 Factor Generator

## Original Problem Statement
TA Engine - Institutional-grade quant trading platform. Building autonomous Alpha Factory for systematic signal generation. PHASE 13.3 implements Factor Generator that converts 308 features into 1000+ candidate factors.

## Architecture Overview
```
backend/
├── core/
│   └── database/              # Unified MongoDB Connection
├── modules/
│   ├── alpha_factory/         
│   │   ├── alpha_types.py           # PHASE 13.1 - Node types
│   │   ├── alpha_node_registry.py   # PHASE 13.1 - Node registry
│   │   ├── alpha_repository.py      # PHASE 13.1 - Node persistence
│   │   ├── alpha_routes.py          # PHASE 13.1 - Node API
│   │   ├── feature_library/         # PHASE 13.2
│   │   │   ├── feature_types.py     # 308 features
│   │   │   ├── feature_registry.py
│   │   │   ├── feature_transforms.py # 16 transforms
│   │   │   └── feature_routes.py
│   │   └── factor_generator/        # PHASE 13.3 ✅
│   │       ├── factor_types.py      # Factor, FactorBatchRun
│   │       ├── factor_templates.py  # 8 templates
│   │       ├── feature_selector.py  # Category compatibility
│   │       ├── factor_combinator.py # Creates factors
│   │       ├── factor_constraints.py # Anti-garbage
│   │       ├── factor_transformer.py # 14 transforms
│   │       ├── factor_generator.py  # Main engine
│   │       ├── factor_repository.py
│   │       └── factor_routes.py
│   └── [other modules...]
├── datasets/
└── server.py                  # FastAPI v13.3.0
```

## What's Been Implemented

### PHASE 13.1 — Alpha Node Registry ✅
- 89 nodes across 9 types

### PHASE 13.2 — Alpha Feature Library ✅
- 308+ features across 8 categories
- 16 transforms

### PHASE 13.3 — Factor Generator (2026-03-11) ✅
**Core Features:**
- **1140+ factors** generated from 308 features
- 8 factor templates
- Feature Selector (category compatibility)
- Factor Combinator
- Factor Constraints (anti-garbage)
- MongoDB persistence

**Factor Templates:**
| Template | Count | Description |
|----------|-------|-------------|
| single_feature | 50 | A |
| pair_feature | 200 | A + B |
| triple_feature | 200 | A + B + C |
| ratio_feature | 190 | A / B |
| difference_feature | 150 | A - B |
| interaction_feature | 200 | A * B |
| regime_conditioned | 150 | A in regime R |
| conditional_feature | - | A if B |

**Factor Families:**
| Family | Count |
|--------|-------|
| momentum | 555 |
| breakout | 240 |
| regime | 150 |
| microstructure | 47 |
| volume | 46 |
| correlation | 44 |
| structure | 40 |
| macro | 13 |
| volatility | 5 |

**API Endpoints (Factor Generator):**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/factor-generator/health` | GET | Health check |
| `/api/factor-generator/stats` | GET | Statistics |
| `/api/factor-generator/run` | POST | Generate factors |
| `/api/factor-generator/generate-batch` | POST | Alias for /run |
| `/api/factor-generator/factors` | GET | List factors |
| `/api/factor-generator/factors/search` | GET | Search factors |
| `/api/factor-generator/families` | GET | Family breakdown |
| `/api/factor-generator/templates` | GET | Template breakdown |
| `/api/factor-generator/runs` | GET | Generation history |
| `/api/factor-generator/{factor_id}` | GET | Get factor |
| `/api/factor-generator/factors` | DELETE | Clear all |

## Test Results
- PHASE 13.1: 21/21 tests passed (100%)
- PHASE 13.2: 95%+ passed
- PHASE 13.3: 48/48 tests passed (100%)

## Alpha Factory Pipeline
```
Feature Library (308 features)
      ↓
Factor Generator (templates + combinator)
      ↓
1140+ Candidate Factors
      ↓
Factor Ranker (NEXT)
      ↓
Alpha Graph / DAG
      ↓
Alpha Deployment
```

## Roadmap

### Completed Phases
- [x] PHASE 13.1 — Alpha Node Registry ✅ (89 nodes)
- [x] PHASE 13.2 — Alpha Feature Library ✅ (308 features)
- [x] PHASE 13.3 — Factor Generator ✅ (1140+ factors)

### Next Phases
- [ ] PHASE 13.4 — Factor Ranker (IC, Sharpe, Decay, Stability)
- [ ] PHASE 13.5 — Alpha Graph (supports/contradicts/amplifies)
- [ ] PHASE 13.6 — Alpha DAG (computational dependencies)
- [ ] PHASE 13.7 — Alpha Deployment

### Future
- PHASE 14 — Meta Portfolio Layer
- PHASE 15 — Risk Intelligence

## Factor Families (Target Mix)
| Family | Current | Target |
|--------|---------|--------|
| trend | 0 | 150 |
| momentum | 555 | 200 |
| breakout | 240 | 150 |
| reversal | 0 | 100 |
| regime | 150 | 150 |
| liquidity | 0 | 100 |
| correlation | 44 | 100 |
| microstructure | 47 | 100 |

## Tech Stack
- Python (FastAPI)
- MongoDB (ta_engine database)
- Pure Python transforms (no pandas required)

## Key Insights
- Factor Generator produces candidate factors, not final signals
- Ranker will filter to ~100-200 approved factors
- DAG will compute factor values in real-time
- Graph will reason about factor relationships
