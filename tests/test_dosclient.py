import json


def test_dos_load():
    """
    Test loading a DOS Schema
    """

    jsonstring = """
    {"data_object": {"updated": "2018-05-26T133720.895752ZZ", "name": "NWD315403.recab.cram", "version": "2018-05-26T133720.895752Z", "urls": [{"url": "gs://cgp-commons-multi-region-public/topmed_open_access/d688eb64-049c-5c3a-bc51-75e50791be49/NWD315403.recab.cram"}, {"url": "s3://cgp-commons-public/topmed_open_access/d688eb64-049c-5c3a-bc51-75e50791be49/NWD315403.recab.cram"}], "checksums": [{"checksum": "adc549efb6ce05e5c141c96ed6a4f33df023fbfc", "type": "md5"}], "size": "19404138841", "id": "be07e9bd-f750-4686-9777-57edaad08ffb", "aliases": ["repoDataBundleId:be07e9bd-f750-4686-9777-57edaad08ffb", "center_name:UW", "submitter_donor_id:", "sampleId:df7351bb-835e-4330-bffd-9b66045858a5", "submittedSampleId:NWD315403", "repoBaseUrl:", "analysis_type:", "repoCode:DSS-AWS-Oregon", "aliases:[u'dg.4503/be07e9bd-f750-4686-9777-57edaad08ffb']", "repoOrg:UCSC", "file_type:cram", "submittedSpecimenId:NWD315403", "file_version:2018-05-26T133720.895752Z", "workflow:", "access:public", "fileMd5sum:adc549efb6ce05e5c141c96ed6a4f33df023fbfc", "program:TOPMed", "repoType:HCA DSS", "repoName:DSS-AWS-Oregon", "donor:04733067-8a9a-4088-b623-b11debb5caf6", "workflowVersion:", "experimentalStrategy:", "download_id:be07e9bd-f750-4686-9777-57edaad08ffb", "repoCountry:US", "fileSize:19404138841", "submittedDonorId:HG01249", "specimen_type:Normal - blood derived", "metadataJson:", "lastModified:2018-05-26T133720.895752Z", "study:topmed-public", "submitterDonorPrimarySite:B-lymphocyte", "specimenUUID:4ba2771a-57d9-477f-b0c9-306fceb0a29b", "project:topmed-public", "redwoodDonorUUID:", "title:NWD315403.recab.cram", "software:", "file_id:be07e9bd-f750-4686-9777-57edaad08ffb"]}}
    """

    from indexd.doi.dosclient import DOSClient
    from indexd.doi.dosclient import Document
    client = DOSClient("https://test.example/index")
    doc = Document(client, "be07e9bd-f750-4686-9777-57edaad08ffb", json.loads(jsonstring))
