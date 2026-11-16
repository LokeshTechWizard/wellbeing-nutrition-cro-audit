"""
Wellbeing Nutrition - Korean Marine Collagen Peptides
CRO Audit Script using Playwright
Author: CRO Audit Agent
Date: 2026-10-24
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Playwright async API ────────────────────────────────────────────────────
try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)

# ── Configuration ───────────────────────────────────────────────────────────
TARGET_URL = "https://wellbeingnutrition.com/products/korean-marine-collagen-peptides?qty=1"
OUTPUT_DIR = Path(__file__).parent
SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

DESKTOP_VIEWPORT = {"width": 1440, "height": 900}
MOBILE_VIEWPORT  = {"width": 390,  "height": 844}   # iPhone 14 Pro

# ── Findings container ──────────────────────────────────────────────────────
findings = []
console_errors = []
failed_requests = []
audit_log = []

def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    audit_log.append(line)

def add_finding(finding_id, category, description, evidence, steps,
                impact, severity, confidence, fix, validation,
                screenshot=None):
    findings.append({
        "id": finding_id,
        "category": category,
        "description": description,
        "evidence": evidence,
        "screenshot": screenshot or "",
        "reproduction_steps": steps,
        "customer_impact": impact,
        "severity": severity,          # Critical / High / Medium / Low
        "confidence": confidence,      # Verified / Observed / Assumption / Hypothesis
        "recommended_fix": fix,
        "validation_method": validation,
        "recorded_at": datetime.now().isoformat(),
    })

# ── Helper: capture screenshot ──────────────────────────────────────────────
async def shot(page, name: str) -> str:
    path = SCREENSHOT_DIR / f"{name}.png"
    await page.screenshot(path=str(path), full_page=False)
    log(f"  📸  Screenshot saved: {path.name}")
    return str(path)

async def full_shot(page, name: str) -> str:
    path = SCREENSHOT_DIR / f"{name}.png"
    await page.screenshot(path=str(path), full_page=True)
    log(f"  📸  Full-page screenshot saved: {path.name}")
    return str(path)

# ── Phase 1: Desktop Inspection ─────────────────────────────────────────────
async def inspect_desktop(browser):
    log("=== PHASE 1: DESKTOP INSPECTION (1440×900) ===")
    ctx = await browser.new_context(
        viewport=DESKTOP_VIEWPORT,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0.0.0 Safari/537.36"
    )
    page = await ctx.new_page()

    # Capture console errors
    page.on("console", lambda msg: console_errors.append({
        "type": msg.type, "text": msg.text, "url": page.url
    }) if msg.type in ("error", "warning") else None)

    # Capture failed network requests
    page.on("requestfailed", lambda req: failed_requests.append({
        "url": req.url, "failure": req.failure, "viewport": "desktop"
    }))

    try:
        log(f"  Navigating to {TARGET_URL}")
        resp = await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=45000)
        status = resp.status if resp else "unknown"
        log(f"  HTTP status: {status}")
        await page.wait_for_timeout(3000)

        # ── Full-page screenshot ─────────────────────────────────────────
        sc_desktop_full = await full_shot(page, "desktop_full_page")
        sc_desktop_hero = await shot(page, "desktop_hero_atf")

        # ── Product title ────────────────────────────────────────────────
        title_el = await page.query_selector("h1")
        title_text = (await title_el.inner_text()).strip() if title_el else "NOT FOUND"
        log(f"  Product title: {title_text!r}")

        # ── Price inspection ─────────────────────────────────────────────
        price_selectors = [
            ".price", ".product-price", "[data-price]", ".price__regular",
            ".price--main", "span.money", ".product__price"
        ]
        price_text = "NOT FOUND"
        for sel in price_selectors:
            el = await page.query_selector(sel)
            if el:
                t = (await el.inner_text()).strip()
                if t:
                    price_text = t
                    break
        log(f"  Price element: {price_text!r}")

        # ── Subscription / purchase-type selector ────────────────────────
        sub_selectors = [
            ".subscription", ".purchase-options", "[data-selling-plan]",
            ".selling-plan", ".subscribe-save", "input[name='selling_plan']"
        ]
        sub_found = False
        for sel in sub_selectors:
            el = await page.query_selector(sel)
            if el:
                sub_found = True
                log(f"  Subscription selector found: {sel}")
                break
        if not sub_found:
            log("  Subscription option: NOT DETECTED via common selectors")

        # ── Pack / variant selector ──────────────────────────────────────
        variant_sel = await page.query_selector_all(
            "select[name='options[Size]'], .variant-selector, "
            "[data-option], .product-form__option, input[type='radio']"
        )
        log(f"  Variant/option elements found: {len(variant_sel)}")

        # ── Quantity selector ────────────────────────────────────────────
        qty_el = await page.query_selector(
            "input[name='quantity'], .quantity__input, [data-quantity-input]"
        )
        log(f"  Quantity input found: {bool(qty_el)}")

        # ── Add to Cart button ────────────────────────────────────────────
        atc_selectors = [
            "button[name='add']", ".btn-addtocart", "#AddToCart",
            "[data-action='add-to-cart']", "button.product-form__submit",
            "button:has-text('Add to Cart')", "button:has-text('Add to Bag')"
        ]
        atc_el = None
        for sel in atc_selectors:
            atc_el = await page.query_selector(sel)
            if atc_el:
                log(f"  ATC button found via: {sel}")
                break
        if not atc_el:
            log("  ATC button: NOT FOUND via common selectors")
            add_finding(
                "F001", "VERIFIED TECHNICAL BUG",
                "Add-to-Cart button not detectable via standard selectors",
                "Playwright query_selector returned None for all standard ATC selectors",
                ["Navigate to product page", "Inspect DOM for button[name='add'] and common ATC selectors"],
                "Customer cannot add product; 100% cart abandonment",
                "Critical", "Observed",
                "Verify button markup and ensure standard name/data attributes are present",
                "Manual DOM inspection and automated selector audit"
            )

        # ── ATC button above-the-fold check ─────────────────────────────
        if atc_el:
            box = await atc_el.bounding_box()
            if box:
                atc_y = box["y"]
                atc_visible_atf = atc_y < DESKTOP_VIEWPORT["height"]
                log(f"  ATC button Y position: {atc_y:.0f}px | Above fold: {atc_visible_atf}")
                if not atc_visible_atf:
                    add_finding(
                        "F002", "OBSERVED USABILITY CONCERN",
                        "Add-to-Cart button requires scrolling on desktop (below the fold)",
                        f"ATC button detected at Y={atc_y:.0f}px; viewport height={DESKTOP_VIEWPORT['height']}px",
                        ["Load product page at 1440×900", "Observe initial visible area without scrolling"],
                        "Users who do not scroll may miss the primary purchase CTA",
                        "High", "Observed",
                        "Reposition ATC button above the fold or add a sticky purchase bar",
                        "A/B test sticky vs. inline CTA on scroll depth and add-to-cart rate"
                    )

        # ── Reviews / social proof ────────────────────────────────────────
        review_selectors = [
            ".reviews", ".product-reviews", "[data-reviews]",
            ".stamped-reviews", ".yotpo", "#shopify-product-reviews",
            ".review-count", ".star-rating"
        ]
        reviews_found = False
        for sel in review_selectors:
            el = await page.query_selector(sel)
            if el:
                reviews_found = True
                log(f"  Reviews section found: {sel}")
                break
        if not reviews_found:
            log("  Reviews: NOT DETECTED via common selectors")

        # ── Trust badges ──────────────────────────────────────────────────
        trust_selectors = [
            ".trust-badge", ".security-badge", ".payment-icons",
            "[class*='trust']", "[class*='secure']", ".badge"
        ]
        trust_found = any([
            await page.query_selector(sel) for sel in trust_selectors
        ])
        log(f"  Trust badges found: {trust_found}")

        # ── FAQ section ───────────────────────────────────────────────────
        faq_el = await page.query_selector(
            ".faq, [class*='faq'], details, summary, .accordion"
        )
        log(f"  FAQ/accordion section: {bool(faq_el)}")

        # ── Shipping / returns visibility ─────────────────────────────────
        page_text = (await page.inner_text("body")).lower()
        shipping_mentioned = "free shipping" in page_text or "delivery" in page_text
        returns_mentioned  = "return" in page_text or "refund" in page_text
        log(f"  Shipping info mentioned on page: {shipping_mentioned}")
        log(f"  Returns info mentioned on page: {returns_mentioned}")

        # ── Scroll and capture mid-page ───────────────────────────────────
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 3)")
        await page.wait_for_timeout(1000)
        sc_desktop_mid = await shot(page, "desktop_mid_page")

        await page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.66)")
        await page.wait_for_timeout(1000)
        sc_desktop_lower = await shot(page, "desktop_lower_page")

        # ── ATC interaction test ──────────────────────────────────────────
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(1000)

        if atc_el:
            log("  Testing ATC click...")
            try:
                await atc_el.scroll_into_view_if_needed()
                await page.wait_for_timeout(500)
                sc_pre_atc = await shot(page, "desktop_pre_atc_click")
                await atc_el.click(timeout=5000)
                await page.wait_for_timeout(2000)
                sc_post_atc = await shot(page, "desktop_post_atc_click")
                log("  ATC click executed. Inspecting cart feedback...")

                # Check for cart drawer
                cart_drawer_sel = [
                    ".cart-drawer", "#cart-drawer", ".mini-cart",
                    "[class*='drawer']", ".cart-notification", ".cart-popup"
                ]
                cart_drawer_found = False
                for sel in cart_drawer_sel:
                    el = await page.query_selector(sel)
                    if el:
                        visible = await el.is_visible()
                        if visible:
                            cart_drawer_found = True
                            log(f"  Cart drawer visible: {sel}")
                            sc_cart = await shot(page, "desktop_cart_drawer")
                            break

                if not cart_drawer_found:
                    log("  Cart drawer: NOT VISIBLE after ATC click")
                    add_finding(
                        "F003", "OBSERVED USABILITY CONCERN",
                        "No visible cart feedback / drawer detected immediately after ATC click",
                        "After clicking ATC button, no cart drawer or notification appeared within 2s",
                        ["Navigate to product page", "Click Add to Cart button", "Observe cart feedback"],
                        "Customer unsure if product was added, may click multiple times or abandon",
                        "High", "Observed",
                        "Implement cart drawer with immediate visual feedback on ATC",
                        "A/B test cart drawer vs. cart-page redirect on ATC conversion and repeat-click rate"
                    )
            except PlaywrightTimeoutError:
                log("  ATC click timed out")
                add_finding(
                    "F004", "VERIFIED TECHNICAL BUG",
                    "ATC button click timed out or element not interactable",
                    "Playwright click() raised TimeoutError on ATC element",
                    ["Navigate to product page", "Attempt to click ATC button"],
                    "Customer cannot add product to cart",
                    "Critical", "Verified",
                    "Debug button z-index, overlapping elements, or JS event handler issues",
                    "Reproduce manually in Chrome DevTools; check for covered elements"
                )

        # ── Navigate to cart ──────────────────────────────────────────────
        cart_urls = ["/cart", "https://wellbeingnutrition.com/cart"]
        try:
            await page.goto("https://wellbeingnutrition.com/cart",
                            wait_until="domcontentloaded", timeout=20000)
            await page.wait_for_timeout(2000)
            sc_cart_page = await shot(page, "desktop_cart_page")
            cart_body = (await page.inner_text("body")).lower()
            if "empty" in cart_body or "no items" in cart_body:
                log("  Cart page: appears empty (product may not have been added)")
            else:
                log("  Cart page: contains items")
        except Exception as e:
            log(f"  Cart navigation error: {e}")

        # ── Record findings based on observations ─────────────────────────
        if not shipping_mentioned:
            add_finding(
                "F005", "OBSERVED USABILITY CONCERN",
                "Shipping cost / free shipping threshold not prominently displayed on product page",
                "Body text search for 'free shipping' / 'delivery' returned False on product page",
                ["Load product page", "Search page for shipping information without scrolling"],
                "Customer uncertain about total cost; price anxiety may prevent purchase",
                "High", "Observed",
                "Add shipping information near ATC button (e.g., 'Free shipping on orders over ₹X')",
                "Heatmap analysis of where users leave the page; survey on checkout abandonment reasons"
            )

        if not returns_mentioned:
            add_finding(
                "F006", "OBSERVED USABILITY CONCERN",
                "Return / refund policy not visible on product page",
                "Body text search for 'return' / 'refund' returned False on product page",
                ["Load product page", "Search page for returns information"],
                "Customer risk aversion increases without clear returns policy; may not convert",
                "Medium", "Observed",
                "Add a brief returns guarantee near ATC (e.g., '30-day money-back guarantee')",
                "Exit survey asking customers why they did not purchase"
            )

        await ctx.close()
        return {
            "title": title_text,
            "price": price_text,
            "subscription_found": sub_found,
            "variants_count": len(variant_sel),
            "qty_found": bool(qty_el),
            "atc_found": bool(atc_el),
            "reviews_found": reviews_found,
            "trust_badges": trust_found,
            "faq_found": bool(faq_el),
            "shipping_mentioned": shipping_mentioned,
            "returns_mentioned": returns_mentioned,
        }

    except Exception as e:
        log(f"  DESKTOP INSPECTION ERROR: {e}")
        await ctx.close()
        return {}


# ── Phase 2: Mobile Inspection ───────────────────────────────────────────────
async def inspect_mobile(browser):
    log("=== PHASE 2: MOBILE INSPECTION (390×844 – iPhone 14 Pro) ===")
    ctx = await browser.new_context(
        viewport=MOBILE_VIEWPORT,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                   "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                   "Version/17.0 Mobile/15E148 Safari/604.1",
        is_mobile=True,
        has_touch=True
    )
    page = await ctx.new_page()
    page.on("console", lambda msg: console_errors.append({
        "type": msg.type, "text": msg.text, "url": page.url, "viewport": "mobile"
    }) if msg.type in ("error", "warning") else None)

    try:
        log(f"  Navigating to {TARGET_URL}")
        await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(3000)

        sc_mobile_hero = await shot(page, "mobile_hero_atf")
        sc_mobile_full = await full_shot(page, "mobile_full_page")

        # ── ATC visibility on mobile ──────────────────────────────────────
        atc_el = None
        for sel in ["button[name='add']", "button:has-text('Add to Cart')",
                    ".product-form__submit", "#AddToCart"]:
            atc_el = await page.query_selector(sel)
            if atc_el:
                break

        if atc_el:
            box = await atc_el.bounding_box()
            if box:
                atc_y_mobile = box["y"]
                log(f"  Mobile ATC Y: {atc_y_mobile:.0f}px | Viewport height: {MOBILE_VIEWPORT['height']}")
                if atc_y_mobile > MOBILE_VIEWPORT["height"]:
                    add_finding(
                        "F007", "OBSERVED USABILITY CONCERN",
                        "Add-to-Cart button is below the fold on mobile (390×844)",
                        f"ATC Y={atc_y_mobile:.0f}px exceeds mobile viewport height of {MOBILE_VIEWPORT['height']}px",
                        ["Load product page on mobile (390×844)", "Do not scroll", "Observe ATC button"],
                        "Mobile users (likely majority of traffic) may miss CTA without scrolling",
                        "High", "Observed",
                        "Implement sticky mobile ATC bar that remains fixed at bottom of viewport",
                        "A/B test sticky mobile CTA bar vs. current layout on mobile add-to-cart rate"
                    )
        else:
            log("  Mobile ATC button: NOT FOUND")

        # ── Touch target sizes ────────────────────────────────────────────
        buttons = await page.query_selector_all("button, a[href], input[type='radio']")
        small_targets = []
        for btn in buttons[:20]:  # Sample first 20
            box = await btn.bounding_box()
            if box and (box["width"] < 44 or box["height"] < 44):
                txt = (await btn.inner_text()).strip()[:40]
                small_targets.append({"text": txt, "w": box["width"], "h": box["height"]})

        log(f"  Touch targets < 44px (sample of 20): {len(small_targets)}")
        if len(small_targets) > 3:
            add_finding(
                "F008", "OBSERVED USABILITY CONCERN",
                f"{len(small_targets)} interactive elements have touch targets smaller than 44×44px (WCAG 2.5.8 / Apple HIG)",
                f"Playwright bounding box check on first 20 interactive elements: {small_targets[:3]}...",
                ["Load product page on mobile", "Inspect button/link bounding boxes"],
                "Difficult tap interactions on mobile; accidental mis-taps reduce usability",
                "Medium", "Observed",
                "Increase minimum touch target size to 44×44px for all interactive elements",
                "Automated Playwright bounding-box regression test; manual testing on real device"
            )

        # ── Scroll to capture sections ────────────────────────────────────
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        await page.wait_for_timeout(1000)
        sc_mobile_mid = await shot(page, "mobile_mid_page")

        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(1000)
        sc_mobile_bottom = await shot(page, "mobile_bottom_page")

        # ── Font readability ──────────────────────────────────────────────
        body_font = await page.evaluate("""() => {
            const el = document.querySelector('p, .product-description, .description');
            if (!el) return null;
            const s = window.getComputedStyle(el);
            return { fontSize: s.fontSize, lineHeight: s.lineHeight, color: s.color };
        }""")
        log(f"  Body font info: {body_font}")
        if body_font and body_font.get("fontSize"):
            fs = float(body_font["fontSize"].replace("px", ""))
            if fs < 16:
                add_finding(
                    "F009", "OBSERVED USABILITY CONCERN",
                    f"Body/description text font-size ({fs}px) may be below comfortable mobile reading threshold (16px)",
                    f"CSS computed style: {body_font}",
                    ["Load product page on mobile", "Inspect body text font size via DevTools"],
                    "Small text increases cognitive load and reduces product comprehension on mobile",
                    "Medium", "Observed",
                    "Set minimum body font size to 16px on mobile viewports",
                    "Accessibility audit with Lighthouse; user reading comprehension test"
                )

        await ctx.close()

    except Exception as e:
        log(f"  MOBILE INSPECTION ERROR: {e}")
        await ctx.close()


# ── Phase 3: Accessibility Quick Check ──────────────────────────────────────
async def check_accessibility(browser):
    log("=== PHASE 3: BASIC ACCESSIBILITY CHECK ===")
    ctx = await browser.new_context(viewport=DESKTOP_VIEWPORT)
    page = await ctx.new_page()
    try:
        await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(2000)

        # Images without alt text
        imgs_no_alt = await page.evaluate("""() => {
            const imgs = Array.from(document.querySelectorAll('img'));
            return imgs.filter(i => !i.alt || i.alt.trim() === '').length;
        }""")
        log(f"  Images missing alt text: {imgs_no_alt}")
        if imgs_no_alt > 0:
            add_finding(
                "F010", "OBSERVED USABILITY CONCERN",
                f"{imgs_no_alt} product image(s) lack descriptive alt text",
                f"DOM query: imgs.filter(i => !i.alt).length = {imgs_no_alt}",
                ["Load product page", "DevTools: document.querySelectorAll('img:not([alt])')"],
                "Screen reader users receive no product image context; WCAG 1.1.1 violation",
                "Medium", "Observed",
                "Add descriptive alt text to all product images",
                "Automated axe-core scan; manual screen-reader test"
            )

        # Form inputs without labels
        inputs_no_label = await page.evaluate("""() => {
            const inputs = Array.from(document.querySelectorAll('input, select, textarea'));
            return inputs.filter(i => {
                const id = i.id;
                const label = id ? document.querySelector('label[for="' + id + '"]') : null;
                const aria  = i.getAttribute('aria-label') || i.getAttribute('aria-labelledby');
                return !label && !aria;
            }).length;
        }""")
        log(f"  Inputs missing labels: {inputs_no_label}")
        if inputs_no_label > 0:
            add_finding(
                "F011", "OBSERVED USABILITY CONCERN",
                f"{inputs_no_label} form input(s) lack accessible labels (no <label for=>, aria-label, or aria-labelledby)",
                f"DOM query count: {inputs_no_label}",
                ["Load product page", "DevTools: inspect input elements for label associations"],
                "Screen reader users cannot identify form fields; WCAG 1.3.1 violation",
                "Medium", "Observed",
                "Associate all inputs with visible labels or aria-label attributes",
                "axe-core automated test; NVDA/JAWS screen reader test"
            )

        await ctx.close()
    except Exception as e:
        log(f"  ACCESSIBILITY CHECK ERROR: {e}")
        await ctx.close()


# ── Phase 4: Console & Network Error Summary ─────────────────────────────────
def add_network_findings():
    if failed_requests:
        log(f"  Failed network requests: {len(failed_requests)}")
        add_finding(
            "F012", "VERIFIED TECHNICAL BUG",
            f"{len(failed_requests)} network request(s) failed during page load",
            json.dumps(failed_requests[:5], indent=2),
            ["Open DevTools Network tab", "Reload product page", "Filter for failed requests"],
            "Broken assets or APIs may cause missing images, broken reviews, or non-functional features",
            "High", "Verified",
            "Investigate and fix each failed request; add monitoring alerts",
            "Automated network request monitoring in CI/CD"
        )

    js_errors = [e for e in console_errors if e["type"] == "error"]
    if js_errors:
        log(f"  JavaScript console errors: {len(js_errors)}")
        add_finding(
            "F013", "VERIFIED TECHNICAL BUG",
            f"{len(js_errors)} JavaScript console error(s) detected during page load",
            json.dumps(js_errors[:5], indent=2),
            ["Open DevTools Console tab", "Reload product page", "Filter for errors"],
            "JS errors may disable cart functionality, reviews, or tracking",
            "High", "Verified",
            "Investigate and resolve each JS error; add error monitoring (Sentry or similar)",
            "Automated Playwright console-error assertion in CI"
        )


# ── Main runner ──────────────────────────────────────────────────────────────
async def main():
    log("╔═══════════════════════════════════════════════════════╗")
    log("║   WELLBEING NUTRITION CRO AUDIT — Playwright Script   ║")
    log("╚═══════════════════════════════════════════════════════╝")
    log(f"Target: {TARGET_URL}")
    log(f"Started: {datetime.now().isoformat()}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        log("Browser launched: Chromium (headless)")

        desktop_data = await inspect_desktop(browser)
        await inspect_mobile(browser)
        await check_accessibility(browser)
        add_network_findings()

        await browser.close()

    # ── Save findings to JSON ────────────────────────────────────────────
    out_json = OUTPUT_DIR / "findings.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "audit_metadata": {
                "target_url": TARGET_URL,
                "audit_date": datetime.now().isoformat(),
                "tool": "Playwright + Python",
                "desktop_viewport": DESKTOP_VIEWPORT,
                "mobile_viewport": MOBILE_VIEWPORT,
                "total_findings": len(findings),
                "console_errors": len(console_errors),
                "failed_requests": len(failed_requests),
            },
            "desktop_inspection": desktop_data,
            "findings": findings,
            "console_errors": console_errors,
            "failed_requests": failed_requests,
            "audit_log": audit_log,
        }, f, indent=2, ensure_ascii=False)
    log(f"\n✅ Findings saved to: {out_json}")
    log(f"   Total findings: {len(findings)}")
    log(f"   Screenshots: {len(list(SCREENSHOT_DIR.glob('*.png')))} files in {SCREENSHOT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
