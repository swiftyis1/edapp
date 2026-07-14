# Sprint 7: Advanced B2B Billing & School Admin Quota Dashboards (Weeks 13 & 14)

**Theme:** Create school administrator quota management dashboards, configure Stripe B2B invoicing, and implement metered student seat licensing checks.

---

## Sprint Goals & Scope

*   **Objective:** Monetize school-level pilots via Stripe B2B metered invoicing, allow school admins to assign seat licenses, and enforce licensing limits during enrollment.
*   **Approach:** Build a Stripe invoice-generation service, enforce licensing constraints in user registration models, and construct school-level quota dashboards.

---

## 📋 Iteration Checklist

### Week 13: Stripe B2B Invoicing & Quotas

*   [x] **1. Metered Licensing Engine**
    *   Implement student seat checkout portals in Stripe, supporting seat packages (e.g. 50, 100, 500 seats).
*   [x] **2. Stripe Webhook Invoicing**
    *   Handle `invoice.paid` and `invoice.payment_failed` webhooks to automatically activate/freeze campus accounts.
*   [x] **3. License Enforcement Middleware**
    *   Implement database middleware to block student registration or classroom joins when the campus seat limit is exceeded.

---

### Week 14: School Administrator Quota Panel

*   [x] **4. School Admin Profile**
    *   Add a new UserProfile role choice: `School Admin` (linked to a specific `Campus`).
*   [x] **5. School Quota Dashboard**
    *   Build a dedicated dashboard for School Admins displaying seat quotas, active seat usage, student growth rates, and invite codes.
*   [x] **6. Invoicing Receipts**
    *   Allow School Admins to download past payment invoices and billing statements.
