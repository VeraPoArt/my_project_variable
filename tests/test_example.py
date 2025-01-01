def test_open_page(page, config):
    page.goto(config["base_url"])
    assert page.get_by_role("heading", name="Example Domain").is_visible()