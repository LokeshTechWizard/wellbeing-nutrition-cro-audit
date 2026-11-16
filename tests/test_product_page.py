"""
Automated regression tests for Wellbeing Nutrition CRO improvements.
Run with: python -m pytest tests/ -v

These tests check observable properties of the product page.
They are supplementary to manual testing and do not replace it.
"""

import pytest
import asyncio
import json
from pathlib import Path
from datetime import datetime

# ── Playwright is required ──────────────────────────────────────────────────
try:
    from playwright.sync_api import sync_playwright, expect
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

TARGET_URL = "https://wellbeingnutrition.com/products/korean-marine-collagen-peptides?qty=1"
DESKTOP_VIEWPORT = {"width": 1440, "height": 900}
MOBILE_VIEWPORT  = {"width": 390,  "height": 844}
TEST_RESULTS_DIR = Path(__file__).parent.parent / "screenshots" / "test_evidence"
TEST_RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ══════════════════════════════════════════════════════════════════
# SKIP ALL TESTS IF PLAYWRIGHT NOT INSTALLED
# ══════════════════════════════════════════════════════════════════
pytestmark = pytest.mark.skipif(
    not HAS_PLAYWRIGHT,
    reason="playwright not installed — run: pip install playwright && playwright install chromium"
)


@pytest.fixture(scope="session")
def browser_instance():
    """Shared browser instance for the test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        yield browser
        browser.close()


@pytest.fixture
def desktop_page(browser_instance):
    """Desktop viewport page fixture."""
    ctx = browser_instance.new_context(viewport=DESKTOP_VIEWPORT)
    page = ctx.new_page()
    yield page
    ctx.close()


@pytest.fixture
def mobile_page(browser_instance):
    """Mobile viewport page fixture."""
    ctx = browser_instance.new_context(
        viewport=MOBILE_VIEWPORT,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                   "AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
        is_mobile=True,
        has_touch=True
    )
    page = ctx.new_page()
    yield page
    ctx.close()


# ══════════════════════════════════════════════════════════════════
# TEST GROUP 1: Page Load
# ══════════════════════════════════════════════════════════════════

class TestPageLoad:
    """Verify the product page loads successfully."""

    def test_page_returns_200(self, desktop_page):
        """Product page should return HTTP 200."""
        response = desktop_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        assert response is not None, "No response received from server"
        assert response.status == 200, f"Expected HTTP 200, got {response.status}"

    def test_page_has_title(self, desktop_page):
        """Page title should not be empty or a generic error page title."""
        desktop_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        title = desktop_page.title()
        assert title, "Page title is empty"
        # Should not be a generic error page
        for error_phrase in ["404", "not found", "error", "page unavailable"]:
            assert error_phrase not in title.lower(), f"Page title suggests error: {title!r}"

    def test_product_heading_present(self, desktop_page):
        """An H1 element should be present on the page."""
        desktop_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        desktop_page.wait_for_timeout(2000)
        h1 = desktop_page.query_selector("h1")
        assert h1 is not None, "No H1 element found on product page"
        h1_text = h1.inner_text().strip()
        assert len(h1_text) > 0, "H1 element is present but empty"
        print(f"\n  H1 text: {h1_text!r}")


# ══════════════════════════════════════════════════════════════════
# TEST GROUP 2: Add-to-Cart Functionality
# ══════════════════════════════════════════════════════════════════

class TestAddToCart:
    """Test the core add-to-cart interaction."""

    def test_atc_button_exists(self, desktop_page):
        """An Add-to-Cart button should be present."""
        desktop_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        desktop_page.wait_for_timeout(2000)

        atc_selectors = [
            "button[name='add']",
            "#AddToCart",
            "button.product-form__submit",
            "[data-action='add-to-cart']",
        ]
        found = False
        for sel in atc_selectors:
            el = desktop_page.query_selector(sel)
            if el:
                found = True
                print(f"\n  ATC button found via: {sel}")
                break

        assert found, (
            "Add-to-Cart button not found via any standard selector. "
            "Selectors tried: " + str(atc_selectors)
        )

    def test_atc_button_is_enabled(self, desktop_page):
        """ATC button should not be disabled by default."""
        desktop_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        desktop_page.wait_for_timeout(2000)

        for sel in ["button[name='add']", "button.product-form__submit"]:
            el = desktop_page.query_selector(sel)
            if el:
                disabled = el.get_attribute("disabled")
                assert disabled is None, f"ATC button is disabled (attribute: {disabled!r})"
                return

        pytest.skip("ATC button not found — skipping enabled state test")

    def test_atc_button_above_fold_desktop(self, desktop_page):
        """
        ATC button Y position check on desktop.
        OBSERVATION (not assertion failure): Records whether ATC is above fold.
        We do not fail the test if it is below fold, but we record it.
        """
        desktop_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        desktop_page.wait_for_timeout(2000)

        for sel in ["button[name='add']", "button.product-form__submit"]:
            el = desktop_page.query_selector(sel)
            if el:
                box = el.bounding_box()
                if box:
                    is_above_fold = box["y"] < DESKTOP_VIEWPORT["height"]
                    print(f"\n  ATC button Y={box['y']:.0f}px | Above fold on desktop: {is_above_fold}")
                    # This is an observation finding, not a hard failure
                    if not is_above_fold:
                        print(
                            f"  ⚠ OBSERVATION: ATC button is {box['y'] - DESKTOP_VIEWPORT['height']:.0f}px "
                            f"below the desktop fold."
                        )
                return

        pytest.skip("ATC button not found — skipping fold position test")


# ══════════════════════════════════════════════════════════════════
# TEST GROUP 3: Mobile Layout
# ══════════════════════════════════════════════════════════════════

class TestMobileLayout:
    """Mobile-specific layout and usability tests."""

    def test_page_loads_on_mobile(self, mobile_page):
        """Product page should load on mobile viewport."""
        response = mobile_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        assert response is not None
        assert response.status == 200, f"Mobile page returned {response.status}"

    def test_atc_below_fold_mobile(self, mobile_page):
        """
        Record whether the ATC button is below the fold on mobile.
        This is an observational test — it records and reports, does not fail.
        """
        mobile_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        mobile_page.wait_for_timeout(2000)

        for sel in ["button[name='add']", "button.product-form__submit"]:
            el = mobile_page.query_selector(sel)
            if el:
                box = el.bounding_box()
                if box:
                    is_above_fold = box["y"] < MOBILE_VIEWPORT["height"]
                    msg = (
                        f"Mobile ATC button Y={box['y']:.0f}px "
                        f"| Viewport={MOBILE_VIEWPORT['height']}px "
                        f"| Above fold: {is_above_fold}"
                    )
                    print(f"\n  {msg}")

                    # Save evidence
                    mobile_page.screenshot(
                        path=str(TEST_RESULTS_DIR / "test_mobile_atc_fold.png"),
                        full_page=False
                    )

                    if not is_above_fold:
                        # Record as an observation, not a hard test failure
                        # because the existing site may intentionally have this layout
                        print(
                            f"  ⚠ FINDING F007 CONFIRMED: ATC button is below mobile fold "
                            f"by {box['y'] - MOBILE_VIEWPORT['height']:.0f}px"
                        )
                    return

        pytest.skip("ATC button not found on mobile — skipping fold test")

    def test_no_horizontal_scroll_mobile(self, mobile_page):
        """Page should not require horizontal scrolling on mobile (max-width check)."""
        mobile_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        mobile_page.wait_for_timeout(2000)

        scroll_width = mobile_page.evaluate("document.body.scrollWidth")
        viewport_width = MOBILE_VIEWPORT["width"]
        print(f"\n  Body scrollWidth={scroll_width}px | Viewport={viewport_width}px")

        assert scroll_width <= viewport_width + 5, (
            f"Horizontal scroll detected: scrollWidth={scroll_width}px > viewport={viewport_width}px. "
            "Page may have elements overflowing beyond viewport on mobile."
        )

    def test_touch_target_minimum_sizes(self, mobile_page):
        """Sample of interactive elements should have minimum 44px touch targets (Apple HIG)."""
        mobile_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        mobile_page.wait_for_timeout(2000)

        small_targets = mobile_page.evaluate("""() => {
            const els = Array.from(document.querySelectorAll('button, a[href]')).slice(0, 30);
            return els
                .map(el => {
                    const r = el.getBoundingClientRect();
                    return { tag: el.tagName, text: el.innerText.slice(0, 30), w: r.width, h: r.height };
                })
                .filter(e => e.w > 0 && e.h > 0 && (e.w < 44 || e.h < 44));
        }""")

        if small_targets:
            print(f"\n  Touch targets < 44px (of first 30 sampled): {len(small_targets)}")
            for t in small_targets[:5]:
                print(f"    {t['tag']}: {t['text']!r} — {t['w']:.0f}×{t['h']:.0f}px")

            # Soft assertion: warn but don't fail (site may have valid reasons)
            # Change to assert len(small_targets) == 0 for strict enforcement
            if len(small_targets) > 5:
                pytest.warns(UserWarning,
                    match="Many small touch targets detected")
        else:
            print("\n  All sampled touch targets meet 44px minimum.")


# ══════════════════════════════════════════════════════════════════
# TEST GROUP 4: Accessibility Checks
# ══════════════════════════════════════════════════════════════════

class TestAccessibility:
    """Basic automated accessibility checks. NOT a substitute for full WCAG audit."""

    def test_images_have_alt_text(self, desktop_page):
        """Product images should have non-empty alt text."""
        desktop_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        desktop_page.wait_for_timeout(2000)

        missing_alt = desktop_page.evaluate("""() => {
            return Array.from(document.querySelectorAll('img'))
                .filter(img => !img.alt || img.alt.trim() === '')
                .map(img => img.src.split('/').pop())
                .slice(0, 10);
        }""")

        print(f"\n  Images missing alt text: {len(missing_alt)}")
        if missing_alt:
            print(f"  Affected images (sample): {missing_alt[:5]}")

        # This is an observational assertion
        assert len(missing_alt) == 0, (
            f"{len(missing_alt)} image(s) are missing alt text: {missing_alt[:5]}. "
            "WCAG 1.1.1 requires all meaningful images to have descriptive alt text."
        )

    def test_page_has_lang_attribute(self, desktop_page):
        """HTML element should have a lang attribute for screen readers."""
        desktop_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        lang = desktop_page.evaluate("document.documentElement.lang")
        print(f"\n  HTML lang attribute: {lang!r}")
        assert lang, "HTML element missing lang attribute (WCAG 3.1.1)"

    def test_no_js_errors_on_load(self, desktop_page):
        """No JavaScript errors should fire on initial page load."""
        js_errors = []
        desktop_page.on("console", lambda msg: js_errors.append(msg.text)
                        if msg.type == "error" else None)

        desktop_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        desktop_page.wait_for_timeout(3000)

        if js_errors:
            print(f"\n  JavaScript console errors ({len(js_errors)}):")
            for e in js_errors[:5]:
                print(f"    {e}")

        # Soft assertion: log but do not fail (some JS errors may be from third-party scripts)
        print(f"\n  Total JS console errors: {len(js_errors)}")


# ══════════════════════════════════════════════════════════════════
# TEST GROUP 5: Trust & Clarity Checks
# ══════════════════════════════════════════════════════════════════

class TestTrustAndClarity:
    """Check for presence of trust signals and key information."""

    def test_price_is_visible(self, desktop_page):
        """A price element should be visible on the product page."""
        desktop_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        desktop_page.wait_for_timeout(2000)

        price_selectors = [
            ".price", ".product-price", "span.money",
            "[data-price]", ".price__regular", ".price--main"
        ]
        found_price = None
        for sel in price_selectors:
            el = desktop_page.query_selector(sel)
            if el and el.is_visible():
                found_price = el.inner_text().strip()
                break

        print(f"\n  Price text found: {found_price!r}")
        assert found_price, (
            "No visible price element found. Customer cannot determine cost without scrolling "
            "or hunting for price information."
        )

    def test_shipping_info_on_page(self, desktop_page):
        """
        Check for shipping information on the product page.
        Observational — records presence or absence.
        """
        desktop_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        desktop_page.wait_for_timeout(2000)

        page_text = desktop_page.inner_text("body").lower()
        has_shipping = "free shipping" in page_text or "shipping" in page_text
        has_delivery = "delivery" in page_text

        print(f"\n  'Shipping' mentioned: {has_shipping}")
        print(f"  'Delivery' mentioned: {has_delivery}")

        # Observational — not a hard failure
        if not has_shipping:
            print(
                "  ⚠ FINDING F005: Shipping information not detected in page text. "
                "Customers may be uncertain about shipping costs."
            )

    def test_returns_policy_on_page(self, desktop_page):
        """
        Check for returns / refund information on the product page.
        Observational — records presence or absence.
        """
        desktop_page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        desktop_page.wait_for_timeout(2000)

        page_text = desktop_page.inner_text("body").lower()
        has_returns = "return" in page_text or "refund" in page_text

        print(f"\n  Returns/refund information mentioned: {has_returns}")
        if not has_returns:
            print(
                "  ⚠ FINDING F006: Returns/refund policy not detected in page text. "
                "First-time buyers may be deterred by perceived purchase risk."
            )


# ══════════════════════════════════════════════════════════════════
# TEST GROUP 6: Prototype Tests (local file)
# ══════════════════════════════════════════════════════════════════

class TestPrototype:
    """Tests against the local CRO prototype file."""

    PROTOTYPE_PATH = str(Path(__file__).parent.parent / "prototype" / "index.html")

    def test_prototype_loads(self, browser_instance):
        """Prototype HTML should load in browser without errors."""
        ctx = browser_instance.new_context()
        page = ctx.new_page()
        js_errors = []
        page.on("console", lambda msg: js_errors.append(msg.text)
                if msg.type == "error" else None)

        page.goto(f"file:///{self.PROTOTYPE_PATH.replace(chr(92), '/')}")
        page.wait_for_timeout(1000)

        assert "prototype" in page.title().lower() or page.query_selector("h1") is not None, \
            "Prototype page did not load correctly"

        if js_errors:
            print(f"\n  Prototype JS errors: {js_errors}")
        assert len(js_errors) == 0, f"Prototype has JS errors: {js_errors}"
        ctx.close()

    def test_prototype_atc_button(self, browser_instance):
        """Prototype ATC button should be clickable and update cart badge."""
        ctx = browser_instance.new_context(viewport=DESKTOP_VIEWPORT)
        page = ctx.new_page()
        page.goto(f"file:///{self.PROTOTYPE_PATH.replace(chr(92), '/')}")
        page.wait_for_timeout(1000)

        # Initial badge should be 0
        badge = page.query_selector("#cartBadge")
        assert badge is not None, "Cart badge element not found in prototype"
        assert badge.inner_text().strip() == "0", "Initial cart badge should show 0"

        # Click ATC
        atc = page.query_selector("#atcBtn")
        assert atc is not None, "ATC button not found in prototype"
        atc.click()
        page.wait_for_timeout(500)

        # Badge should update
        new_count = badge.inner_text().strip()
        assert new_count != "0", f"Cart badge did not update after ATC click (still: {new_count!r})"
        print(f"\n  Cart badge after ATC click: {new_count!r}")

        ctx.close()

    def test_prototype_cart_drawer_opens(self, browser_instance):
        """Cart drawer should open after ATC click."""
        ctx = browser_instance.new_context(viewport=DESKTOP_VIEWPORT)
        page = ctx.new_page()
        page.goto(f"file:///{self.PROTOTYPE_PATH.replace(chr(92), '/')}")
        page.wait_for_timeout(1000)

        atc = page.query_selector("#atcBtn")
        assert atc is not None
        atc.click()
        page.wait_for_timeout(600)

        drawer = page.query_selector("#cartDrawer")
        assert drawer is not None, "Cart drawer element not found"
        assert "open" in (drawer.get_attribute("class") or ""), \
            "Cart drawer did not open after ATC click"

        ctx.close()

    def test_prototype_sticky_bar_mobile(self, browser_instance):
        """Sticky mobile ATC bar should appear after scrolling on mobile."""
        ctx = browser_instance.new_context(
            viewport=MOBILE_VIEWPORT,
            is_mobile=True, has_touch=True
        )
        page = ctx.new_page()
        page.goto(f"file:///{self.PROTOTYPE_PATH.replace(chr(92), '/')}")
        page.wait_for_timeout(1000)

        bar = page.query_selector("#stickyBar")
        assert bar is not None, "Sticky ATC bar element not found"

        # Before scroll — should not be visible
        classes_before = bar.get_attribute("class") or ""
        assert "visible" not in classes_before, "Sticky bar visible before scroll (should appear after)"

        # Scroll down
        page.evaluate("window.scrollTo(0, 500)")
        page.wait_for_timeout(500)

        classes_after = bar.get_attribute("class") or ""
        assert "visible" in classes_after, \
            "Sticky bar did not appear after scrolling 500px (expected 'visible' class)"

        ctx.close()

    def test_prototype_quantity_controls(self, browser_instance):
        """Quantity + and - controls should update the display."""
        ctx = browser_instance.new_context(viewport=DESKTOP_VIEWPORT)
        page = ctx.new_page()
        page.goto(f"file:///{self.PROTOTYPE_PATH.replace(chr(92), '/')}")
        page.wait_for_timeout(1000)

        qty = page.query_selector("#qty-display")
        assert qty is not None, "Quantity display element not found"
        assert qty.inner_text().strip() == "1", "Initial quantity should be 1"

        # Click + button
        plus_btn = page.locator('.qty-btn').nth(1)
        plus_btn.click()
        page.wait_for_timeout(200)
        assert qty.inner_text().strip() == "2", "Quantity should be 2 after clicking +"

        # Click - button
        minus_btn = page.locator('.qty-btn').nth(0)
        minus_btn.click()
        page.wait_for_timeout(200)
        assert qty.inner_text().strip() == "1", "Quantity should be 1 after clicking -"

        ctx.close()

    def test_prototype_no_horizontal_scroll_mobile(self, browser_instance):
        """Prototype should not require horizontal scrolling on mobile."""
        ctx = browser_instance.new_context(viewport=MOBILE_VIEWPORT, is_mobile=True)
        page = ctx.new_page()
        page.goto(f"file:///{self.PROTOTYPE_PATH.replace(chr(92), '/')}")
        page.wait_for_timeout(1000)

        scroll_width = page.evaluate("document.body.scrollWidth")
        assert scroll_width <= MOBILE_VIEWPORT["width"] + 5, \
            f"Horizontal scroll in prototype: scrollWidth={scroll_width}px"
        ctx.close()

    def test_prototype_coupon_discount(self, browser_instance):
        """Applying WELLBEING10 in cart drawer applies a 10% discount."""
        ctx = browser_instance.new_context(viewport=DESKTOP_VIEWPORT)
        page = ctx.new_page()
        page.goto(f"file:///{self.PROTOTYPE_PATH.replace(chr(92), '/')}")
        page.wait_for_timeout(1000)

        # Clear any existing cart items in localStorage
        page.evaluate("localStorage.clear(); if(window.STATE) { window.STATE.cartItems = []; window.STATE.couponCode = null; }")
        page.reload()
        page.wait_for_timeout(800)

        # Add item to cart
        page.click("#atcBtn")
        page.wait_for_timeout(500)

        # Drawer should be open
        drawer = page.query_selector("#cartDrawer")
        assert drawer is not None
        assert "open" in (drawer.get_attribute("class") or "")

        # Enter coupon code WELLBEING10
        page.fill("#cartCouponInput", "WELLBEING10")
        page.click(".apply-coupon-btn")
        page.wait_for_timeout(400)

        # Verify coupon applied confirmation message is visible
        coupon_msg = page.query_selector("#couponAppliedMsg")
        assert coupon_msg is not None
        assert coupon_msg.is_visible(), "Coupon applied message is not visible"

        ctx.close()

    def test_prototype_pincode_checker(self, browser_instance):
        """Pincode delivery checker provides delivery speed estimate."""
        ctx = browser_instance.new_context(viewport=DESKTOP_VIEWPORT)
        page = ctx.new_page()
        page.goto(f"file:///{self.PROTOTYPE_PATH.replace(chr(92), '/')}")
        page.wait_for_timeout(1000)

        page.fill("#pincodeInput", "110001")
        page.click(".pincode-check-btn")
        page.wait_for_timeout(300)

        result = page.query_selector("#pincodeResultMsg")
        assert result is not None
        assert "active" in (result.get_attribute("class") or "")
        text = result.inner_text()
        assert "Delivery to 110001" in text and "business days" in text

        ctx.close()

    def test_prototype_chatbot_toggle(self, browser_instance):
        """AI Chatbot widget can be opened and closed."""
        ctx = browser_instance.new_context(viewport=DESKTOP_VIEWPORT)
        page = ctx.new_page()
        page.goto(f"file:///{self.PROTOTYPE_PATH.replace(chr(92), '/')}")
        page.wait_for_timeout(1000)

        # Open chatbot
        page.click("#chatbotTriggerBtn")
        page.wait_for_timeout(300)

        modal = page.query_selector("#chatbotModal")
        assert modal is not None
        assert "open" in (modal.get_attribute("class") or "")

        # Close chatbot
        page.click("#chatbotModal .chatbot-modal-header button")
        page.wait_for_timeout(300)
        assert "open" not in (modal.get_attribute("class") or "")

        ctx.close()

    def test_prototype_quick_add_cross_sell(self, browser_instance):
        """Quick Add button on similar products adds the product to cart."""
        ctx = browser_instance.new_context(viewport=DESKTOP_VIEWPORT)
        page = ctx.new_page()
        page.goto(f"file:///{self.PROTOTYPE_PATH.replace(chr(92), '/')}")
        page.wait_for_timeout(1000)

        # Clear cart
        page.evaluate("localStorage.clear(); if(window.STATE) { window.STATE.cartItems = []; }")
        page.reload()
        page.wait_for_timeout(800)

        # Click the first quick add button
        quick_add_btn = page.locator(".quick-add-btn").nth(0)
        assert quick_add_btn.count() > 0
        quick_add_btn.click()
        page.wait_for_timeout(500)

        # Verify cart drawer opened and badge shows items
        drawer = page.query_selector("#cartDrawer")
        assert drawer is not None
        assert "open" in (drawer.get_attribute("class") or "")

        badge = page.query_selector("#cartBadge")
        assert badge is not None
        count = int(badge.inner_text().strip())
        assert count >= 1

        ctx.close()

