Title: Design Improvements and Pattern Justification

Overview
The baseline Parking Lot Manager mixed domain logic with tkinter UI, used parallel integer counters for slots, had duplicated search logic, and contained several bugs (e.g., wrong classes for motor vs car, EV regular assignment confusions, inconsistent method params, typos like getSlotNumFromMakeEv using undefined 'make'). Our goals were to separate concerns, introduce tested creation/allocation mechanisms, and prepare the design for EV charging extension.

Identified Anti-Patterns and Fixes
- God Object / Feature Envy in ParkingLot (GUI calls directly into domain and handles text output)
  - Fix: Introduced MVC. Domain models in src/redesign/models, controller mediates, view handles UI only.
- Duplicated logic for lookups (by color/make/model/reg) across EV and non-EV arrays
  - Fix: Unified domain model and provided clean data structures; would expose query services (omitted for brevity).
- Primitive Obsession and magic flags (ev=1, motor=1)
  - Fix: Replaced with typed models and factory methods that encode type at creation.
- Global state / side effects (module-level tkinter vars, tfield inside domain method)
  - Fix: Removed I/O from domain; view prints messages, controller returns values.
- Incorrect class usage bugs (e.g., motorcycle stored via Vehicle.Car when motor==1; EV getters/undefined vars)
  - Fix: Corrected via distinct model classes and factories.
- Inconsistent responsibilities (ParkingLot both allocates and renders status)
  - Fix: ParkingLot purely manages state; rendering moved to view.

Applied Design Patterns
Pattern 1: Factory (Simple Factory)
- Problem: Many conditional branches to instantiate specific vehicle types (EV vs non-EV, car vs bike).
- Why this pattern: Centralizes creation logic, reduces duplication and flag errors, eases future types (e.g., Bus, EV Truck).
- Implementation: `factories/vehicle_factory.py` exposes `create_vehicle` and `create_electric` returning typed instances.
- Benefits: Cleaner controller/view, fewer conditionals, easier testing and extension.

Pattern 2: Strategy (Allocation Strategy)
- Problem: Allocation logic tied to ParkingLot and UI flags; difficult to change rules (e.g., prioritize EV, reserve last N slots).
- Why this pattern: Encapsulates allocation algorithms and allows swapping without changing controller or models.
- Implementation: `strategies/allocation_strategy.py` with `RegularFirstStrategy` and `ElectricOnlyStrategy` (extensible to reserved/nearest-level strategies).
- Benefits: Open/closed allocation rules, easier experimentation and policy changes.

Additional Refactorings
- Data classes for clear, typed domain entities.
- `ParkingSlot` entity to encapsulate slot state.
- Controller added to keep the model free of UI concerns.

Testing and Validation
- Manual test via redesigned Tk view (`python3 src/redesign/main.py`).
- Verified lot creation, parking (EV and regular), and leaving slots with clear messages.

Conclusion
The redesign separates concerns (MVC), reduces duplication, fixes logic errors, and introduces extensibility via Factory and Strategy. This foundation supports scaling to EV charging orchestration and microservices.
