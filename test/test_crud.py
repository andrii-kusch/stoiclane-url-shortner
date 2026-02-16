from src import crud


def test_create_url_sets_short_code(db_session):
    row = crud.create_url(db_session, "https://example.com")
    assert row.id is not None
    assert row.short_code is not None
    assert row.original_url == "https://example.com"
    assert row.click_count == 0


def test_get_url_by_code(db_session):
    row = crud.create_url(db_session, "https://example.com/a")
    fetched = crud.get_url_by_code(db_session, row.short_code)
    assert fetched is not None
    assert fetched.id == row.id
    assert fetched.original_url == "https://example.com/a"


def test_increment_click_count(db_session):
    row = crud.create_url(db_session, "https://example.com/b")
    assert row.click_count == 0

    crud.increment_click_count(db_session, row)
    fetched = crud.get_url_by_code(db_session, row.short_code)
    assert fetched.click_count == 1

    crud.increment_click_count(db_session, fetched)
    fetched2 = crud.get_url_by_code(db_session, row.short_code)
    assert fetched2.click_count == 2