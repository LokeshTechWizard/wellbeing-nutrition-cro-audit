# Implementation and Measurement Plan
## Wellbeing Nutrition — Korean Marine Collagen Peptides CRO

**Inter IIT Tech Meet 15.0 | Product Management Problem Statement**  
Prepared: 2026-10-24 | Updated: 2026-10-25 (V2)

---

## Overview

This plan covers the practical rollout of the five CRO recommendations from the audit strategy in prioritised order. It distinguishes between what can be implemented immediately, what requires company data first, and what requires A/B validation before full rollout.

---

## Phase 0 — Data Gathering (Before Any Implementation)

**Duration:** 1–2 weeks  
**Owner:** Product Manager + Analytics Team

Before implementing any recommendation, request the following from Wellbeing Nutrition's internal teams:

| Data Point | Source | Purpose |
|------------|--------|---------|
| Monthly page sessions (mobile vs. desktop) | GA4 / analytics | Size A/B tests; confirm mobile-first assumption |
| Add-to-cart rate (current baseline) | GA4 funnel | Baseline for EXP-001 |
| Product-page-to-checkout rate | GA4 funnel | Baseline for EXP-002 |
| Checkout abandonment rate and top reasons | GA4 + exit surveys | Validate shipping/returns hypothesis |
| Free shipping threshold | Operations | Required for EXP-002 messaging |
| Delivery SLA by region | Operations | Required for EXP-002 messaging |
| Returns policy terms | Customer Service | Required for EXP-002 messaging |
| Prior A/B tests on this page | CRO/Dev team | Avoid re-testing known results |
| Heatmaps / session recordings (Hotjar or Clarity) | Marketing/Analytics | Confirm scroll depth and ATC discoverability |

**Risk:** Without this data, A/B tests cannot be properly sized and results may be inconclusive.

---

## Implementation Order

### Step 1 — Sticky Mobile ATC Bar (EXP-001)
**Priority:** Highest  
**Type:** Frontend-only change (no backend)  
**Teams:** Frontend Engineering, QA, Analytics  
**Estimated effort:** 2–4 dev days + 1 QA day

#### Implementation Steps
1. **Engineering:** Add a fixed-position `<div>` to the product page template that appears after 300px scroll on screens < 768px.
2. **Engineering:** Populate the bar with the current selected variant price (from existing JS state).
3. **Engineering:** Wire ATC click in the sticky bar to the same cart-add function as the inline button.
4. **Engineering:** Dismiss the bar or change CTA to "View Cart" on successful add-to-cart.
5. **Engineering:** Implement behind a feature flag for A/B testing.
6. **Analytics:** Instrument `sticky_bar_impression`, `sticky_bar_atc_click` events.
7. **QA:** Verify on real iOS and Android devices (at minimum iPhone 14, Samsung S22).
8. **QA:** Verify no interference with cookie consent banners or chat widgets.
9. **A/B test:** 50/50 split; run until statistical significance reached (duration depends on traffic volume).
10. **Decision:** If hypothesis supported → full rollout. If not → iterate or drop.

#### Rollback Plan
Feature flag set to 0% variant instantly disables the bar. No backend deployment needed.

#### Required Analytics Events
- `sticky_bar_impression` (with scroll_depth, viewport, variant)
- `sticky_bar_atc_click` (product_id, price, variant)
- `add_to_cart` (source: sticky_bar vs. inline)

---

### Step 2 — Shipping & Returns Trust Strip (EXP-002)
**Priority:** Second  
**Type:** Content + frontend change  
**Teams:** Content/Copy, Frontend Engineering, Operations, Customer Service, QA, Analytics  
**Estimated effort:** 1 content day + 1 dev day + 1 QA day  
**Prerequisite:** Confirmed shipping threshold, delivery SLA, and returns policy from internal teams (Phase 0)

#### Implementation Steps
1. **Content:** Write copy using confirmed values only — no placeholder text in production.
2. **Engineering:** Insert three-icon trust strip below ATC button in product template.
3. **Engineering:** Link shipping and returns icons to existing policy pages.
4. **Engineering:** Implement behind feature flag for A/B testing.
5. **Analytics:** Instrument `trust_strip_impression`, `trust_strip_link_click`.
6. **QA:** Verify display on mobile, tablet, and desktop.
7. **QA:** Verify links resolve to correct policy pages.
8. **A/B test:** All devices; segment analysis by new vs. returning visitors.
9. **Decision:** Based on product-page-to-checkout rate and returns rate.

#### Risk: Policy Review Required
If the returns policy is restrictive or the shipping threshold is high relative to the product price, displaying it prominently may hurt rather than help conversion. A qualitative review of the policy (against competitor standards and customer expectations) is recommended before launch.

#### Rollback Plan
Feature flag set to 0%. No database or backend rollback required.

---

### Step 3 — Immediate Cart Feedback (Drawer or Notification)
**Priority:** Third  
**Type:** Frontend + potentially theme change  
**Teams:** Frontend Engineering, UX Design, QA, Analytics  
**Estimated effort:** 3–5 dev days + 1 UX design day + 1 QA day

#### Implementation Steps
1. **UX Design:** Design cart drawer (or toast notification as lighter alternative).
2. **Engineering:** Implement cart drawer with: product name, variant, quantity, price, cart total, "Continue Shopping" and "Proceed to Checkout" CTAs.
3. **Engineering:** Ensure drawer reflects real-time cart state (handles existing items).
4. **Analytics:** Instrument `cart_drawer_opened`, `proceed_to_checkout_from_drawer`.
5. **QA:** Cross-device testing; verify accessibility (keyboard close, focus management, ARIA role="dialog").
6. **Launch:** This can be a direct rollout if a toast notification is chosen (lower risk) or an A/B test if a full drawer is implemented (higher investment).

---

### Step 4 — Returns Guarantee Badge
**Priority:** Fourth  
**Type:** Content addition  
**Teams:** Content, Legal/CS, Engineering  
**Estimated effort:** 0.5 dev day (once policy confirmed)  
**Prerequisite:** Legal/CS confirmation of guarantee terms

#### Risk
Do not display guarantee terms that are not honoured in practice — this creates customer service and trust issues downstream.

---

### Step 5 — Product Benefits Restructure
**Priority:** Fifth  
**Type:** Copywriting + layout  
**Teams:** Content, Marketing, UX Design  
**Estimated effort:** 2–3 content + design days  
**Prerequisite:** Customer research (user testing or survey) to confirm which benefits resonate most

#### Note
This is an assumption-backed intervention. Conduct user testing (5–8 interviews or a comprehension survey) before investing in full copy restructure.

---

## QA Checklist for Each Intervention

- [ ] Renders correctly on Chrome, Safari, Firefox (latest)
- [ ] Renders correctly on iOS Safari (iPhone 14+) and Android Chrome
- [ ] Passes Lighthouse accessibility audit (score ≥ 90)
- [ ] No new JavaScript console errors
- [ ] Analytics events fire correctly (verified in GA4 DebugView)
- [ ] Feature flag can disable the change within 5 minutes
- [ ] Screen reader (NVDA or VoiceOver) can access new elements
- [ ] Page load time (LCP) does not increase by more than 100ms

---

## Monitoring Plan

| Metric | Alert Threshold | Monitoring Tool | Review Frequency |
|--------|----------------|-----------------|-----------------|
| Mobile add-to-cart rate | Drop > 5% vs. baseline | GA4 funnel | Daily during test |
| Bounce rate | Increase > 10% | GA4 | Daily during test |
| Page load time (LCP) | > 2.5s | Lighthouse / CrUX | Weekly |
| JavaScript errors | Any new error | Sentry or equivalent | Real-time |
| Returns rate | Increase > 20% baseline | Operations dashboard | Weekly |
| Cart abandonment rate | Increase > 5% | GA4 funnel | Daily during test |

---

## Risks and Limitations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Insufficient traffic volume for statistical significance | Medium | High | Run tests for minimum 2–4 weeks; do not stop early |
| Seasonal demand spikes distorting results | Medium | Medium | Avoid running during major sale events; document test period context |
| Anti-bot / CDN caching interfering with A/B test delivery | Low | High | Verify test delivery with analytics team before launch |
| Policy information is inaccurate or changes during test | Low | High | Lock policy copy before launch; set change-control process |
| Conflicting A/B tests on same page | Unknown | High | Audit existing test calendar before launching |
| Technical implementation diverges from design spec | Medium | Medium | Design QA review before launch |

---

## Data Not Available (Required from Wellbeing Nutrition)

The following items could not be determined from external inspection and are required for a fully informed implementation decision:

1. Current product-page conversion rate (page sessions → purchase)
2. Device split (mobile vs. desktop sessions %)
3. Funnel drop-off points (add-to-cart, checkout, payment)
4. Customer acquisition channel mix (organic, paid, social, email)
5. Existing A/B test results on this page
6. Heatmap scroll depth data (what % of users scroll to the ATC button)
7. Customer feedback / exit survey data
8. Free shipping threshold and delivery SLA
9. Returns policy details
10. Average sessions per month on this product page

---

*This plan contains recommendations and proposed processes. It does not represent a committed timeline or guarantee of results. All projected outcomes require validation through A/B testing with Wellbeing Nutrition's actual traffic.*
