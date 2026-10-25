def test_root_increments(client):
    assert client.get("/").json() == {"visites": 1}
    assert client.get("/").json() == {"visites": 2}


def test_health_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_health_redis_down(client, fake_server):
    fake_server.connected = False
    resp = client.get("/health")
    assert resp.status_code == 503
    assert resp.text == "redis down"


def test_metrics_counts_requests(client):
    client.get("/")
    body = client.get("/metrics").text
    assert 'http_requests_total{method="GET",path="/",status="200"}' in body
    assert "http_request_duration_seconds" in body


def test_reset_counter(client):
    # incremente quelques fois
    client.get("/")
    client.get("/")

    # remise a zero
    resp = client.post("/reset")

    assert resp.status_code == 200
    assert resp.json() == {"visites": 0}

    # verifie que le compteur repart a 1
    resp = client.get("/")
    assert resp.json() == {"visites": 1}


def test_root_header_version(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.headers.get("X-Visites-Version") == "0.1.0"
