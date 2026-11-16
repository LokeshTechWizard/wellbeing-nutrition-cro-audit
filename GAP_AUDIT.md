# Gap-Audit Checklist: Wellbeing Nutrition CRO Prototype
## Inter IIT Tech Meet 15.0 — Product Management Problem Statement
**Target Page:** [Wellbeing Nutrition — Korean Marine Collagen Peptides](https://wellbeingnutrition.com/products/korean-marine-collagen-peptides?qty=1)  
**Audit Date:** 2026-10-25 | **Auditor:** Lead CRO & Frontend Architect  
**Status Key:**
- `PRESENT`: Implemented and verified in prototype
- `MISSING`: Not yet present in V2, required for complete experience
- `BROKEN`: Present in some form but dysfunctional or suboptimal
- `UNABLE TO VERIFY`: Third-party / internal proprietary data that cannot be verified without internal access

---

## 1. Header & Navigation

| Element | Status in V2 | Gap / Action Required in V3 | Status in V3 |
|---|---|---|---|
| Announcement Bar with Promo | MISSING | Top promo bar ("Free Shipping > ₹999 \| Use code WELLBEING10 for 10% OFF") | PRESENT |
| Official Brand Logo | PRESENT (Text) | SVG / Styled typography matching Wellbeing Nutrition identity | PRESENT |
| Navigation: "Shop All" | MISSING | Add direct navigation link | PRESENT |
| Navigation: "Shop by Benefits" Mega Dropdown | MISSING | Multi-column benefits dropdown (Skin, Hair, Bone & Joint, Sleep, Gut) | PRESENT |
| Navigation: "Shop by Categories" Dropdown | MISSING | Dropdown (Marine Collagen, Melts, Slow, Powders, Effervescents) | PRESENT |
| Navigation: "World of Wellbeing" Dropdown | MISSING | Dropdown (Our Story, Science, Blogs, Traceability) | PRESENT |
| Navigation: "Blog" & "FREE Consultation" | MISSING | Links with "New" and "Free" badge indicators | PRESENT |
| Navigation: "Kids" & "Best Wellness Buys" | MISSING | Category links with "Hot" badge indicator | PRESENT |
| Header Utility Icons | BROKEN (Cart only) | Add Quick Deals (Lightning), Wishlist (Heart), Notification (Bell), Search (Magnifier), Cart | PRESENT |
| Functional Search Interaction | MISSING | Expandable/Modal Search Overlay with live query filter & trending tags | PRESENT |
| Synchronized Cart Badge | PRESENT | Retain `#cartBadge` live update upon item addition/removal | PRESENT |
| Mobile Hamburger Menu & Drawer | MISSING | Touch-friendly slide-out drawer with accordion navigation | PRESENT |

---

## 2. Product Hero & Gallery

| Element | Status in V2 | Gap / Action Required in V3 | Status in V3 |
|---|---|---|---|
| Primary Product Image Display | PRESENT | High-res Korean Marine Collagen container front image | PRESENT |
| Image Proportions & Containment | PRESENT | Maintain `object-fit: contain` to prevent cropping | PRESENT |
| Clickable Thumbnails Gallery | PRESENT | Front pouch, Supplement Nutrition Facts, Scoop Lifestyle view | PRESENT |
| Image Zoom / Fullscreen Modal | MISSING | Click-to-enlarge modal preview for high-resolution inspection | PRESENT |
| Gallery Sticky Positioning (Desktop) | PRESENT | Confined to desktop (`@media (min-width: 992px)`) with max-height cap | PRESENT |
| Mobile Gallery Flow | PRESENT | Inline `position: relative` preventing overlap on mobile | PRESENT |

---

## 3. Purchase Panel & Pricing

| Element | Status in V2 | Gap / Action Required in V3 | Status in V3 |
|---|---|---|---|
| Product Title & Subtitle | PRESENT | "Pure Korean Marine Collagen Peptides \| Unflavored \| Combat Signs of Ageing" | PRESENT |
| Aggregate Rating & Review Count | PRESENT | 4.8 / 5 Rating with verified star count | PRESENT |
| Live Selling Price & MRP | PRESENT | ₹1,745 (Selling) \| ₹1,799 / ₹2,320 (MRP) with 25% discount tag | PRESENT |
| Member Price Callout | MISSING | VIP Member Price (₹1,658) incentive banner | PRESENT |
| Subscribe & Save vs. One-Time Selector | PRESENT | Clear toggle showing 10% recurring discount | PRESENT |
| Pack Size Options (100g, 200g, 400g) | PRESENT | Pack selection buttons updating price and unit savings dynamically | PRESENT |
| Quantity Selector (+/-) | PRESENT | Accessible selector `#qty-display`, bounded between 1 and 10 | PRESENT |
| Add to Cart Button (`#atcBtn`) | PRESENT | High-contrast CTA with instant tactile feedback (`Added!`) | PRESENT |
| Buy Now Button (Express Flow) | MISSING | 1-Click checkout modal demonstrating expedited purchasing | PRESENT |
| Pincode Delivery Estimator | MISSING | Interactive Indian pincode checker giving estimated delivery SLA | PRESENT |
| In-Stock / Urgency Signal | MISSING | "In Stock — Dispatches within 24 Hours" verified operational signal | PRESENT |

---

## 4. Trust Signals & Reassurance

| Element | Status in V2 | Gap / Action Required in V3 | Status in V3 |
|---|---|---|---|
| Shipping & Delivery Information | PRESENT | 3-item strip (Free shipping over ₹999, Fast Delivery, 30-Day Returns) | PRESENT |
| 30-Day Money-Back Guarantee | PRESENT | Dedicated shield badge near purchase panel | PRESENT |
| Quality Certifications Strip | MISSING | Wild-caught Marine Fish, Clean Label, Mercury-Free, Zero Sugar | PRESENT |
| Disclaimer for Illustrative Elements | PRESENT | Explicit `[ILLUSTRATIVE]` markers on unverified corporate SLAs | PRESENT |

---

## 5. Detailed Product Information & Science

| Element | Status in V2 | Gap / Action Required in V3 | Status in V3 |
|---|---|---|---|
| Structured Overview & Deep Dive | BROKEN (Minimal) | Expand into structured tabbed / accordion layout | PRESENT |
| Quantified Benefits & Molecular Size | MISSING | Highlight 8000mg Collagen/serving, Type I & III, <1000 Daltons | PRESENT |
| Full Nutritional Facts & Amino Acids | MISSING | Table detailing Glycine, Proline, Hydroxyproline breakdown | PRESENT |
| Directions of Use & Flavor Profile | PRESENT | Daily scoop instructions, unflavored/mixable in beverages | PRESENT |
| Clinical Studies & Research Data | MISSING | Double-blind clinical findings on skin elasticity & hydration | PRESENT |
| Third-Party Lab Purity Reports (COA) | MISSING | Heavy metals test summary (Mercury, Lead, Arsenic: Non-detectable) | PRESENT |

---

## 6. Social Proof & Reviews

| Element | Status in V2 | Gap / Action Required in V3 | Status in V3 |
|---|---|---|---|
| Overall Rating Breakdown & Stars | PRESENT | 4.8 / 5 display | PRESENT |
| Star Rating Distribution Bar Chart | MISSING | Visual percentages for 5-star, 4-star, 3-star ratings | PRESENT |
| Star Filter & Sorting Tabs | MISSING | Filter by star rating (All, 5★, 4★) and sort | PRESENT |
| Verified Customer Review Cards | PRESENT | Detailed review cards with verified buyer tags and skin concern tags | PRESENT |
| Helpfulness Voting Interaction | MISSING | "Helpful (X)" thumbs-up counter | PRESENT |
| "Write a Review" Modal Interaction | MISSING | Review submission form dialog for customer engagement | PRESENT |

---

## 7. Interactive Features & Tools

| Element | Status in V2 | Gap / Action Required in V3 | Status in V3 |
|---|---|---|---|
| AI Ingredient Chatbot | MISSING | Floating "Ask Wellbeing AI" assistant with verified product answers | PRESENT |
| Chatbot Fallback for Medical Advice | MISSING | Ethical disclaimer redirecting to healthcare professionals | PRESENT |
| Explore Similar Products Section | MISSING | Cross-sell cards for Mango Peach, Strawberry Watermelon, Tropical Bliss | PRESENT |
| "+ Quick Add" on Similar Products | MISSING | Instant addition of cross-sell products to cart drawer | PRESENT |
| Interactive FAQ Accordion | PRESENT | 7+ comprehensive collapsible questions with keyboard accessibility | PRESENT |

---

## 8. Cart System (`#cartDrawer`)

| Element | Status in V2 | Gap / Action Required in V3 | Status in V3 |
|---|---|---|---|
| Slide-In Cart Drawer | PRESENT | ARIA dialog drawer with backdrop overlay | PRESENT |
| Item Addition Feedback | PRESENT | Banner animation on add | PRESENT |
| In-Cart Quantity Controls | MISSING | Increment / decrement quantity directly in cart drawer | PRESENT |
| In-Cart Item Removal | MISSING | Trash / remove button per line item with auto-recalculation | PRESENT |
| Promo Coupon Code Application | MISSING | Working coupon input (`WELLBEING10` takes 10% off subtotal) | PRESENT |
| Free Shipping Progress Bar | PRESENT | Dynamic bar indicating remaining amount to unlock free shipping | PRESENT |
| Empty-Cart State | PRESENT | Clean empty state with "Shop Best Sellers" CTA | PRESENT |
| Session Persistence (`localStorage`) | MISSING | Cart state survives browser refresh | PRESENT |

---

## 9. Mobile Responsiveness & Polish

| Element | Status in V2 | Gap / Action Required in V3 | Status in V3 |
|---|---|---|---|
| Mobile Sticky Add to Cart Bar | PRESENT | `#stickyBar` scroll-triggered bottom bar with price & ATC | PRESENT |
| Non-Colliding Chatbot & Sticky Bar | BROKEN | Ensure chatbot button sits above sticky bar on mobile (`bottom: 90px`) | PRESENT |
| Zero Horizontal Overflow | PRESENT | Bounded `scrollWidth <= 395px` on 390px mobile viewport | PRESENT |
| Touch Target Minimums (>=44px) | PRESENT | All buttons, links, and inputs satisfy WCAG 2.5.8 & Apple HIG | PRESENT |
| Accessible Keyboard Focus States | PRESENT | Focus outlines on interactive controls | PRESENT |

---

## 10. Complete Footer

| Element | Status in V2 | Gap / Action Required in V3 | Status in V3 |
|---|---|---|---|
| Brand Mission & Trust Logos | MISSING | Rich footer column with brand background | PRESENT |
| Categorized Footer Links | BROKEN (Minimal) | Customer Service, Categories, Company, Policies | PRESENT |
| Newsletter Subscription Box | MISSING | Email input with instant success confirmation | PRESENT |
| Verified Social Links | MISSING | Instagram, Facebook, YouTube, LinkedIn handles | PRESENT |
| Payment Gateway Badges | MISSING | UPI, Visa, Mastercard, RuPay, COD badges | PRESENT |
| Compliance & FSSAI Disclaimers | PRESENT | Academic prototype notice + dietary supplement disclaimer | PRESENT |
