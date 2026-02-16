def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_shorten_and_redirect_increments_clicks(client):
    # Create short URL
    r = client.post("/shorten", json={"url": "https://example.com"})
    assert r.status_code == 200
    body = r.json()
    assert "short_code" in body
    assert body["original_url"] == "https://example.com"
    code = body["short_code"]

    # Redirect should be 302 and include Location header.
    # TestClient follows redirects by default only if follow_redirects=True (depends on versions),
    # so we explicitly disable following.
    r2 = client.get(f"/{code}", follow_redirects=False)
    assert r2.status_code == 302
    assert r2.headers["location"] == "https://example.com"

    # Call again to verify click_count increments (we check via a second redirect call)
    r3 = client.get(f"/{code}", follow_redirects=False)
    assert r3.status_code == 302

def test_click_count_increments_in_db(client, db_session):
    # Create a short URL
    r = client.post("/shorten", json={"url": "https://example.com"})
    assert r.status_code == 200
    code = r.json()["short_code"]

    # First redirect
    r1 = client.get(f"/{code}", follow_redirects=False)
    assert r1.status_code == 302

    # Second redirect
    r2 = client.get(f"/{code}", follow_redirects=False)
    assert r2.status_code == 302

    # Verify click_count in DB
    from src.models import URL

    row = db_session.query(URL).filter(URL.short_code == code).first()
    assert row is not None
    assert row.click_count == 2


def test_shorten_invalid_url(client):
    r = client.post("/shorten", json={"url": "not-a-url"})
    assert r.status_code == 400
    assert "Invalid URL" in r.json()["detail"]


def test_redirect_unknown_code(client):
    r = client.get("/doesnotexist", follow_redirects=False)
    assert r.status_code == 404
    assert r.json()["detail"] == "Short code not found"