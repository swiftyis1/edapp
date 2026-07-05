# Sprint 3: Monetization, License Management & SSO (Weeks 5 & 6)

**Theme:** Implement Stripe subscription checkouts for B2C families and B2B seat licenses for schools, build school-level admin portals for invite codes, and integrate Clever/Google SSO.

---

## Sprint Goals & Scope

*   **Objective:** Monetize the platform by integrating Stripe, enable district administrators to allocate seat quotas to campuses, and simplify registration via SSO.
*   **Approach:** Build standard Stripe checkout/webhook integrations, utilize secure cryptographic invitation codes, and configure OAuth2 flows.

---

## 📋 Iteration Checklist

### Week 5: Stripe Integration (B2C & B2B)

*   [ ] **1. Stripe API Setup & Product Catalog**
    *   Configure Stripe API keys in Django settings and define products (Individual Family Subscription vs. School/District Seat Quotas).
*   [ ] **2. Direct B2C Family Checkout (Stripe)**
    *   Build frontend "Go Premium" card and redirect users to Stripe Checkout Session.
    *   Implement Django webhook endpoint `/api/billing/webhook/` to handle subscription success, renewal, and cancellation events.
*   [ ] **3. School/District B2B Seat License Checkout**
    *   Implement checkout for district administrators to buy blocks of seats (e.g. $2 per seat per year).
    *   Store active subscription details on the `Campus` and `UserProfile` records.
*   [ ] **4. Quota Allocation & Check Enforcements**
    *   Allow District Admins to adjust seat quotas across campuses. Enforce seat limit checks when students join classrooms.

---

### Week 6: SSO & Teacher Invitation Roster

*   [ ] **5. Google Classroom / Clever SSO Setup**
    *   Register OAuth2 client IDs and secrets.
    *   Create backend SSO callback views to authenticate users and auto-detect their roles.
*   [ ] **6. Teacher Invite Code System**
    *   Allow school admins to generate and email unique invite links or codes to teachers.
    *   Implement teacher registration path validating invite codes.
*   [ ] **7. Subscription Status Badging**
    *   Add premium indicators and warning locks to the Next.js UI when seat limits are exceeded or subscriptions expire.
*   [ ] **8. Billing & Quota Verification**
    *   Create verification scripts to test Stripe webhook events and SSO callbacks.
