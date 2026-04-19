# Frontend Smoke Checklist (Slice 0)

Use this checklist after backend and frontend are running. It covers the minimum role-routing and authentication behavior needed for Slice 0.

## Setup

- Backend API is reachable at `http://localhost:8504`
- Frontend is reachable at `http://localhost:8503`
- Seeded test accounts exist: `admin@example.com`, `customer@example.com`, and `driver@example.com` (default password: `DeliverU123`)

## Auth and Session

- Open landing page and confirm primary actions route to login/register
- Register a new customer account and confirm success feedback
- Login with a valid account and confirm redirect to `/app`
- Refresh the browser and confirm session persists
- Logout and confirm redirect to unauthenticated route

## Role Routing and Guards

- Login as customer and confirm `/app` resolves to `/app/customer`
- Login as driver and confirm `/app` resolves to `/app/driver`
- Login as admin and confirm `/app` resolves to `/app/admin`
- As customer, open `/app/admin` and verify redirect to `/app/customer`
- As driver, open `/app/customer` and verify redirect to `/app/driver`
- As admin, open `/app/driver` and verify redirect to `/app/admin`

## Inactive and Error Cases

- Deactivate a user via API and verify login is rejected
- Use an invalid password and verify login error is shown
- Remove access token from storage and verify protected route redirects to login

## Regression Checks

- Top navigation brand link works from all app role routes
- Dashboard header renders without the old dashboard chip
- Legacy items page is not reachable through app navigation
