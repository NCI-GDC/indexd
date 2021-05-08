from sqlalchemy import and_, func

from indexd.errors import UserError
from indexd.index.drivers.alchemy import (
    IndexRecord,
    IndexRecordUrlMetadataJsonb,
)
from indexd.index.drivers.query import URLsQueryDriver

driver_query_map = {
    "sqlite": dict(array_agg=func.group_concat, string_agg=func.group_concat),
    "postgresql": dict(array_agg=func.array_agg, string_agg=func.string_agg)
}


class AlchemyURLsQueryDriver(URLsQueryDriver):
    """SQLAlchemy based impl"""

    def __init__(self, alchemy_driver):
        """ Queries index records based on URL
        Args:
            alchemy_driver (indexd.index.drivers.alchemy.SQLAlchemyIndexDriver):
        """
        self.driver = alchemy_driver

    def query_urls(self, exclude=None, include=None, versioned=None, offset=0, limit=1000, fields="did,urls", **kwargs):

        if kwargs:
            raise UserError("Unexpected query parameter(s) {}".format(kwargs.keys()))

        versioned = versioned.lower() in ["true", "t", "yes", "y"] if versioned else None

        with self.driver.session as session:
            # special database specific functions dependent of the selected dialect
            q_func = driver_query_map.get(session.bind.dialect.name)

            query = session.query(
                IndexRecordUrlMetadataJsonb.did,
                q_func['string_agg'](IndexRecordUrlMetadataJsonb.url, ","),
            )

            # add version filter if versioned is not None
            if versioned is True:  # retrieve only those with a version number
                query = query.outerjoin(IndexRecord)
                query = query.filter(IndexRecord.version.isnot(None))
            elif versioned is False: # retrieve only those without a version number
                query = query.outerjoin(IndexRecord)
                query = query.filter(~IndexRecord.version.isnot(None))

            query = query.group_by(IndexRecordUrlMetadataJsonb.did)

            # add url filters
            if include and exclude:
                query = query.having(and_(~q_func['string_agg'](IndexRecordUrlMetadataJsonb.url, ",").contains(exclude),
                                          q_func['string_agg'](IndexRecordUrlMetadataJsonb.url, ",").contains(include)))
            elif include:
                query = query.having(q_func['string_agg'](IndexRecordUrlMetadataJsonb.url, ",").contains(include))
            elif exclude:
                query = query.having(~q_func['string_agg'](IndexRecordUrlMetadataJsonb.url, ",").contains(exclude))
            # [('did', 'urls')]
            record_list = query.order_by(IndexRecordUrlMetadataJsonb.did.asc()).offset(offset).limit(limit).all()
        return record_list

    def query_metadata_by_key(self, key, value, url=None, versioned=None, offset=0,
                              limit=1000, fields="did,urls,rev,size", **kwargs):

        if kwargs:
            raise UserError("Unexpected query parameter(s) {}".format(kwargs.keys()))

        versioned = versioned.lower() in ["true", "t", "yes", "y"] if versioned else None
        with self.driver.session as session:
            query = session.query(
                IndexRecordUrlMetadataJsonb.did,
                IndexRecordUrlMetadataJsonb.url,
                IndexRecord.rev,
                IndexRecord.size,
            )
            if key == 'type':
                query = query.filter(
                    IndexRecord.did == IndexRecordUrlMetadataJsonb.did,
                    IndexRecordUrlMetadataJsonb.type == value)
            elif key == 'state':
                query = query.filter(
                    IndexRecord.did == IndexRecordUrlMetadataJsonb.did,
                    IndexRecordUrlMetadataJsonb.state == value)
            else:
                query = query.filter(
                    IndexRecord.did == IndexRecordUrlMetadataJsonb.did,
                    IndexRecordUrlMetadataJsonb.urls_metadata[key].astext == value)

            # filter by version
            if versioned is True:
                query = query.filter(IndexRecord.version.isnot(None))
            elif versioned is False:
                query = query.filter(~IndexRecord.version.isnot(None))

            # add url filter
            if url:
                query = query.filter(IndexRecordUrlMetadataJsonb.url.like("%{}%".format(url)))

            # [('did', 'url', 'rev', 'size')]
            record_list = query.order_by(IndexRecordUrlMetadataJsonb.did.asc()).offset(offset).limit(limit).all()
        return record_list
