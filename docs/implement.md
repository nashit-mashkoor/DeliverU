# DeliverU Implementation Plan

## How to Use This Plan

This plan is intentionally organized in two ways so that implementation stays ordered and complete:

- **Vertical slices** are the primary delivery order.
- **Phases** are the coverage buckets that make sure no important area is skipped.

Use the document like this:

- Execute the project in **slice order**, from top to bottom.
- Treat **Slice 0** as the mandatory foundation gate before feature delivery begins.
- Complete each slice end-to-end before moving to the next one.
- For every slice, include schema, migration, API, auth and permissions, frontend flow, tests, and manual QA.
- After finishing a slice, update the matching **phase checklist items** so the document stays complete.
- If a task appears in both a slice and a phase, the **slice defines sequencing** and the **phase defines coverage**.
- After every implementation update the "Current Repo Status" by marking the relvent portion and updating the status


In practice:

- **Slices answer:** what should be built next?
- **Phases answer:** what areas of the system must eventually be covered?

This structure prevents two common failures:

- building the frontend first without backend foundations
- finishing feature slices while quietly missing required cross-cutting work such as auth, validation, testing, or hardening

## Build Strategy

- Do not implement the whole frontend first.
- Do not implement the entire backend blindly in isolation either.
- Start by completing the foundation work in Slice 0, then move through the remaining slices in order.
- Build each feature as a vertical slice in this order: schema -> migration -> DTOs/services/controllers -> tests -> frontend page/flow -> integration QA.
- Use seed data and minimal internal admin tooling early so customer and driver flows are not blocked by a polished admin panel.

## Current Repo Status

- [X] The repo baseline has been transitioned from template shell to DeliverU foundation across backend, frontend, runtime scripts, and docs.
- [X] Real API routing is active: the `/api/v1/{path:path}` placeholder is removed and auth routes are wired and live.
- [X] Authentication is role-aware end-to-end (`admin`, `customer`, `driver`) with backend RBAC helpers and frontend role route guards.
- [X] Core DeliverU domain schema is implemented in models and migrations (users/profiles/regions/slots/assignments/catalog/orders/complaints/ledger/proofs/recurring templates).
- [X] Database change management is migration-driven; startup uses Alembic and no longer relies on template `create_all()` bootstrap behavior.
- [X] Seed/bootstrap flow exists and is repeatable via `make seed` for one complete dev set (admin/customer/driver/region/slot/grocery/restaurant).
- [X] Local and Docker development flows are validated with current env setup, and backend auth/RBAC tests are present and passing.
- [X] Slice 0 foundation gate (Phases 0-3) is complete and verified; next work should proceed from Slice 3 onward.
- [ ] Retire the example `items` module once real DeliverU domain modules exist or keep it only if it is repurposed into grocery/catalog code.

## Ordered Vertical Slices

Follow this exact implementation order. Complete each slice end-to-end before starting the next one.

For every slice, use this execution pattern:

-  Schema/model updates.
-  Alembic migration.
-  DTOs, service logic, and controller/router.
-  Auth and permission checks.
-  Frontend UI flow.
-  Tests and manual QA mapped to SRS use cases.

### Slice 0: Foundation Completion (Phases 0 to 3)

Relevant phases:
- Phase 0: Lock Core Decisions
- Phase 1: Project Foundation Cleanup
- Phase 2: Core Database Schema and Migrations
- Phase 3: Authentication and RBAC

This is a mandatory prerequisite slice. Do not start Slice 1 until this slice is complete.

- [X] Complete every checklist item in Phase 0, Phase 1, Phase 2, and Phase 3.
- [X] Freeze core decisions: role model, region geometry strategy, slot rules, order statuses, complaint statuses, finance-entry approach, and MVP restaurant order format.
- [X] Standardize the project baseline: remove template naming, enforce module structure, and confirm env consistency.
- [X] Establish the quality baseline: backend tests, frontend smoke/QA checklist, and repeatable local + Docker development workflows.
- [X] Finalize seed-data approach for admin, customer, driver, region, slot, grocery, and restaurant bootstrap.
- [X] Implement the full DeliverU domain schema and generate stable Alembic migrations.
- [X] Make migration-driven schema changes the source of truth.
- [X] Implement role-aware auth end-to-end across signup, login, refresh, logout, me, change-password, and deactivate flows.
- [X] Implement authorization rules so access is enforced by role and account state.
- [X] Update frontend auth context and guards so role-based entry is working end-to-end.
- [X] Add and pass backend auth/RBAC tests including success, failure, inactive-user, and permission-boundary cases.
- [X] Verify readiness gate: API routes are active, auth is live, migrations are stable, and seeded data exists for the next slices.

### Slice 1: Platform Enablement

Relevant phases:
- Phase 1: Project Foundation Cleanup
- Phase 3: Authentication and RBAC
- Phase 13: Hardening and Release Readiness

- [X] Remove the global `501` placeholder and enable real API routing in `backend/main.py`.
- [X] Register working routers and ensure backend serves real endpoints.
- [X] Clean baseline template naming in backend/frontend entry files.
- [X] Ensure local dev and Docker flows run cleanly with current env files.
- [X] Confirm the app can boot, serve APIs, and support the next feature slices without template blockers.

### Slice 2: Auth + Role Shell

Relevant phases:
- Phase 3: Authentication and RBAC
- Phase 5: Customer MVP
- Phase 6: Driver MVP
- Phase 7: Admin MVP

- [ ] Finalize role-aware user/auth model (`admin`, `customer`, `driver`).
- [ ] Implement login, refresh, logout, me, and role-aware guards.
- [ ] Update frontend auth context and route guards for role-based app areas.
- [ ] Ensure customer, admin, and driver app shells are accessible after login.
- [ ] Confirm redirects and permissions behave correctly for each role.

### Slice 3: Regions

Relevant phases:
- Phase 4: Serviceability and Operational Setup APIs
- Phase 7: Admin MVP

- [ ] Implement region schema and migrations.
- [ ] Implement admin region CRUD APIs and validations.
- [ ] Build minimal admin region management UI.
- [ ] Validate region creation/editing rules and persistence.

### Slice 4: Delivery Slots

Relevant phases:
- Phase 4: Serviceability and Operational Setup APIs
- Phase 7: Admin MVP

- [ ] Implement slot schema linked to regions.
- [ ] Implement admin slot CRUD APIs.
- [ ] Enforce slot rules: valid time windows, conflicts, active status, capacity, and cutoff/lock settings.
- [ ] Build minimal admin slot management UI.
- [ ] Validate slot behavior because later customer ordering depends on it.

### Slice 5: Driver Setup + Region Assignment

Relevant phases:
- Phase 4: Serviceability and Operational Setup APIs
- Phase 6: Driver MVP
- Phase 7: Admin MVP

- [ ] Implement driver profile schema and CRUD APIs.
- [ ] Implement region-driver assignment APIs.
- [ ] Build minimal admin driver + assignment UI.
- [ ] Add seed data capability for at least one driver per test region.
- [ ] Confirm the system can determine which drivers belong to which region.

### Slice 6: Grocery Catalog

Relevant phases:
- Phase 4: Serviceability and Operational Setup APIs
- Phase 5: Customer MVP
- Phase 7: Admin MVP

- [ ] Implement grocery catalog schema and admin CRUD APIs.
- [ ] Implement customer-facing grocery listing by region.
- [ ] Build minimal admin grocery management UI.
- [ ] Validate that the catalog can support the first real customer order slice.

### Slice 7: Customer Profile + Serviceability

Relevant phases:
- Phase 4: Serviceability and Operational Setup APIs
- Phase 5: Customer MVP

- [ ] Implement customer profile APIs.
- [ ] Implement location update flow and region assignment logic.
- [ ] Add non-serviceable-location handling.
- [ ] Build customer profile UI with location update.
- [ ] Confirm the system can determine whether a customer can place orders.

### Slice 8: Customer Browse Availability

Relevant phases:
- Phase 5: Customer MVP

- [ ] Implement available slots API for the next 24 hours by customer region.
- [ ] Implement customer browse APIs for groceries and availability metadata.
- [ ] Build customer browse/start-order UI.
- [ ] Validate that only serviceable and valid choices are presented.

### Slice 9: Customer Place Grocery Order

Relevant phases:
- Phase 5: Customer MVP

- [ ] Implement `orders` and `order_items` schema usage in the live flow.
- [ ] Implement place-order API for grocery-only one-time orders.
- [ ] Build customer place-order UI and order detail basics.
- [ ] Validate empty order, invalid slot, lock rules, and location/serviceability edge cases.
- [ ] Confirm the first real business-critical end-to-end ordering flow works.

### Slice 10: Customer Manage Pending Orders + History

Relevant phases:
- Phase 5: Customer MVP

- [ ] Implement update-order API with lock/cutoff enforcement.
- [ ] Implement cancel-order API with lock/cutoff enforcement.
- [ ] Implement order-history API.
- [ ] Build customer order history and edit/cancel UX.
- [ ] Confirm the customer lifecycle is usable after order creation.

### Slice 11: Driver Upcoming Orders + Order Detail

Relevant phases:
- Phase 6: Driver MVP

- [ ] Implement driver upcoming orders API grouped by slot/region.
- [ ] Implement driver order detail API.
- [ ] Build driver upcoming orders and detail pages.
- [ ] Confirm drivers can see the work assigned to them.

### Slice 12: Driver Mark Complete

Relevant phases:
- Phase 6: Driver MVP

- [ ] Implement order status transition logic for completion.
- [ ] Implement driver mark-complete API with validation.
- [ ] Build completion UX and ensure status visibility for customer and admin.
- [ ] Confirm the core fulfillment loop is operational.

### Slice 13: Admin Order Oversight

Relevant phases:
- Phase 7: Admin MVP

- [ ] Implement admin order list/detail APIs.
- [ ] Build admin order monitoring/detail pages.
- [ ] Ensure order timeline/status is visible for support operations.
- [ ] Confirm admins can observe live and completed order flow.

### Slice 14: Restaurants

Relevant phases:
- Phase 4: Serviceability and Operational Setup APIs
- Phase 5: Customer MVP
- Phase 7: Admin MVP

- [ ] Implement restaurant schema and admin CRUD APIs.
- [ ] Implement customer restaurant availability by region.
- [ ] Build restaurant selection in customer order flow using free-text order details for MVP.
- [ ] Build minimal admin restaurant management UI.
- [ ] Keep this simpler than full menu modeling in the initial implementation.

### Slice 15: Complaints

Relevant phases:
- Phase 8: Complaints

- [ ] Implement complaint schema and customer complaint create/list/detail APIs.
- [ ] Implement admin complaint list/detail/status-update APIs.
- [ ] Build customer and admin complaint pages.
- [ ] Ensure complaints can be linked to customer, driver, order, and region where appropriate.

### Slice 16: Proof Uploads

Relevant phases:
- Phase 9: Media and File Uploads

- [ ] Integrate MinIO-backed upload service in backend.
- [ ] Implement proof attachment model and APIs linked to orders.
- [ ] Build driver proof upload UI.
- [ ] Ensure customer/admin proof viewing for relevant order detail screens.
- [ ] Add file validation, ownership checks, and size/type restrictions.

### Slice 17: Driver Finance Ledger

Relevant phases:
- Phase 10: Driver Finance
- Phase 6: Driver MVP
- Phase 7: Admin MVP

- [ ] Implement unified driver ledger schema/API for payable and receival entries.
- [ ] Implement admin add/delete ledger entry flows.
- [ ] Implement driver payable history view APIs.
- [ ] Build admin finance and driver history UIs.
- [ ] Confirm the driver finance model is usable operationally.

### Slice 18: Recurring Orders

Relevant phases:
- Phase 11: Recurring Orders
- Phase 5: Customer MVP

- [ ] Implement recurring order template model and APIs.
- [ ] Implement background generation jobs via TaskIQ.
- [ ] Add safeguards for slot changes, cutoff windows, and inactive catalog items.
- [ ] Build customer recurring-order management UI.
- [ ] Confirm recurring behavior does not break the one-time ordering model.

### Slice 19: Analytics

Relevant phases:
- Phase 12: Analytics
- Phase 7: Admin MVP

- [ ] Implement analytics queries for busiest regions and slots.
- [ ] Decide live vs cached/precomputed strategy.
- [ ] Build admin analytics dashboard pages.
- [ ] Validate that analytics reflect real operational data.

# Phases

## Phase 0: Lock Core Decisions

- [X] Decide user model: single `users` table with role enum (`admin`, `customer`, `driver`).
- [X] Decide whether customer, driver, and admin use one React app with role-based routing; recommended: yes.
- [X] Decide region geometry for MVP: bounding box.
- [X] Define slot business rules: `capacity=20`, `order_cutoff_minutes=30`, `edit_cancel_lock_minutes=30`, `is_active` state.
- [X] Define order statuses: `draft`, `placed`, `locked`, `assigned`, `in_progress`, `completed`, `cancelled`.
- [X] Define complaint statuses: `open`, `in_review`, `resolved`, `rejected`.
- [X] Define finance entry types for drivers: unified ledger (`driver_ledger_entries`) instead of separate payable/receival tables.
- [X] Decide restaurant ordering model for MVP: restaurant selection plus free-text notes (no structured menu modeling yet).
- [X] Merge duplicate SRS complaint-view requirements into one implementation flow.

### Phase 0 Decision Record (Frozen)

- User/auth model: single `users` table with role enum (`admin`, `customer`, `driver`), with customer self-signup and admin-created driver/admin accounts.
- Profile model: separate `customer_profiles` and `driver_profiles`; no separate `admin_profiles` in MVP.
- Serviceability model: region matching uses bounding-box geometry for MVP.
- Slot model: recurring daily slot templates per region; orders reference selected slots.
- Slot defaults: `capacity=20`, `order_cutoff_minutes=30`, `edit_cancel_lock_minutes=30`, `is_active=true`.
- Assignment model: drivers can be assigned to multiple regions via `region_driver_assignments`.
- Catalog model: groceries are associated with regions.
- Restaurant MVP model: optional restaurant selection with free-text order details.
- Recurring order scope: recurring applies to both grocery and restaurant order content.
- Driver finance model: unified ledger entries in `driver_ledger_entries`.
- Complaint linkage: `customer_id` required, with optional `order_id`, `driver_id`, and `region_id`.
- Complaint requirement merge: treat SRS UC-4 and UC-8 as one customer complaint-view flow (list + status + detail) implemented under Phase 8.
- Proof uploads: driver-uploaded, with customer and admin read access.
- Seeding strategy: dedicated seed/bootstrap command; initial seed includes one complete usable set.
- Validation baseline: both local non-Docker and Docker flows must pass.
- Backend test baseline: PostgreSQL-backed integration tests for auth/RBAC.
- Frontend test baseline for Slice 0: manual smoke checklist.
- Legacy handling: keep `items` module inactive for now.
- Compatibility stance: optimize for a clean DeliverU foundation rather than template backward compatibility.

## Phase 1: Project Foundation Cleanup

- [X] Standardize project naming to `DeliverU` across backend metadata, docs, frontend copy, and infra.
- [X] Set up a clean backend module pattern for real features: `dto`, `service`, `controller`.
- [X] Add a backend test structure with `pytest`.
- [X] Add frontend smoke test strategy or at least page-level manual QA checklist.
- [X] Confirm environment configuration in `.env.example` is consistent with actual app names and database names.
- [X] Ensure local development works with both Docker and non-Docker flows.
- [X] Add seed/dev bootstrap data strategy for admin, customer, driver, region, slot, grocery, restaurant.

## Phase 2: Core Database Schema and Migrations

Reference:
- Current ER model and divergence note: `docs/er-model.md`

- [X] Design and implement initial domain schema in `backend/database/models.py`.
- [X] Create Alembic migrations for the first real schema.
- [X] Stop relying on template `create_all()` as the main persistence path once migrations are stable.

- [X] Implement `users`.
- [X] Implement `customer_profiles`.
- [X] Implement `driver_profiles`.
- [X] Implement `admin_profiles` or admin role fields if a separate profile is unnecessary.
- [X] Implement `regions`.
- [X] Implement `delivery_slots`.
- [X] Implement `region_driver_assignments`.
- [X] Implement `grocery_items`.
- [X] Implement `restaurants`.
- [X] Implement `orders`.
- [X] Implement `order_items`.
- [X] Implement `complaints`.
- [X] Implement `driver_ledger_entries`.
- [X] Implement `proof_attachments`.
- [X] Implement `recurring_order_templates` for later use.

## Phase 3: Authentication and RBAC

- [X] Expand auth beyond the current template user model into role-aware authentication.
- [X] Implement customer signup.
- [X] Implement admin and driver account creation flows.
- [X] Implement login, refresh token, logout, current user, change password, and deactivate endpoints.
- [X] Implement role-based authorization helpers and route guards.
- [X] Add backend tests for auth success, failure, inactive users, and permissions.
- [X] Update frontend auth context to understand roles and redirect users to the correct area.

## Phase 4: Serviceability and Operational Setup APIs

- [ ] Implement region CRUD APIs.
- [ ] Implement slot CRUD APIs.
- [ ] Implement driver CRUD APIs.
- [ ] Implement region-driver assignment APIs.
- [ ] Implement grocery CRUD APIs.
- [ ] Implement restaurant CRUD APIs.
- [ ] Implement customer profile update and location-to-region assignment logic.
- [ ] Add validation for slot conflicts, invalid times, and non-serviceable customer locations.
- [ ] Add seed scripts so at least one region, slot, driver, grocery catalog, and restaurant exist in dev.

## Phase 5: Customer MVP

- [ ] Build customer profile API and frontend page.
- [ ] Build location update flow and assign customer to closest valid region.
- [ ] Build available-slots API for the next 24 hours.
- [ ] Build grocery catalog API for a customer's region.
- [ ] Build nearby/open restaurants API for a customer's region.
- [ ] Build place-order API.
- [ ] Build update-order API with lock/cutoff rules.
- [ ] Build cancel-order API with lock/cutoff rules.
- [ ] Build order-history API.
- [ ] Build customer home/dashboard page.
- [ ] Build customer place-order page.
- [ ] Build customer order detail page.
- [ ] Build customer order history page.
- [ ] Build frontend validation and error states for empty order, invalid location, and locked order behavior.
- [ ] Add backend and manual QA coverage for UC-1, UC-2, UC-3, UC-6, UC-7, UC-9, and UC-10.

## Phase 6: Driver MVP

- [ ] Build driver login and role-specific route protection.
- [ ] Build upcoming slots/orders API for drivers by assigned region.
- [ ] Build driver order detail API.
- [ ] Build mark-order-complete API.
- [ ] Build driver upcoming orders page.
- [ ] Build driver order detail page.
- [ ] Build driver completion flow with status changes and success/error handling.
- [ ] Add backend and manual QA coverage for UC-41, UC-43, UC-44, and UC-46.

## Phase 7: Admin MVP

- [ ] Build admin area layout and navigation.
- [ ] Build admin pages for regions.
- [ ] Build admin pages for slots.
- [ ] Build admin pages for drivers.
- [ ] Build admin pages for driver-region assignments.
- [ ] Build admin pages for groceries.
- [ ] Build admin pages for restaurants.
- [ ] Build admin order detail page.
- [ ] Build admin customer management flow only if still needed in MVP.
- [ ] Add backend and manual QA coverage for region, slot, driver, grocery, restaurant, and order-view admin use cases.

## Phase 8: Complaints

- [ ] Implement customer complaint create/list/detail APIs.
- [ ] Implement admin complaint list/detail/update-status APIs.
- [ ] Build customer complaints pages.
- [ ] Build admin complaints pages.
- [ ] Ensure complaints link to customer, driver, order, and region where possible.
- [ ] Add QA coverage for UC-4, UC-5, UC-8, UC-13, and UC-14.

## Phase 9: Media and File Uploads

- [ ] Integrate MinIO properly in backend services.
- [ ] Implement upload handling for driver proof attachments.
- [ ] Implement upload handling for restaurant menu images.
- [ ] Implement upload handling for user profile images if required.
- [ ] Add file size, type, and ownership validation.
- [ ] Build driver proof upload UI.
- [ ] Build customer/admin proof viewing where required.
- [ ] Add QA coverage for UC-45.

## Phase 10: Driver Finance

- [ ] Implement unified driver ledger model and APIs.
- [ ] Support admin add/delete ledger entries for payables and receivals.
- [ ] Support driver payable history view.
- [ ] Build admin driver finance pages.
- [ ] Build driver payable history page.
- [ ] Add QA coverage for UC-35, UC-38, UC-39, UC-40, and UC-41.

## Phase 11: Recurring Orders

- [ ] Design recurring order template model and generation rules.
- [ ] Use TaskIQ jobs to generate future orders from recurring templates.
- [ ] Add safeguards for slot validity, cutoff times, and inactive catalog entries.
- [ ] Build customer recurring-order setup and management UI.
- [ ] Build admin visibility into recurring order activity if needed.
- [ ] Add QA coverage for recurring-order behavior from the ordering flow.

## Phase 12: Analytics

- [ ] Implement aggregate queries for busiest regions.
- [ ] Implement aggregate queries for busiest slots.
- [ ] Decide whether analytics are computed live or cached/precomputed.
- [ ] Build admin analytics dashboard pages.
- [ ] Add QA coverage for UC-28.

## Phase 13: Hardening and Release Readiness

- [ ] Add backend tests for all critical services and permission boundaries.
- [ ] Add API validation tests for invalid inputs and unauthorized access.
- [ ] Add end-to-end smoke flows for customer, driver, and admin.
- [ ] Add error handling, empty states, and loading states across frontend pages.
- [ ] Review CORS, auth, rate limiting, and secure file access.
- [ ] Review logging and auditability for admin and driver actions.
- [ ] Review Docker and deployment settings for production readiness.
- [ ] Remove dead template code and unused example modules.
- [ ] Update README and technical docs to match the implemented system.

## Recommended First Vertical Slice

- [X] Wire existing auth router and make login/register/me work for real.
- [ ] Implement user roles and profile basics.
- [ ] Implement regions, slots, and grocery catalog with seed data.
- [ ] Implement customer place-order flow for grocery-only orders.
- [ ] Implement customer order history.
- [ ] Implement driver upcoming orders and mark-complete flow.
- [ ] Only after this first slice is stable, build out the rest of the admin UI, restaurants, complaints, recurring orders, finance, and analytics.

## Definition of Done For Every Slice

- [ ] Database model exists.
- [ ] Alembic migration exists.
- [ ] DTOs and validation exist.
- [ ] Service layer exists.
- [ ] Controller/router is wired into FastAPI.
- [ ] Permission checks exist.
- [ ] Backend tests exist.
- [ ] Frontend route/page exists.
- [ ] Frontend handles loading, success, empty, and error states.
- [ ] Manual QA is mapped back to the relevant SRS use cases.
