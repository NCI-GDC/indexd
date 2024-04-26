from packaging.version import Version


def test_index_get(indexd_systems_api):

    version_data = indexd_systems_api.version_get()
    version = Version(version_data.version)
    assert version.major is not None
    assert len(version_data.commit) > 6
