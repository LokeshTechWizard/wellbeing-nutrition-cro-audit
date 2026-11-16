# A/B Test Plan
## Wellbeing Nutrition — Korean Marine Collagen Peptides

**Inter IIT Tech Meet 15.0 | Product Management Problem Statement**  
Prepared: 2026-10-24 | Updated: 2026-10-25 (V2)

> **Important methodological note:** No baseline conversion rates, sample sizes, statistical significance thresholds, or test outcomes are presented below. These require Wellbeing Nutrition's actual GA4 (or equivalent) data to calculate. The plans below are design specifications for experiments that the company's analytics or CRO team would size and evaluate.

---

## Experiment 1 — Sticky Mobile Add-to-Cart Bar

### 1. Test Name
`EXP-001 | Sticky Mobile ATC Bar`

### 2. Observed Problem / Motivation
**Observed fact:** During automated mobile inspection (390×844 viewport), the Add-to-Cart button was detected at a Y position exceeding the initial viewport height, meaning it is not visible to mobile users without scrolling.

**Supporting external research:** Baymard Institute finds that on mobile product pages, a sticky ATC button reduces the effort required to initiate a purchase by eliminating the need to scroll back to the CTA after reading product details (https://baymard.com/research/mobile-usability, accessed 2026-10).

### 3. Hypothesis
If we display a fixed-bottom Add-to-Cart bar on mobile devices (visible after the user scrolls past the product image), then the mobile product-page-to-cart rate will increase compared to the current scroll-to-CTA layout, because reducing the number of steps to reach the CTA removes a discoverability friction for users who read product details before acting.

### 4. Control Experience
Current product page layout on mobile: ATC button is inline in the page and requires scrolling to reach. No persistent CTA visible once the user scrolls past the button.

### 5. Variant Experience
A fixed-position bar appears at the bottom of the mobile screen after the user scrolls at least 300px (approximately past the hero image). The bar contains:
- Truncated product name
- Current selected price
- "Add to Cart" button (full width, high contrast)

The bar disappears or updates to "View Cart" after item is successfully added. The bar does not appear on desktop.

### 6. Primary Metric
**Mobile add-to-cart rate** = (sessions that trigger add-to-cart event on mobile) ÷ (total mobile product page sessions)

*This is the proposed metric. The current baseline value is unknown and must be retrieved from Wellbeing Nutrition's analytics platform.*

### 7. Guardrail Metric
**Mobile bounce rate** on the product page — must not increase significantly (would indicate the sticky bar is intrusive or disrupts reading).

**Secondary guardrail:** Mobile average order value — must not decrease (could indicate customers are rushing past upsell prompts).

### 8. Target User Segment / Eligibility Criteria
- Device type: mobile (detected via UA or screen width < 768px)
- Page: product page for Korean Marine Collagen Peptides only (initial rollout)
- New and returning visitors (no exclusions)
- Exclude: users already in a conflicting A/B test on the same page

### 9. Required Tracking Events
| Event | Properties |
|-------|------------|
| `sticky_bar_impression` | scroll_depth, variant |
| `sticky_bar_atc_click` | product_id, price, variant_name |
| `add_to_cart` | source (sticky_bar vs. inline_button), product_id |
| `checkout_started` | session_id |
| `purchase_completed` | session_id, revenue |
| `page_exit` | scroll_depth, time_on_page |

### 10. What Evidence Would Support or Reject the Hypothesis

**Supports hypothesis:**
- Statistically significant increase in mobile add-to-cart rate in the variant vs. control
- No significant increase in mobile bounce rate
- No significant decrease in average order value

**Rejects hypothesis:**
- No statistically significant difference in mobile add-to-cart rate
- Increase in bounce rate (bar is annoying users)
- Decrease in average order value (users skipping upsell / pack selection)

**Inconclusive result:** Increase in add-to-cart rate but also increase in bounce rate — requires qualitative investigation (session recordings) before deciding.

### 11. Dependencies and Risks

| Item | Detail |
|------|--------|
| **Dependency** | Requires GA4 data to calculate required sample size (minimum detectable effect, baseline conversion rate, desired statistical power) |
| **Dependency** | Engineering team must implement variant; QA must verify it does not break on all target mobile devices |
| **Risk** | If the bar obscures important content (e.g., subscription selector, trust badges), it could reduce comprehension and hurt conversion — mitigate with scroll-threshold tuning |
| **Risk** | Interaction with any existing live A/B tests on the same page could confound results |
| **Risk** | Seasonal demand fluctuation during test period could mask treatment effect |
| **Rollback** | Server-side feature flag allows instant rollback to control if guardrail metrics breach |

---

## Experiment 2 — Shipping & Returns Reassurance Banner Near ATC

### 1. Test Name
`EXP-002 | Shipping & Returns Trust Strip`

### 2. Observed Problem / Motivation
**Observed fact:** Body text inspection of the product page found no mention of "free shipping," "delivery time," "return," or "refund" in the immediately visible area near the Add-to-Cart button.

**External research:** Baymard Institute identifies "unexpected shipping costs" as the single most common reason for checkout abandonment (cited in their E-Commerce Checkout Usability study, https://baymard.com/lists/cart-abandonment-rate, accessed 2026-10). Even when shipping is free, many customers abandon because they are uncertain about costs and must discover this only at checkout.

### 3. Hypothesis
If we add a three-icon trust strip directly below the Add-to-Cart button showing (1) free shipping threshold, (2) estimated delivery time, and (3) returns policy, then the product-page-to-checkout rate will increase compared to the current layout, because reducing shipping and returns uncertainty at the point of purchase decision addresses a primary source of cost anxiety.

### 4. Control Experience
Current product page: no shipping, delivery, or returns information visible near the ATC button.

### 5. Variant Experience
A horizontal strip of three icon + text pairs appears immediately below the ATC button:
- 🚚 **Free shipping** on orders over ₹[X] *(actual threshold from Wellbeing Nutrition)*
- 📦 **Delivered in [X]–[Y] days** *(actual SLA from Wellbeing Nutrition)*
- ↩️ **[X]-day returns** *(actual policy from Wellbeing Nutrition)*

The icons link to the full shipping and returns policy pages. The copy is factual and based only on Wellbeing Nutrition's actual policies — no fabricated values.

**Note:** This variant requires confirmed values from Wellbeing Nutrition's operations and customer service teams before launch.

### 6. Primary Metric
**Product-page-to-checkout rate** = (sessions that reach checkout) ÷ (total product page sessions)

*Baseline unknown; requires company analytics.*

### 7. Guardrail Metric
**Returns rate** — if the policy is featured prominently, it should not cause a significant increase in actual returns (would indicate it is attracting the wrong buyers). Monitor for 30 days post-experiment.

**Secondary guardrail:** Customer service contact rate for shipping/returns questions — should decrease or stay flat (indicates the information is resolving uncertainty, not creating new questions).

### 8. Target User Segment / Eligibility Criteria
- All devices (desktop and mobile)
- Product page for Korean Marine Collagen Peptides only (initial rollout)
- New visitors (first purchase segment is most affected by trust concerns)
- Exclude: users who have previously purchased (returning buyers already trust the brand)

### 9. Required Tracking Events
| Event | Properties |
|-------|------------|
| `trust_strip_impression` | variant, device, new_vs_returning |
| `trust_strip_link_click` | link_target (shipping_policy / returns_policy) |
| `add_to_cart` | product_id, session_type |
| `checkout_started` | session_id |
| `purchase_completed` | session_id, revenue, is_new_customer |
| `return_initiated` | order_id, reason |

### 10. What Evidence Would Support or Reject the Hypothesis

**Supports hypothesis:**
- Statistically significant increase in product-page-to-checkout rate for the variant, especially for new visitors
- Decrease or no change in customer service contacts about shipping/returns
- No significant increase in returns rate

**Rejects hypothesis:**
- No statistically significant difference in product-page-to-checkout rate
- Significant increase in returns rate (trust strip is attracting low-intent buyers)

**Inconclusive / requires further investigation:**
- Significant click-through on shipping/returns policy links but no improvement in checkout rate — suggests customers are reading the policy and finding it unsatisfactory; policy improvement may be needed before the strip adds value

### 11. Dependencies and Risks

| Item | Detail |
|------|--------|
| **Dependency** | Confirmed shipping threshold and delivery SLA from operations team |
| **Dependency** | Confirmed returns policy from customer service team |
| **Dependency** | GA4 or equivalent analytics for sample size calculation |
| **Risk** | If the stated free-shipping threshold is high (e.g., ₹2,500+ for a ₹1,000 product), displaying it may increase price anxiety rather than reduce it — pre-test with qualitative review |
| **Risk** | Returns policy that is restrictive may hurt conversion when prominently displayed — audit policy before running experiment |
| **Rollback** | Feature flag; remove strip from variant within one hour if anomalous bounce rate detected |

---

## What Wellbeing Nutrition Analytics Are Needed to Size These Tests

To calculate required sample size and evaluate results, the following data is needed:

1. **Baseline conversion rates:**
   - Current mobile add-to-cart rate (for EXP-001)
   - Current product-page-to-checkout rate by device and new vs. returning (for EXP-002)

2. **Traffic volume:**
   - Monthly unique sessions to the Korean Marine Collagen Peptides page
   - Device split (mobile vs. desktop %)
   - New vs. returning visitor split

3. **Statistical parameters (to agree with analytics team):**
   - Minimum Detectable Effect (MDE) — smallest improvement worth detecting
   - Statistical significance threshold (typically α = 0.05)
   - Statistical power (typically β = 0.80)

4. **Experiment history:**
   - Any prior A/B tests on this page and their outcomes (to avoid re-testing known results)

5. **Seasonal context:**
   - High-demand periods (sales, festivals) that should be avoided or accounted for during the test

---

*These are proposed experiment designs. No outcomes, conversion rates, or sample sizes are presented as real values. All metrics require actual company data to calculate.*
