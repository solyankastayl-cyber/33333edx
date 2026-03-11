# TA Engine PRD - PHASE 13.2 Alpha Feature Library

## Original Problem Statement
TA Engine - Institutional-grade quant trading platform. Building autonomous Alpha Factory for systematic signal generation. PHASE 13.2 implements Feature Library as foundation for Factor Generator that will create 10,000+ factors.

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
│   │   └── feature_library/         # PHASE 13.2 ✅
│   │       ├── feature_types.py     # Feature dataclass, 308 features
│   │       ├── feature_registry.py  # Central registry
│   │       ├── feature_transforms.py # 16 transforms
│   │       ├── feature_repository.py # MongoDB persistence
│   │       └── feature_routes.py    # API endpoints
│   └── [other modules...]
├── datasets/                  # Historical data (BTC, SPX, DXY)
└── server.py                  # FastAPI application v13.2.0
```

## What's Been Implemented

### PHASE 13.1 — Alpha Node Registry (2026-03-11) ✅
- 89 nodes across 9 types
- CRUD API, search, stats

### PHASE 13.2 — Alpha Feature Library (2026-03-11) ✅
**Core Features:**
- **308 features** registered across 8 categories
- 16 transforms available
- MongoDB persistence with indexes
- Full CRUD + Search API
- Transform computation layer

**Feature Categories:**
| Category | Count | Examples |
|----------|-------|----------|
| price | 63 | returns, momentum, zscore, percentile, RSI |
| volatility | 35 | ATR, realized vol, compression, expansion |
| volume | 30 | spikes, profiles, OBV, VWAP |
| liquidity | 33 | orderbook depth, spread, liquidation |
| structure | 25 | BOS, CHOCH, swings, FVG, order blocks |
| microstructure | 30 | flow imbalance, aggression, toxicity |
| correlation | 61 | BTC-SPX, cross-asset, lead-lag |
| context | 31 | funding, OI, macro regime, sessions |

**Transforms Available:**
- raw, lag, difference, pct_change
- rolling_mean, rolling_std
- zscore, percentile_rank, minmax_scale
- log_transform, ratio
- binary_threshold, clip, rank
- ema, sma

**API Endpoints (Feature Library):**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/alpha-features/health` | GET | Health check |
| `/api/alpha-features/stats` | GET | Statistics |
| `/api/alpha-features` | GET | List features |
| `/api/alpha-features/{id}` | GET | Get feature |
| `/api/alpha-features` | POST | Create feature |
| `/api/alpha-features/{id}` | PUT | Update feature |
| `/api/alpha-features/{id}` | DELETE | Deprecate |
| `/api/alpha-features/categories` | GET | Category breakdown |
| `/api/alpha-features/transforms` | GET | Available transforms |
| `/api/alpha-features/search` | GET | Search features |
| `/api/alpha-features/tags` | GET | All unique tags |
| `/api/alpha-features/by-category/{cat}` | GET | Features by category |
| `/api/alpha-features/transform` | POST | Apply transform |
| `/api/alpha-features/{id}/dependencies` | GET | Feature dependencies |

## Test Results
- PHASE 13.1: 21/21 tests passed (100%)
- PHASE 13.2: 95% (minor REST status code issue fixed)
- MongoDB connected and healthy
- All CRUD operations working

## Roadmap

### Completed Phases
- [x] PHASE 13.1 — Alpha Node Registry ✅ (89 nodes)
- [x] PHASE 13.2 — Alpha Feature Library ✅ (308 features)

### Next Phases
- [ ] PHASE 13.3 — Factor Generator (templates, combinator, transformer)
- [ ] PHASE 13.4 — Alpha Graph (logical relationships)
- [ ] PHASE 13.5 — Alpha DAG (computational dependencies)
- [ ] PHASE 13.6 — Factor Ranker
- [ ] PHASE 13.7 — Alpha Deployment

### Future
- PHASE 14 — Meta Portfolio Layer
- PHASE 15 — Risk Intelligence

## Tech Stack
- Python (FastAPI)
- MongoDB (ta_engine database)
- 16 built-in transforms (pure Python)

## Data Pipeline
```
Feature Library (308 features)
      ↓
Factor Generator (templates + combinator)
      ↓
10,000+ Candidate Factors
      ↓
Factor Ranker
      ↓
Alpha Graph / DAG
      ↓
Alpha Deployment
```

## Feature to Factor Flow
Features → raw building blocks
Factors → trading constructs built from features

Example:
- Features: volatility_compression, breakout_pressure, volume_confirmation
- Factor: breakout_quality_factor (combines all three with weights)
