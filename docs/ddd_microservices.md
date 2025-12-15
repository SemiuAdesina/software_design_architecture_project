Title: Domain-Driven Design and Microservices Architecture for EasyParkPlus

## Core Domain and Subdomains
- Core domain: Parking Operations Management (allocation, occupancy, EV charging orchestration)
- Supporting subdomains: Payments & Billing, Customer Accounts, Facility Inventory, Notifications, Reporting/Analytics

## Bounded Contexts and Ubiquitous Language
- Parking Context
  - Terms: ParkingLot, Level, Slot, Allocation, Occupancy, Ticket, Leave
  - Rules: EV vehicles must occupy EV slots; non-EV may not park in EV slots
- EV Charging Context
  - Terms: Charger, Connector, ChargingSession, StateOfCharge (SoC), Tariff, Meter
  - Rules: A ChargingSession is bound to one Vehicle and one Connector at a time
- Customer Context
  - Terms: Customer, VehicleProfile, Subscription, PaymentMethod
- Billing Context
  - Terms: Invoice, ChargeItem, RatePlan, Tax, Refund
- Notifications Context
  - Terms: Event, Template, Channel (Email/SMS/Push), Delivery

## Domain Model Sketches (Entities / Value Objects / Aggregates)
- Parking Context
  - Aggregates: ParkingLot (owns Slots), Ticket (check-in/check-out data)
  - Entities: Slot{id, isEV, status, vehicleRef}, ParkingLot{id, level, regularCapacity, evCapacity}
  - Value Objects: RegistrationNumber, Color, MakeModel
- EV Charging Context
  - Aggregates: ChargingStation (owns Chargers), ChargingSession (lifecycle: start/stop)
  - Entities: Charger{id, status, connectorType}, ChargingSession{id, vehicleReg, kWh, startTs, endTs}
  - Value Objects: TariffId, MeterReading, SOC
- Customer Context
  - Aggregates: Customer (owns VehicleProfiles, PaymentMethods)
  - Entities: Customer{id, name, contact}, VehicleProfile{registration, type}, PaymentMethod{token}
- Billing Context
  - Aggregates: Invoice (owns ChargeItems)
  - Entities: Invoice{id, customerId, total, status}, ChargeItem{type, qty, unitPrice}

## Context Map (Relationships)
- Parking → emits ParkingEvents (VehicleParked, VehicleLeft)
- EV Charging subscribes to VehicleParked (EV) to propose start of ChargingSession; emits ChargingSessionStarted/Ended
- Billing subscribes to ParkingEvents and ChargingSessionEnded to calculate charges → emits InvoiceCreated
- Notifications subscribes to InvoiceCreated and Charging thresholds
- Customer provides customer/vehicle data to other contexts via API lookup

## Microservices Architecture
- Services (align to bounded contexts)
  1) parking-service
     - Responsibilities: lot/slot management, allocation, occupancy, search
     - DB: PostgreSQL (lots, slots, tickets, indexes on registration, color)
  2) ev-charging-service
     - Responsibilities: charger inventory, session lifecycle, metering, tariffs
     - DB: PostgreSQL (stations, chargers, sessions, tariffs); time-series store optional for meter reads
  3) customer-service
     - Responsibilities: customers, vehicle profiles, auth linkage
     - DB: PostgreSQL (customers, vehicles)
  4) billing-service
     - Responsibilities: rating, invoicing, payments orchestration
     - DB: PostgreSQL (invoices, items, payments); integrates with payment gateway
  5) notification-service
     - Responsibilities: templating, multi-channel delivery
     - DB: PostgreSQL (templates, deliveries)
  6) reporting-service (optional)
     - Responsibilities: analytical summaries
     - DB: Warehouse/OLAP; fed by CDC/ETL

## APIs/Endpoints (external and service-to-service)
- parking-service (HTTP+JSON)
  - POST /lots {level, capacityRegular, capacityEv}
  - POST /lots/{lotId}/park {reg, make, model, color, type, isEv}
  - POST /lots/{lotId}/leave {slotNumber, isEv}
  - GET /lots/{lotId}/status
  - Events (pub): VehicleParked, VehicleLeft
- ev-charging-service
  - POST /stations {name, location}
  - POST /sessions/start {reg, stationId, connectorId}
  - POST /sessions/{sessionId}/stop
  - GET /sessions/{sessionId}
  - Events (sub): VehicleParked(EV); (pub): ChargingSessionStarted, ChargingSessionEnded
- customer-service
  - GET /customers/{id}
  - GET /vehicles/{reg}
- billing-service
  - POST /invoices {customerId, items}
  - GET /invoices/{id}
  - Events (sub): VehicleLeft, ChargingSessionEnded; (pub): InvoiceCreated, PaymentReceived
- notification-service
  - POST /deliver {channel, recipient, templateId, data}
  - Events (sub): InvoiceCreated

## Databases per Service
- Separate schemas/databases; no cross-service DB access
- Referential integrity maintained via IDs and events, not foreign keys across services

## Async Integration & Events
- Broker: Kafka or RabbitMQ
- Topics: parking.events, charging.events, billing.events, notifications.events
- Event examples:
  - VehicleParked {lotId, slotNumber, reg, isEv, ts}
  - VehicleLeft {lotId, slotNumber, reg, isEv, duration, ts}
  - ChargingSessionEnded {sessionId, reg, kWh, duration, tariffId, ts}
  - InvoiceCreated {invoiceId, customerId, total, ts}

## EV Charging Extension Notes
- Charging sessions tied to parking occupancy; enforce charger availability per slot/connector
- Dynamic tariffs by time-of-day; peak pricing via billing-service
- SoC-based notifications (e.g., 80% reached) via notification-service

## Non-Functional Concerns
- Scalability: stateless services with horizontal autoscaling; DB read replicas as needed
- Resilience: circuit breakers, retries, idempotency keys for events and payments
- Observability: structured logs, metrics (Prometheus), tracing (OpenTelemetry)
- Security: OAuth2/OpenID Connect at API gateway; per-service authZ; PII encryption
- Data: GDPR/CCPA deletion flows; event retention policies; schema versioning (Avro/Protobuf)

## Deployment Topology
- API Gateway → Services in containers (Kubernetes)
- Message broker cluster, per-service DB instances
- CI/CD pipelines with contract tests (API + event schemas)
