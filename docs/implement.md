# DeliverU Implementation Plan

## Build Strategy

- [ ] Do not implement the whole frontend first.
- [ ] Start with backend foundations: domain model, migrations, auth, RBAC, API contracts.
- [ ] Build each feature as a vertical slice in this order: schema -> migration -> DTOs/services/controllers -> tests -> frontend page -> integration QA.
- [ ] Keep MVP focused on one-time ordering first.
- [ ] Defer recurring orders, proof uploads, analytics, and advanced finance flows until the core order lifecycle is stable.
- [ ] Use seed data for early development so customer and driver flows can be built before the full admin panel is complete.

## Current Repo Reality

- [ ] Replace remaining template naming such as `MyApp`, template dashboard copy, and example-only item language.
- [ ] Remove the `/api/v1/{path:path}` placeholder from `backend/main.py`.
- [ ] Wire real routers into `backend/main.py` starting with auth and then real DeliverU modules.
- [ ] Retire the example `items` module once real DeliverU domain modules exist or keep it only if it is repurposed into grocery/catalog code.

## Phase 0: Lock Core Decisions

- [ ] Decide user model: single `users` table with role enum (`admin`, `customer`, `driver`) is recommended.
- [ ] Decide whether customer, driver, and admin use one React app with role-based routing; recommended: yes.
- [ ] Decide region geometry for MVP; recommended: simple polygon or bounding box first.
- [ ] Define slot business rules: capacity, cutoff time, lock time, active/inactive state.
- [ ] Define order statuses: `draft`, `placed`, `locked`, `assigned`, `in_progress`, `completed`, `cancelled`.
- [ ] Define complaint statuses: `open`, `in_review`, `resolved`, `rejected`.
- [ ] Define finance entry types for drivers; recommended: unified ledger instead of separate payable/receival tables.
- [ ] Decide restaurant ordering model for MVP; recommended: restaurant selection plus free-text notes, not full structured menus yet.
- [ ] Merge duplicate SRS complaint-view requirements into one implementation flow.

## Phase 1: Project Foundation Cleanup

- [ ] Standardize project naming to `DeliverU` across backend metadata, docs, frontend copy, and infra.
- [ ] Set up a clean backend module pattern for real features: `dto`, `service`, `controller`.
- [ ] Add a backend test structure with `pytest`.
- [ ] Add frontend smoke test strategy or at least page-level manual QA checklist.
- [ ] Confirm environment configuration in `.env.example` is consistent with actual app names and database names.
- [ ] Ensure local development works with both Docker and non-Docker flows.
- [ ] Add seed/dev bootstrap data strategy for admin, customer, driver, region, slot, grocery, restaurant.

## Phase 2: Core Database Schema and Migrations

- [ ] Design and implement initial domain schema in `backend/database/models.py`.
- [ ] Create Alembic migrations for the first real schema.
- [ ] Stop relying on template `create_all()` as the main persistence path once migrations are stable.

- [ ] Implement `users`.
- [ ] Implement `customer_profiles`.
- [ ] Implement `driver_profiles`.
- [ ] Implement `admin_profiles` or admin role fields if a separate profile is unnecessary.
- [ ] Implement `regions`.
- [ ] Implement `delivery_slots`.
- [ ] Implement `region_driver_assignments`.
- [ ] Implement `grocery_items`.
- [ ] Implement `restaurants`.
- [ ] Implement `orders`.
- [ ] Implement `order_items`.
- [ ] Implement `complaints`.
- [ ] Implement `driver_ledger_entries`.
- [ ] Implement `proof_attachments`.
- [ ] Implement `recurring_order_templates` for later use.

## Phase 3: Authentication and RBAC

- [ ] Expand auth beyond the current template user model into role-aware authentication.
- [ ] Implement customer signup.
- [ ] Implement admin and driver account creation flows.
- [ ] Implement login, refresh token, logout, current user, change password, and deactivate endpoints.
- [ ] Implement role-based authorization helpers and route guards.
- [ ] Add backend tests for auth success, failure, inactive users, and permissions.
- [ ] Update frontend auth context to understand roles and redirect users to the correct area.

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

- [ ] Wire existing auth router and make login/register/me work for real.
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
