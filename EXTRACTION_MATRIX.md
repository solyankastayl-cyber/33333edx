# EXTRACTION MATRIX: FOMO-SEOFv1.69 → Текущий проект

**Дата:** Февраль 2026  
**Архитектурный вердикт:** Точечный extraction, НЕ массовый перенос

---

## Корзина 1: ПЕРЕНОСИМ СРАЗУ (P0)

| Компонент из FOMO | Куда в новой архитектуре | Приоритет | Статус |
|-------------------|--------------------------|-----------|--------|
| **Reliability Index (URI)** | Adaptive Intelligence / System Intelligence / Alpha Deployment Safety | P0 | Ожидает |
| **Drift Detection (PSI + EMA)** | Adaptive Intelligence / Alpha Factory | P0 | Ожидает |
| **Funding / OI Engine** | Exchange Intelligence Layer | P0 | Ожидает |
| **Derivatives Pressure Engine** | Exchange Intelligence Layer | P0 | Ожидает |
| **Liquidation / Exchange Flow Engine** | Exchange Intelligence Layer | P0 | Ожидает |

---

## Корзина 2: ПЕРЕНОСИМ ПОЗЖЕ (P1-P2)

| Компонент из FOMO | Куда в новой архитектуре | Приоритет | Статус |
|-------------------|--------------------------|-----------|--------|
| **Simulation Engine (capital-centric куски)** | Risk / Portfolio Research | P2 | Отложено |
| **Whale / Event Detectors** | Exchange Intelligence Layer | P2 | Отложено |
| **Отдельные exchange patterns** | Feature Library (если не покрыты) | P2 | Отложено |
| **Exchange Volume Context** | Exchange Intelligence Layer | P1 | Отложено |

---

## Корзина 3: НЕ ПЕРЕНОСИМ

| Компонент из FOMO | Причина |
|-------------------|---------|
| **Prediction API** (Python 7 эндпоинтов) | Другой контур (predictive, не trading) |
| **Chart / UI services** (10 файлов) | Не нужны для trading brain |
| **Combined boost system** (0.7–1.3) | Слишком примитивно, заменено Alpha Graph/DAG/Ranker |
| **Predictive MetaBrain** | Живёт в predictive contour отдельно |
| **Старые 40+ индикаторов** (если покрыты Feature Library) | Дублирование |
| **Старые regime/context engines целиком** | Уже есть Market Context, Regime Engine, Correlation, Liquidity |

---

## Корзина 4: ИСПОЛЬЗУЕМ КАК REFERENCE ONLY

| Компонент из FOMO | Что взять |
|-------------------|-----------|
| **Старые aggregate coefficients** | Логику взвешивания как идею |
| **Старый meta verdict logic** | Паттерны принятия решений |
| **Regime baselines** | Формат хранения и threshold'ы |

---

## ПЛАН ИНТЕГРАЦИИ

### PHASE 13.8 — Exchange Intelligence Layer
**Цель:** Встроить exchange-native engines в текущую trading-архитектуру

Структура:
```
modules/exchange_intelligence/
  funding_oi_engine.ts         — funding rate + OI pressure analysis
  derivatives_pressure.ts      — derivatives market pressure signals
  exchange_liquidation.ts      — liquidation flow / cascade detection
  exchange_flow.ts             — exchange-specific order flow context
  exchange_volume_context.ts   — volume anomalies + context
  exchange_context_aggregator.ts — агрегатор всех exchange signals
  types.ts
  index.ts
```

### PHASE 13.8.1 — Production Safeguards (URI + Drift)
**Цель:** Встроить reliability и drift monitoring

Структура:
```
modules/adaptive_intelligence/
  reliability/
    reliability_index.ts       — URI (4 компонента)
    data_health.ts
    drift_health.ts
    capital_health.ts
    calibration_health.ts
    types.ts
  drift/
    drift_detector.ts          — PSI computation
    drift_stabilizer.ts        — EMA smoothing
    drift_baseline.ts          — baseline versioning
    types.ts
```

### PHASE 13.9 — Trading MetaBrain
**Цель:** Объединить TA intelligence + Exchange Intelligence

```
modules/trading_metabrain/
  ta_intelligence_adapter.ts
  exchange_intelligence_adapter.ts
  trading_metabrain.ts         — unified trading context
  types.ts
```
