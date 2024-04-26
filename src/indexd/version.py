from importlib import resources

import versionista


def get_version() -> versionista.VersionData:
    with resources.path("indexd", "versionista.txt") as p:
        return versionista.package_version(p)
