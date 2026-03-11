# TA Engine PRD - PHASE 13.4 Factor Ranker

## Original Problem Statement
TA Engine - Institutional-grade quant trading platform. Building autonomous Alpha Factory for systematic signal generation. PHASE 13.4 implements Factor Ranker that filters 1140+ candidate factors to ~100-200 approved factors.

## Architecture Overview
```
backend/
├── core/database/              # MongoDB Connection
├── modules/alpha_factory/         
│   ├── alpha_types.py           # PHASE 13.1 - 89 nodes
│   ├── alpha_node_registry.py
│   ├── feature_library/         # PHASE 13.2 - 308+ features
│   ├── factor_generator/        # PHASE 13.3 - 1140+ factors
│   └── factor_ranker/           # PHASE 13.4 ✅
│       ├── factor_metrics.py    # IC, Sharpe, Stability, Decay
│       ├── factor_evaluator.py  # Synthetic performance eval
│       ├── factor_ranker.py     # Main ranking engine
│       ├── ranker_repository.py # MongoDB persistence
│       └── ranker_routes.py     # API endpoints
└── server.py                    # FastAPI v13.4.0
```

## What's Been Implemented

### PHASE 13.1 — Alpha Node Registry ✅
- 89 nodes across 9 types

### PHASE 13.2 — Alpha Feature Library ✅
- 315+ features across 8 categories

### PHASE 13.3 — Factor Generator ✅
- 1299+ factors from 8 templates

### PHASE 13.4 — Factor Ranker (2026-03-11) ✅
**Core Features:**
- **1236 factors evaluated**
- **105 approved factors** (4 STRONG + 101 PROMISING)
- 5 metrics: IC, Sharpe, Stability, Decay, Regime Consistency
- Composite score ranking
- Family balance constraint (max 35% per family)

**Metrics:**
| Metric | Description | Thresholds |
|--------|-------------|------------|
| IC | Information Coefficient | ELITE: 0.04+, STRONG: 0.03+, PROMISING: 0.02+ |
| Sharpe | Risk-adjusted returns | ELITE: 1.0+, STRONG: 0.6+, PROMISING: 0.35+ |
| Stability | IC consistency over time | ELITE: 0.65+, STRONG: 0.50+, PROMISING: 0.35+ |
| Decay | IC decay across lags | Lower is better |
| Regime | IC consistency across regimes | Higher is better |

**Verdict Distribution:**
| Verdict | Count | Approved |
|---------|-------|----------|
| ELITE | 0 | Yes |
| STRONG | 4 | Yes |
| PROMISING | 101 | Yes |
| WEAK | 931 | No |
| REJECTED | 200 | No |

**Family Distribution (Approved):**
| Family | Count |
|--------|-------|
| momentum | 49 |
| breakout | 29 |
| regime | 16 |
| microstructure | 4 |
| correlation | 4 |
| volume | 2 |
| structure | 1 |

**API Endpoints:**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/factor-ranker/health` | GET | Health check |
| `/api/factor-ranker/stats` | GET | Statistics |
| `/api/factor-ranker/run` | POST | Run ranking |
| `/api/factor-ranker/evaluate/{id}` | POST | Evaluate single |
| `/api/factor-ranker/rankings` | GET | List rankings |
| `/api/factor-ranker/top` | GET | Top N factors |
| `/api/factor-ranker/approved` | GET | Approved factors |
| `/api/factor-ranker/verdicts` | GET | Verdict breakdown |
| `/api/factor-ranker/runs` | GET | Ranking history |
| `/api/factor-ranker/{factor_id}` | GET | Get ranking |

## Test Results
- PHASE 13.1: 21/21 passed (100%)
- PHASE 13.2: 95%+ passed
- PHASE 13.3: 48/48 passed (100%)
- PHASE 13.4: 14/14 passed (100%)

## Alpha Factory Pipeline (Complete)
```
Feature Library (315 features)
      ↓
Factor Generator (1299 candidates)
      ↓
Factor Ranker (105 approved)    ← CURRENT
      ↓
Alpha Graph (NEXT)
      ↓
Alpha DAG
      ↓
Alpha Deployment
```

## Roadmap

### Completed Phases
- [x] PHASE 13.1 — Alpha Node Registry ✅ (89 nodes)
- [x] PHASE 13.2 — Alpha Feature Library ✅ (315 features)
- [x] PHASE 13.3 — Factor Generator ✅ (1299 factors)
- [x] PHASE 13.4 — Factor Ranker ✅ (105 approved)

### Next Phases
- [ ] PHASE 13.5 — Alpha Graph (relationships: supports/contradicts/amplifies)
- [ ] PHASE 13.6 — Alpha DAG (computational dependencies)
- [ ] PHASE 13.7 — Alpha Deployment

### Future
- PHASE 14 — Meta Portfolio Layer
- PHASE 15 — Risk Intelligence

## Composite Score Formula
```
score = 0.35 * IC_normalized
      + 0.25 * Sharpe_normalized
      + 0.20 * Stability
      + 0.10 * Regime_Consistency
      - 0.10 * Decay_Score
```

## Note on Synthetic Data
Factor evaluation currently uses synthetic data that simulates realistic performance characteristics based on:
- Factor family (microstructure has higher base IC)
- Template complexity (conditional > triple > pair > single)
- Tag quality (momentum, zscore tags boost performance)

In production, this would be replaced with real market data backtests.

## Tech Stack
- Python (FastAPI)
- MongoDB (ta_engine database)
- Pure Python metrics (no pandas/numpy required)
