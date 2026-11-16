# Prioritised CRO Strategy
## Wellbeing Nutrition — Korean Marine Collagen Peptides

**Inter IIT Tech Meet 15.0 | Product Management Problem Statement**  
Audit Date: 2026-10-24 | Prototype Updated: 2026-10-25 (V2)

> **V2 Update:** Prototype updated with real product images from the Wellbeing Nutrition public CDN and corrected gallery sticky-positioning bug (now desktop-only).

---

## Target Customer Segment

**Primary segment:** Health-conscious women aged 25–45 in urban India, purchasing wellness supplements online.  
**Key purchase decision:** "Will this collagen product actually work, and is this brand trustworthy enough to spend ₹1,000+ on it for the first time?"  
**Device mix:** Assumption — majority mobile traffic (consistent with Indian e-commerce trends; to be confirmed with GA4 data).

**Source:** Assumption based on product category and Indian e-commerce demographic patterns. Internal Wellbeing Nutrition analytics required to confirm.

---

## Purchase Journey Map

```
1. Discovery (social/search ad) →
2. Product page landing →
3. Understand the product & benefits →
4. Evaluate price and options →
5. Check shipping cost & delivery time →
6. Assess brand trust & returns policy →
7. Select variant / quantity →
8. Click Add to Cart →
9. Review cart →
10. Proceed to checkout →
11. Purchase complete
```

**Three Most Important Friction Points Observed:**

| # | Friction Point | Stage | Evidence Basis |
|---|----------------|-------|----------------|
| 1 | Shipping cost and delivery time absent near ATC | Step 5 | Page body text inspection (observed) |
| 2 | No immediate cart feedback after ATC click | Step 8 | Post-click screenshot inspection (observed) |
| 3 | Add-to-Cart button potentially below the fold (mobile) | Step 8 | Bounding-box measurement (observed) |

---

## Prioritisation Framework

Each intervention is scored on three dimensions using a 1–3 scale:

| Dimension | 1 | 2 | 3 |
|-----------|---|---|---|
| **Impact** | Low — affects small % of users or minor behaviour change | Medium — affects meaningful % of users or mid-stage friction | High — affects majority of users or a critical conversion step |
| **Evidence Confidence** | Assumption / Hypothesis — no direct data | Observed — directly observed on page | Verified — reproducible technical confirmation |
| **Effort** | High — requires significant dev/design work | Medium — requires moderate dev work | Low — small change, quick to implement |

**Priority Score = Impact + Evidence Confidence + Effort**  
*(Higher is better; max = 9)*

---

## Recommended Interventions (Ranked)

### Rank 1 — Sticky Mobile Add-to-Cart Bar
**Priority Score: 8 / 9**

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| Impact | 3 | Mobile users (likely majority) must scroll past all content to reach ATC; removing this friction directly addresses the critical conversion step |
| Evidence Confidence | 2 | Observed via bounding-box measurement; exact mobile traffic % unknown |
| Effort | 3 | CSS + small JS sticky bar; no backend change required |

**Observation:** ATC button detected below the mobile viewport fold (390×844). Users who do not scroll never reach the purchase CTA.

**Hypothesis:** Adding a fixed-bottom "Add to Cart" bar on mobile will increase mobile add-to-cart rate compared to the current layout. (Requires A/B test to validate.)

**Recommended Fix:** Implement a sticky bottom bar on mobile that appears after the user scrolls past the product image, displaying the price and an ATC button. Disappears after item is added.

**External Support:** Baymard Institute reports sticky ATCs on mobile as one of the highest-impact single-page improvements for e-commerce (https://baymard.com/research/mobile-usability, accessed 2026-10).

---

### Rank 2 — Shipping Cost & Delivery Time Near ATC
**Priority Score: 7 / 9**

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| Impact | 3 | Shipping cost is the #1 cart abandonment reason per Baymard (68.7% avg abandonment); uncertainty at product stage = pre-abandonment |
| Evidence Confidence | 2 | Shipping info not detected in body text near ATC (observed); threshold unknown |
| Effort | 2 | Requires content update and possibly conditional logic for order thresholds |

**Observation:** Body text inspection found no "free shipping" or delivery time information near the Add-to-Cart button on the product page.

**Hypothesis:** Displaying "Free shipping on orders over ₹X" or "Delivered in 3–5 days" near the ATC button will reduce checkout abandonment driven by shipping uncertainty. (Requires A/B test and checkout funnel data to validate.)

**Recommended Fix:** Add a single line beneath the ATC button: "🚚 Free shipping on orders over ₹[threshold] | Delivered in [X] business days." Pull the real threshold from the existing free-shipping rule.

**Caveat:** This fix requires confirming the actual shipping threshold and delivery SLA from Wellbeing Nutrition's operations team before implementation.

---

### Rank 3 — Immediate Cart Feedback (Drawer or Notification)
**Priority Score: 7 / 9**

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| Impact | 3 | No cart feedback leaves customers unsure if click registered; drives repeat clicks and cart confusion |
| Evidence Confidence | 2 | No cart drawer/notification detected post-ATC (observed in test); may depend on JS load state |
| Effort | 2 | Cart drawer requires frontend development; simpler notification is faster |

**Observation:** After clicking the ATC button, no visible cart drawer or toast notification appeared within 2 seconds in the automated test.

**Hypothesis:** Implementing a cart drawer or slide-in notification that confirms the item was added (showing item name, quantity, price, and a "Proceed to Checkout" CTA) will increase add-to-cart-to-checkout rate. (Requires funnel analytics to validate.)

**Recommended Fix:** Implement a side-drawer cart that slides in upon ATC click, showing: product name, selected variant, price, total, and two CTAs — "Continue Shopping" and "Proceed to Checkout."

---

### Rank 4 — Returns & Money-Back Guarantee Near ATC
**Priority Score: 6 / 9**

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| Impact | 2 | Addresses risk aversion for first-time buyers; high-intent users most affected |
| Evidence Confidence | 2 | Return/refund text not found on product page (observed) |
| Effort | 2 | Content addition; policy must be confirmed with customer service team |

**Observation:** Body text search for "return" and "refund" on the product page returned negative results, suggesting no returns policy is prominently displayed.

**Hypothesis:** Displaying a clear "30-day money-back guarantee" badge near the ATC button will increase purchase conversion for first-time buyers who are risk-averse. (Requires conversion data segmented by new vs. returning users to validate.)

**Recommended Fix:** Add a brief guarantee statement near ATC: "✓ 30-day money-back guarantee | No questions asked." Ensure this matches the actual policy.

---

### Rank 5 — Product Benefits Hierarchy & Clarity
**Priority Score: 5 / 9**

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| Impact | 2 | Affects product comprehension for undecided customers |
| Evidence Confidence | 1 | Cannot assess benefit clarity from automated inspection alone; requires user testing |
| Effort | 2 | Copywriting and layout change |

**Assumption:** The product description may not immediately communicate the primary benefit (e.g., "skin hydration," "joint support") in a scannable format at the top of the page. This is an assumption that requires user reading comprehension testing to validate.

**Hypothesis:** Restructuring the product description to lead with 3–4 outcome-focused bullet points (e.g., "Visibly firmer skin in 4 weeks," "Supports joint flexibility") above the technical details will increase time-on-page and product-to-cart rate for first-time visitors.

**Recommended Fix:** Rewrite the above-the-fold description to lead with 3–4 concrete customer outcomes as bullet points, followed by technical details.

---

## Single Highest-Priority Recommendation

**Implement the Sticky Mobile Add-to-Cart Bar first.**

**Justification:**
1. The ATC button being below fold on mobile is a directly observable, reproducible friction point.
2. Mobile traffic likely constitutes the majority of visits (assumption to confirm with analytics).
3. It requires no backend changes — pure frontend CSS/JS.
4. It can be implemented and A/B tested within days.
5. If the hypothesis is correct, the impact (mobile add-to-cart rate improvement) will be immediate and measurable.

---

## Data Needed from Wellbeing Nutrition Before Full Implementation

1. **Device breakdown** from GA4 (mobile vs. desktop % of sessions)
2. **Product page drop-off rate** (% who leave without adding to cart)
3. **Add-to-cart → checkout conversion rate** (to measure cart feedback impact)
4. **Checkout abandonment reasons** (post-checkout surveys or heatmaps)
5. **Current shipping threshold and delivery SLA** (for messaging accuracy)
6. **Return policy details** (for guarantee copy accuracy)
7. **Existing A/B test history** on this page (to avoid re-testing known results)

---

*Recommendations are based on observed page characteristics and external research. They are hypotheses until validated by A/B tests with Wellbeing Nutrition's actual traffic and analytics.*
