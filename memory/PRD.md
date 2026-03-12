# TA Engine - Product Requirements Document

## Project Overview
Autonomous Quant Trading System with Alpha Production Machine

## Architecture
- **Backend**: Python FastAPI
- **Database**: MongoDB
- **Core Module**: TA Engine with Alpha Factory

## Phases Completed

### PHASE 13.1 - Alpha Node Registry ✅
- Base alpha nodes and types
- Registry management
- MongoDB persistence

### PHASE 13.2 - Feature Library ✅
- 307 base features
- Feature transforms
- Feature repository

### PHASE 13.3 - Factor Generator ✅
- 1141 candidate factors generated
- 7 factor templates
- Family-based organization

### PHASE 13.4 - Factor Ranker ✅
- 102 approved factors
- Multi-criteria evaluation (IC, Sharpe, Stability)
- Verdict system (ELITE, STRONG, PROMISING)

### PHASE 13.5 - Alpha Graph ✅
- Logical factor relationships
- Support/Conflict/Amplify edges
- Coherence reasoning

### PHASE 13.6 - Alpha DAG ✅
- Computational dependency graph
- ~293 nodes, ~495 edges
- ~2ms execution time

### PHASE 13.7 - Alpha Deployment ✅ (Current)
- 23 deployed factors (5 active, 18 shadow)
- Live signal generation
- Safety layer with shadow mode
- Auto-pause rules
- Full API coverage

## Key Metrics (Phase 13.7)
- Total Deployed: 23 factors
- Active: 5 factors
- Shadow: 18 factors
- Signals (24h): 7+
- Average IC: 0.0533
- Average Sharpe: 0.57

## API Endpoints
- `/api/alpha-deployment/select` - Select factors for deployment
- `/api/alpha-deployment/deploy/{id}` - Deploy specific factor
- `/api/alpha-deployment/activate/{id}` - Activate from shadow
- `/api/alpha-deployment/pause/{id}` - Pause deployment
- `/api/alpha-deployment/signals/generate` - Generate live signals
- `/api/alpha-deployment/signals/{symbol}` - Get signals by symbol
- `/api/alpha-deployment/safety/scan` - Run safety scan
- `/api/alpha-deployment/stats` - Get statistics

## MongoDB Collections
- `alpha_deployments` - Deployed factors
- `alpha_signals_live` - Live signals (TTL: 24h)
- `alpha_deployment_history` - Decision history
- `alpha_deployment_snapshots` - State snapshots

## Exchange Audit Completed
- Full comparative analysis: current project vs FOMO-SEOFv1.69
- Report: `/app/EXCHANGE_AUDIT_REPORT.md`
- Extraction Matrix: `/app/EXTRACTION_MATRIX.md`

### PHASE 13.8 - Exchange Intelligence Module DONE
- 5 engines: FundingOI, DerivativesPressure, Liquidation, ExchangeFlow, Volume
- ExchangeContext aggregator with composite bias scoring
- 8 API endpoints tested (40/40 tests passed)
- Derives proxy signals from candle data, ready for live exchange data

## Next Phases
- PHASE 13.8.1 - Production Safeguards (URI + Drift Detection from FOMO)
- PHASE 13.9 - Trading Decision Layer (TA + Exchange context -> decisions)
- PHASE 14 - Meta Portfolio Layer
- PHASE 15 - Risk Intelligence

## Date Updated
2026-02-27
