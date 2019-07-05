import uuid

from indexd_test_utils import (
    create_random_index,
    create_random_index_version,
)


def test_random_index_version(indexd_client):
    uuid1 = str(uuid.uuid4())

    doc1 = create_random_index(
        indexd_client,
        str(uuid.uuid4()),
        u'1'
    )

    uuid2 = str(uuid.uuid4())

    doc2 = create_random_index_version(
        indexd_client,
        doc1.did,
        version_did=uuid2,
        version=u'2'
    )

    file_name = '{}_warning_huge_file.svs'\
        .format(uuid2)

    url = 's3://super-safe.com/' + file_name

    assert doc2
    assert sorted(doc2.acl) == ['ax', 'bx']
    assert doc2.size
    assert doc2.hashes.get('md5')
    assert doc2.urls[0] == url
    assert doc2.form == 'object'
    assert doc2.file_name == file_name
    assert doc2.urls_metadata.get(url) == {'a': 'b'}
    assert doc2.version == '2'
