import json
from pathlib import Path

from playwright.sync_api import sync_playwright

out = Path(__file__).resolve().parents[1] / "demo/evidence"
out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    context = browser.new_context(
        viewport={"width": 1440, "height": 1000},
        record_video_dir=str(out / "browser-video"),
    )
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto("http://localhost:3002")
    page.get_by_role("button", name="New ticket", exact=True).click()
    page.get_by_label("Subject", exact=True).fill("Lab projector loses HDMI signal")
    page.get_by_label("Requester email").fill("student@example.com")
    page.get_by_label("Campus location").fill("North campus, Lab 204")
    page.get_by_role("combobox", name="Category", exact=True).select_option("HARDWARE")
    page.get_by_label("Description", exact=True).fill(
        "Synthetic campus demonstration: projector disconnects during presentations."
    )
    page.get_by_label("Assigned to").fill("Campus IT")
    page.screenshot(path=str(out / "ticket-create.png"), full_page=True)
    page.get_by_role("button", name="Create ticket", exact=True).click()
    ticket = page.get_by_role(
        "button", name="Lab projector loses HDMI signal", exact=False
    )
    ticket.wait_for()
    ticket.click()
    page.get_by_role("combobox", name="Category", exact=True).select_option("SOFTWARE")
    page.get_by_label("Campus location").fill("North campus, Lab 205")
    page.locator("select[name=status]").select_option("IN_PROGRESS")
    page.get_by_role("button", name="Save changes", exact=True).click()
    ticket.wait_for()
    result = context.request.get("http://localhost:3002/api/tickets?search=Lab%20205")
    assert result.ok and result.json()[0]["category"] == "SOFTWARE"
    page.get_by_label("Search tickets").fill("Lab 205")
    page.wait_for_timeout(500)
    assert page.locator("tbody tr").count() == 1
    page.get_by_label("Search tickets").fill("software")
    page.wait_for_timeout(500)
    assert page.locator("tbody tr").count() == 1
    page.get_by_label("Search tickets").fill("")
    for subject, category, location, priority in [
        ("Campus Wi-Fi drops during lectures", "NETWORK", "Lecture hall A", "URGENT"),
        (
            "Reset library workstation access",
            "ACCOUNT",
            "Library ground floor",
            "MEDIUM",
        ),
    ]:
        response = context.request.post(
            "http://localhost:3002/api/tickets",
            data={
                "subject": subject,
                "requester_email": "demo@example.com",
                "category": category,
                "location": location,
                "priority": priority,
            },
        )
        assert response.status == 201
    page.reload()
    page.get_by_role("button", name="Campus Wi-Fi drops", exact=False).wait_for()
    page.screenshot(path=str(out / "application-desktop.png"), full_page=True)
    page.set_viewport_size({"width": 390, "height": 844})
    page.screenshot(path=str(out / "application-mobile.png"), full_page=True)
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    row = page.locator("tr").filter(has_text="Lab projector loses HDMI signal")
    assert row.get_by_role("button", name="Edit ticket", exact=False).is_visible()
    assert row.get_by_role("button", name="Delete ticket", exact=False).is_visible()
    assert "Lab 205" in row.inner_text() and "Software" in row.inner_text()
    page.once("dialog", lambda dialog: dialog.accept())
    row.get_by_role("button", name="Delete ticket", exact=False).click()
    row.wait_for(state="detached")
    assert not errors, errors
    context.close()
    browser.close()
(out / "browser-check.json").write_text(
    json.dumps(
        {
            "passed": True,
            "checks": [
                "create campus ticket",
                "edit category and location",
                "location search",
                "category search",
                "delete",
                "desktop",
                "mobile details and actions",
                "no horizontal overflow",
                "no JavaScript errors",
            ],
            "data": "synthetic campus demonstration tickets",
        },
        indent=2,
    )
    + "\n"
)
print("PASS: CampusDesk browser workflow, campus fields and mobile accessibility")
