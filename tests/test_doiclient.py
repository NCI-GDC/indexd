def test_get_matsu():
    from indexd.doi.doiclient import DOIClient
    
    signpost = DOIClient(baseurl="https://doi.org/")
    
    res = signpost.get("10.1007/s41060-017-0052-3")
    res = res.to_json()
    assert res["urls"] == ["http://link.springer.com/article/10.1007/s41060-017-0052-3/fulltext.html", "http://link.springer.com/content/pdf/10.1007/s41060-017-0052-3.pdf", "http://link.springer.com/content/pdf/10.1007/s41060-017-0052-3.pdf"]
    assert res["did"] == "10.1007/s41060-017-0052-3"
    assert res["rev"] == None
    assert res["size"] == None
