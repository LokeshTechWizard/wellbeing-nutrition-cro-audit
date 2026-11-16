"""
V2 screenshot capture for CRO Audit Prototype.
Takes desktop and mobile screenshots of the local prototype file.
"""
import asyncio
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: playwright not installed")
    raise

PROTO_PATH = (Path(__file__).parent / "prototype" / "index.html").resolve()
PROTO_URL  = "file:///" + str(PROTO_PATH).replace("\\", "/")
SHOT_DIR   = (Path(__file__).parent / "screenshots").resolve()
SHOT_DIR.mkdir(exist_ok=True)

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])

        # ── Desktop 1440×900 ─────────────────────────────────────
        ctx_d = await browser.new_context(viewport={"width": 1440, "height": 900})
        page_d = await ctx_d.new_page()
        await page_d.goto(PROTO_URL, wait_until="domcontentloaded")
        await page_d.wait_for_timeout(1500)

        # Full page
        await page_d.screenshot(
            path=str(SHOT_DIR / "v2_desktop_full.png"),
            full_page=True
        )
        print("✅  v2_desktop_full.png")

        # ATF (above the fold)
        await page_d.screenshot(
            path=str(SHOT_DIR / "v2_desktop_atf.png"),
            full_page=False
        )
        print("✅  v2_desktop_atf.png")

        # Cart drawer
        await page_d.evaluate("document.getElementById('atcBtn').click()")
        await page_d.wait_for_timeout(800)
        await page_d.screenshot(
            path=str(SHOT_DIR / "v2_desktop_cart_drawer.png"),
            full_page=False
        )
        print("✅  v2_desktop_cart_drawer.png")

        # Close cart
        await page_d.evaluate("document.getElementById('cartDrawer').classList.remove('open')")
        await page_d.evaluate("document.getElementById('cartOverlay').classList.remove('open')")
        await page_d.evaluate("document.body.style.overflow = ''")

        # Thumbnail switch to nutritional info
        await page_d.evaluate("""
            selectThumb(
              document.querySelectorAll('.thumb')[1],
              'https://wellbeingnutrition.com/cdn/shop/files/Korean-Collagen-Back-Nutritional-Info.jpg',
              'Nutritional info view'
            )
        """)
        await page_d.wait_for_timeout(800)
        await page_d.screenshot(
            path=str(SHOT_DIR / "v2_desktop_thumb_switch.png"),
            full_page=False
        )
        print("✅  v2_desktop_thumb_switch.png")

        await ctx_d.close()

        # ── Mobile 390×844 ───────────────────────────────────────
        ctx_m = await browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                       "AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
            is_mobile=True, has_touch=True
        )
        page_m = await ctx_m.new_page()
        await page_m.goto(PROTO_URL, wait_until="domcontentloaded")
        await page_m.wait_for_timeout(1500)

        # Full page
        await page_m.screenshot(
            path=str(SHOT_DIR / "v2_mobile_full.png"),
            full_page=True
        )
        print("✅  v2_mobile_full.png")

        # ATF
        await page_m.screenshot(
            path=str(SHOT_DIR / "v2_mobile_atf.png"),
            full_page=False
        )
        print("✅  v2_mobile_atf.png")

        # Sticky bar (scroll 500px)
        await page_m.evaluate("window.scrollTo(0, 500)")
        await page_m.wait_for_timeout(600)
        await page_m.screenshot(
            path=str(SHOT_DIR / "v2_mobile_sticky_bar.png"),
            full_page=False
        )
        print("✅  v2_mobile_sticky_bar.png")

        # Mid page (product options area)
        await page_m.evaluate("window.scrollTo(0, 900)")
        await page_m.wait_for_timeout(600)
        await page_m.screenshot(
            path=str(SHOT_DIR / "v2_mobile_options.png"),
            full_page=False
        )
        print("✅  v2_mobile_options.png")

        # Cart drawer on mobile
        await page_m.evaluate("window.scrollTo(0, 0)")
        await page_m.wait_for_timeout(400)
        await page_m.evaluate("document.getElementById('atcBtn').scrollIntoView()")
        await page_m.wait_for_timeout(400)
        await page_m.evaluate("document.getElementById('atcBtn').click()")
        await page_m.wait_for_timeout(800)
        await page_m.screenshot(
            path=str(SHOT_DIR / "v2_mobile_cart_drawer.png"),
            full_page=False
        )
        print("✅  v2_mobile_cart_drawer.png")

        await ctx_m.close()
        await browser.close()

    print(f"\n📸  All V2 screenshots saved to: {SHOT_DIR}")
    print(f"    Captured at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

asyncio.run(capture())
