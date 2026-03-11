# АУДИТ И СРАВНИТЕЛЬНЫЙ АНАЛИЗ: Модуль Exchange

**Дата:** Февраль 2026  
**Текущий проект:** `/app/backend/src/modules/exchange*`  
**Референсный проект:** `FOMO-SEOFv1.69` (GitHub)

---

## 1. ОБЩАЯ АРХИТЕКТУРА

Оба проекта используют **идентичную базовую архитектуру**: TypeScript + Fastify + MongoDB + Mongoose. Exchange-логика разделена на три основных модуля:

| Модуль | Текущий проект | FOMO-SEOFv1.69 |
|--------|---------------|----------------|
| `exchange/` | 30+ подмодулей | 30+ подмодулей (идентичная структура) |
| `exchange-ml/` | 14 подмодулей | 18 подмодулей (+chart, +drift, +reliability, +admin snapshots) |
| `exchange-alt/` | 22 подмодуля | 22 подмодуля (идентичная структура) |
| `exchange-sim/` | **НЕ СУЩЕСТВУЕТ** | Полный модуль симуляции |
| Python-слой | **НЕ СУЩЕСТВУЕТ** | `prediction_exchange_routes.py` + `exchange_health.py` |

---

## 2. ИДЕНТИЧНЫЕ КОМПОНЕНТЫ (100% совпадение)

Следующие файлы и модули **полностью идентичны** в обоих проектах:

### 2.1 Exchange Core (`exchange/`)
- `index.ts` — регистрация модуля, 319 строк, идентичная логика
- `models/exchange.types.ts` — контракты данных (ExchangeMarketSnapshot, OrderBookSnapshot, TradeFlowSnapshot, OpenInterestSnapshot, LiquidationEvent, MarketRegime, ExchangeOverview, ExchangeConfig)
- `models/exchange.model.ts` — Mongoose-схемы
- `exchange-data.service.ts` — polling, кэширование, read-only API

### 2.2 Подмодули Exchange (одинаковая структура и файлы)
- `order-flow/` — анализ потока ордеров (analyzer, imbalance calculator, absorption detector)
- `regimes/` — детекция рыночных режимов (indicator-detector, service)
- `liquidations/` — каскадные ликвидации (detector, service)
- `patterns/` — паттерны (library, detector, indicator-detector)
- `observation/` — наблюдения (builder, storage, service)
- `indicators/` — индикаторы (registry, service, snapshot, aggregates, calculators/)
- `labs/` — исследования (attribution, explainability, alerting, historical, canonical, pattern-risk, regime-attribution, regime-forward, sentiment-interaction, whale-risk)
- `providers/` — провайдеры бирж (binance/, coinbase/, okx, bybit, mock, base, registry, selector, health)
- `whales/` — китовая активность (state, storage, ingest, mock, patterns/)
- `funding/` — фандинг (service, normalizer, context classifier, registry, store, adapters/, routes/, services/)
- `screener/` — скринер альткоинов (candidates, feature builder, labeler, pattern space, similarity, winner memory, ml/)
- `macro/` — макро-оверлей (state service, funding overlay, cluster context)
- `sector/` — ротация секторов (state, wave, asset tags)
- `universe/` и `universe-v2/` — сканер юниверса
- `snapshots/` — снэпшоты (builder, features, db)
- `clustering/` — кластеризация паттернов (kmeans, vector builder, feature stats)
- `candidates/` — alt movers / returns
- `intelligence/` — signal intelligence
- `admin/` — админ-контроль
- `cache/` — market cache
- `context/`, `verdict/`, `data/`, `ws/`, `backfill/`, `freeze/`, `forecast/`, `jobs/`, `routes/`

### 2.3 Exchange-ML (общие компоненты)
- `ml.types.ts`, `featureExtractor.ts`, `labeler.ts`, `ml.service.ts`, `ml.trainer.ts`
- `ml.comparison.ts`, `model.registry.ts`, `macroFeatureExtractor.ts`
- `ml.shadow.training.ts`, `ml.modifier.service.ts`, `ml.promotion.service.ts`
- `ml.shadow.monitor.service.ts`, `exchange.verdict.service.ts`
- `dataset/`, `jobs/`, `training/`, `shadow/`, `lifecycle/` (базовые файлы), `performance/`, `perf/`, `config/`, `contracts/`, `snapshots/`, `segments/`, `iteration/`

### 2.4 Exchange-Alt (полностью идентичный)
Все 22 подмодуля совпадают: adapters, alt-opps, alt-sets, clustering, context, db, explain, failure, gating, indicators, jobs, meta-brain, ml, ml-overlay, pattern-memory, portfolio, portfolio-construct, portfolio-filter, propagation, ranking, replay, routes, sector-regime, shadow, strategy-survival, tuning, universe, validation.

---

## 3. КОМПОНЕНТЫ, ПРИСУТСТВУЮЩИЕ ТОЛЬКО В FOMO

### 3.1 Модуль `exchange-sim/` (Симуляция ML-моделей)

**Статус:** Полностью отсутствует в текущем проекте  
**Важность:** ВЫСОКАЯ (капитал-центричная валидация)

**Структура:**
```
exchange-sim/
  core/
    exchange_sim_config.ts    — конфигурация и diagnostic gates
    exchange_sim_runner.ts    — основной runner симуляции
    sim_audit_logger.ts       — аудит-логгирование
    sim_config.ts             — загрузка конфига из ENV
    sim_db.ts                 — изолированная БД для симуляции
    sim_now_provider.ts       — провайдер виртуального времени
  providers/
    sim_price_provider.ts     — провайдер исторических цен
    static_historical_provider.ts
  reporters/
    sim_reporter.ts           — отчёты (JSON, CSV)
  routes/
    exchange_sim_admin.routes.ts
  utils/
    trade_evaluator.ts        — оценка сделок
  exchange_sim.types.ts       — типы (SimConfig, TradeEvaluation, SimEquityMetrics, SimReport)
  index.ts
```

**Ключевые возможности:**
- **Capital-Centric подход**: TradeWinRate, Equity curve, MaxDrawdown, Sharpe-like ratio
- **ENV + DIR разделение**: Environment-модель (USE/WARNING/IGNORE) + Direction-модель (UP/DOWN/NEUTRAL)
- **Diagnostic Modes**: baseline, retrain_only, lifecycle
- **Kill switch**: через ENV и MongoDB-флаги
- **Изолированная БД**: суффикс `_sim` для неинвазивного тестирования
- **Подробные метрики**: accuracy по горизонтам, tradeStats, equityMetrics, envAccuracy, dirAccuracy, lifecycle, shadow, bias, stress, correlations

---

### 3.2 `exchange-ml/chart/` (UI-визуализация)

**Статус:** Полностью отсутствует в текущем проекте  
**Важность:** СРЕДНЯЯ (фронтенд-сервисы)

**Файлы:**
| Файл | Назначение |
|------|-----------|
| `exchange-chart-v2.service.ts` | Построение чарт-данных v2 |
| `exchange-chart-v3.service.ts` | Чарт-данные v3 (rolling forecasts) |
| `exchange-chart-v2.types.ts` | Типы для чартов v2 |
| `exchange-chart-v3.types.ts` | Типы для чартов v3 |
| `exchange-equity-v2.service.ts` | Equity curve данные |
| `exchange-performance-v2.service.ts` | Performance-метрики для UI |
| `exchange-top-alts-v2.service.ts` | Топ-альткоины для дашборда |
| `exchange-ui-adjustments.ts` | UI-адаптации |
| `exchange-ui-v2.routes.ts` | API-роуты для UI v2 |
| `forecast-evolution.service.ts` | Эволюция прогнозов |

---

### 3.3 `exchange-ml/drift/` (Drift Detection & Stabilization)

**Статус:** Полностью отсутствует в текущем проекте  
**Важность:** ВЫСОКАЯ (стабильность ML-моделей)

**Файлы:**
| Файл | Назначение |
|------|-----------|
| `exchange-drift-baseline.model.ts` | Mongoose-модель baseline |
| `exchange-drift-baseline.service.ts` | Сервис создания/управления baseline'ами |
| `exchange-drift-stabilizer.service.ts` | Стабилизатор drift (EMA-сглаживание PSI) |
| `exchange-drift-state.model.ts` | Модель текущего состояния drift |
| `exchange-drift.routes.ts` | Admin API (6 эндпоинтов) |

**Ключевая логика:**
- **PSI (Population Stability Index)**: отслеживание сдвига распределения фичей
- **EMA-сглаживание**: устранение шумовых срабатываний
- **Статусы**: OK → WARN → DEGRADED → CRITICAL
- **Streaks**: подсчёт последовательных предупреждений
- **Baseline gates**: минимальные пороги для auto/manual создания baseline (URI, capitalHealth, driftHealth, minTrades)
- **Cooldown**: минимальный период между baseline'ами

**API эндпоинты:**
- `GET /baseline/latest` — последний baseline
- `GET /baseline/history` — история версий
- `POST /baseline/create` — создание нового baseline
- `GET /baseline/gates` — текущие пороги
- `GET /stabilizer/status` — состояние стабилизатора
- `POST /stabilizer/run` — ручной запуск
- `POST /stabilizer/reset` — сброс streaks

---

### 3.4 `exchange-ml/reliability/` (Unified Reliability Index)

**Статус:** Полностью отсутствует в текущем проекте  
**Важность:** КРИТИЧЕСКАЯ (защита от деградации)

**Файлы:**
| Файл | Назначение |
|------|-----------|
| `exchange-reliability.service.ts` | Основной сервис расчёта URI |
| `exchange-reliability.types.ts` | Типы (уровни, действия, статус) |
| `exchange-reliability.routes.ts` | Admin API |
| `exchange-price-provider-health.service.ts` | Мониторинг здоровья провайдера цен |

**Формула URI:**
```
URI = 0.30 * DataHealth + 0.30 * DriftHealth + 0.25 * CapitalHealth + 0.15 * CalibrationHealth
```

**Уровни и действия:**

| Уровень | Порог | Workers | Training | Promotion | Confidence | Size |
|---------|-------|---------|----------|-----------|------------|------|
| OK | >= 0.75 | Открыты | Открыт | Открыт | 1.0x | 1.0x |
| WARN | 0.60-0.75 | Открыты | Открыт | **БЛОК** | 0.85x | 0.80x |
| DEGRADED | 0.40-0.60 | Открыты | **БЛОК** | **БЛОК** | 0.70x | 0.50x |
| CRITICAL | < 0.40 | **БЛОК** | **БЛОК** | **БЛОК** | 0.50x | 0.25x |

**Компоненты здоровья:**
- **DataHealth**: проверка провайдера цен (свежесть, доступность)
- **DriftHealth**: из exchange_drift_state (EX-S3 стабилизатор)
- **CapitalHealth**: из торговых записей (PnL, MaxDD, Sharpe-like)
- **CalibrationHealth**: shadow vs active accuracy

**Специальное правило:** Если CapitalHealth < 50% → Training блокируется независимо от URI-уровня

---

### 3.5 Дополнительные файлы в `exchange-ml/lifecycle/`

**Статус:** Отсутствуют в текущем проекте

| Файл | Назначение |
|------|-----------|
| `exchange_capital.routes.ts` | API для capital-метрик |
| `exchange_capital_guard.ts` | Capital guard (защита от потерь) |
| `exchange_capital_window.service.ts` | Скользящее окно capital-метрик |

---

### 3.6 Дополнительные файлы в `exchange-ml/admin/`

| Файл | Назначение |
|------|-----------|
| `exchange-admin-snapshot.routes.ts` | Admin API для снэпшотов |
| `exchange-admin-snapshot.service.ts` | Сервис управления снэпшотами |
| `exchange-admin-snapshot.types.ts` | Типы |

---

### 3.7 Python Prediction Layer (`prediction_exchange_routes.py`)

**Статус:** Полностью отсутствует в текущем проекте  
**Важность:** ВЫСОКАЯ (пользовательские API)

**1028 строк Python/FastAPI** с 7 эндпоинтами:

| Эндпоинт | Назначение |
|----------|-----------|
| `GET /api/prediction/exchange/forecast` | Прогноз по горизонтам (24H, 7D, 30D) + ценовой ряд |
| `GET /api/prediction/exchange/alts` | Скоринг альткоинов (z-score нормализация) |
| `GET /api/prediction/exchange/top-signals` | Компактные сигналы из verdicts |
| `GET /api/prediction/exchange/model-health` | Здоровье модели по горизонтам |
| `GET /api/prediction/exchange/graph` | Forecast segments + price chart |
| `GET /api/prediction/exchange/graph3` | Rolling forecast evolution (clean) |
| `GET /api/prediction/exchange/graph4` | Rolling expectation curve + band data |
| `GET /api/prediction/exchange/live-price` | Live цена (Binance → CoinPaprika fallback) |

**Ключевые алгоритмы:**
- **Z-score нормализация**: `0.5 + (v - mean) / std / 4` для universe scoring
- **Composite Score**: `0.45 * momentum + 0.35 * liquidity + 0.20 * derivatives`
- **Risk Profile**: upside/neutral/downside probabilities, worst/best case, volatility
- **Band forecasting** (30D): median target, core band (P25-P75), wide band (P10-P90) с shrinkage
- **ETA to Target**: средние дни до достижения цели с коррекцией на ошибку
- **Drift/regime integration**: текущий режим, confidence, regime baselines

---

### 3.8 Python Exchange Health (`exchange_health.py`)

**Статус:** Полностью отсутствует в текущем проекте  
**Важность:** СРЕДНЯЯ

**226 строк**, проверяющие:
- MongoDB connectivity
- Node.js backend availability (порт 8003)
- System resources (RAM, CPU через psutil)
- Radar V11 engine (universe counts)
- Pipeline freshness (stale detection)
- Cache + rate limiter metrics

**Статусы:** HEALTHY → DEGRADED → CRITICAL

---

### 3.9 `exchange/data/universe_loader.service.ts`

**Статус:** Отсутствует в текущем проекте  
**Важность:** СРЕДНЯЯ

Priority-based загрузчик юниверса:
- **P1**: Top alpha по alphaScore (exchange_symbol_universe_alpha_dynamic)
- **P2**: Top по объёму (exchange_symbol_snapshots)
- **P3**: Remainder (exchange_symbol_universe)

---

## 4. МОДУЛИ, ПРИСУТСТВУЮЩИЕ ТОЛЬКО В ТЕКУЩЕМ ПРОЕКТЕ

Следующие модули **не имеют аналогов в FOMO**:

| Модуль | Назначение |
|--------|-----------|
| `admin_control/` | Админ-команды (validate, dry-run, execute, rollback, audit) |
| `analysis_mode/` | Режимы анализа |
| `autopilot/` | Автопилот |
| `calibration/` | Калибровка моделей |
| `context/` | Контекстный модуль |
| `coverage/` | Покрытие |
| `dashboard/` | Дашборд (collector, types, routes) |
| `digital_twin/` | Цифровой двойник (reactor, consistency, tree builder, counterfactual) |
| `discovery/` | Открытие паттернов (analyzer, generator, dataset) |
| `edge/` + `edge_intelligence/` + `edge_validation/` | Edge-анализ (multiplier, buckets, aggregator, rebuild) |
| `execution/` | Исполнение (portfolio, risk, plan, position) |
| `fractal_engine/` | Фрактальный движок (signature, discovery, storage) |
| `governance/` | Управление |
| `incremental/` | Инкрементальный движок (graph) |
| `indicators/` (standalone) | RSI, OI, macro, volume-profile |
| `liquidity/` | Ликвидность (detector, service) |
| `marketState/` | Состояние рынка |
| `market_graph/` | Графы рынка (transitions, extractor) |
| `market_map/` | Карта рынка (tree, heatmap, timeline) |
| `market_memory/` | Память рынка (vector, search, snapshot, boost) |
| `market_physics/` | Физика рынка (compute) |
| `memory_index/` | Индекс памяти |
| `metabrain/` + `metabrain_v3/` + `metabrain_learning/` + `metabrain_memory/` + `metabrain_regime/` | MetaBrain экосистема (policy, context, optimizer, gating, learning, memory policies, regime learning) |
| `mtf_v2/` | Multi-timeframe v2 (alignment, context) |
| `outcomes/` | Оценка исходов |
| `portfolio/` | Портфель (state, risk, correlation, exposure) |
| `realtime/` | Реал-тайм (hub, broadcast, publishers, channels, simulator) |
| `regime/` | Режим-движок (classifier, features) |
| `scenario_engine/` | Сценарии (generator, simulator, scoring) |
| `scheduler/` | Планировщик бэктестов |
| `state_engine/` | Движок состояния |
| `strategy/` + `strategy_builder/` | Стратегии (registry, backtest, filter, generator, simulator) |
| `structure_ai/` | Структурный AI (detector, chain) |
| `ta/` | **Огромный** модуль TA (ml, scoring, calibration, regime, replay, stream, batch, metrics, graph, patterns, runtime, gates, geometry, simulator, quality, stability, risk, projection, hypothesis, hardening, aggregation, phase4 — 50+ подмодулей) |

---

## 5. МОДУЛИ, УНИКАЛЬНЫЕ ДЛЯ FOMO (не-Exchange)

| Модуль | Назначение |
|--------|-----------|
| `exchange-sim/` | Симуляция (см. раздел 3.1) |
| `meta-brain-v2/` | MetaBrain v2 с exchange provider |
| `chains/` | Chain-модуль |
| `narratives/` | Нарративы |
| `onchain-lite/` | Лёгкий onchain |
| `onchain_v2/` | Onchain v2 (cex_registry) |
| `sentiment-ml/` | ML для сентимента |
| `system/` | Системный модуль |

---

## 6. ТЕХНИЧЕСКИЕ РАЗЛИЧИЯ

### 6.1 Стек

| Аспект | Текущий проект | FOMO-SEOFv1.69 |
|--------|---------------|----------------|
| Основной язык | TypeScript | TypeScript + Python |
| Backend framework | Fastify | Fastify + FastAPI |
| Python-слой | Отсутствует | prediction_exchange_routes, exchange_health, forecast/, radar_v11/ |
| Архитектура | Моносервис | Dual-process (Node + Python) |

### 6.2 ML Pipeline

| Аспект | Текущий проект | FOMO-SEOFv1.69 |
|--------|---------------|----------------|
| Drift detection | Нет | PSI + EMA стабилизатор |
| Reliability Index | Нет | URI (4 компонента, 4 уровня) |
| Capital metrics | Нет | MaxDD, Sharpe, equity curve |
| Simulation | Нет | Полная offline-симуляция |
| ENV/DIR separation | Нет | Environment + Direction модели |
| Chart services | Нет | 10 файлов для UI-визуализации |

### 6.3 Мониторинг

| Аспект | Текущий проект | FOMO-SEOFv1.69 |
|--------|---------------|----------------|
| Provider health | providerStatusCache (in-memory) | Price provider health service + URI |
| System health | Нет | exchange_health.py (MongoDB, Node, RAM, CPU) |
| Pipeline freshness | Нет | Stale detection с порогами |
| Drift monitoring | Нет | Drift state + baseline versioning |

---

## 7. РЕКОМЕНДАЦИИ ПО ИНТЕГРАЦИИ (приоритизация)

### P0 — Критические (нужны для production)
1. **`exchange-ml/reliability/`** — Unified Reliability Index. Без этого модуля ML-система может деградировать незаметно. Формула чёткая, реализация самодостаточная.
2. **`exchange-ml/drift/`** — Drift Detection. Связан с reliability, обеспечивает раннее обнаружение деградации модели.

### P1 — Высокий приоритет
3. **`exchange-sim/`** — Simulation Engine. Позволяет валидировать модели до деплоя в production. Capital-centric метрики критичны для оценки реальной полезности.
4. **`exchange-ml/lifecycle/` расширения** — Capital guard, capital window. Защита от необратимых потерь.

### P2 — Средний приоритет
5. **`prediction_exchange_routes.py`** (или TypeScript-аналог) — пользовательские API для прогнозов, графиков, сигналов.
6. **`exchange-ml/chart/`** — UI-сервисы для визуализации.
7. **`exchange/data/universe_loader.service.ts`** — приоритизированная загрузка юниверса.

### P3 — Низкий приоритет
8. **`exchange_health.py`** — системный мониторинг (может быть заменён TypeScript-эквивалентом).
9. **`exchange-ml/admin/` расширения** — дополнительные admin-снэпшоты.

---

## 8. ВЫВОДЫ

### Совпадающий код (~90% Exchange core)
Базовый модуль Exchange **практически идентичен** в обоих проектах. Это включает:
- Все модели данных и контракты
- Все провайдеры бирж (Binance, Bybit, OKX, Coinbase, Mock)
- Все подмодули (order flow, regimes, liquidations, patterns, observation, indicators, labs, whales, funding, screener, macro, sector, universe, snapshots, clustering, candidates, intelligence)
- Основной ML-пайплайн (dataset, training, shadow, lifecycle, performance)

### Ключевые расхождения
FOMO-SEOFv1.69 продвинулся дальше в направлении **production-ready ML operations**:
1. **Reliability + Drift**: полный стек мониторинга здоровья ML-системы
2. **Simulation**: offline-валидация перед деплоем
3. **Capital-centric метрики**: фокус на реальный P&L вместо accuracy
4. **Python prediction layer**: богатый API для пользователей

Текущий проект, в свою очередь, имеет **значительно более развитую аналитическую инфраструктуру**:
1. **MetaBrain экосистема**: 5 модулей MetaBrain с learning, memory, regime
2. **TA Engine**: огромный модуль с 50+ подмодулями
3. **Edge/Fractal/Digital Twin**: продвинутые аналитические движки
4. **Strategy Builder/Execution**: полная цепочка от стратегии до исполнения
5. **Portfolio/Risk**: развитый риск-менеджмент
6. **Realtime**: полноценный WebSocket hub

**Вывод**: Оба проекта разошлись в разных направлениях от общей кодовой базы Exchange. FOMO фокусируется на MLOps/reliability, текущий проект — на аналитическую глубину и принятие решений.
