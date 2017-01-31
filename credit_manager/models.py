# -*- coding: utf-8 -*-
"""`credit_manager.handlers` module.

Provides app web handlers.
"""


from schema_factory import BaseSchema, StringNode, SchemaError
from settings import POSTGRES
from lunatic import QueryManager, QueryManagerError, DBEngine, DBEngineError
from os import path
from credit_manager.errors import ModelError


db_engine = DBEngine(pool_factory='queue', **POSTGRES)


class CreditSchema(BaseSchema):
    """Base credit schema class.
    """

    uid = StringNode()
    client_name = StringNode(required=True)
    description = StringNode(required=True)
    start = StringNode(required=True)

    @property
    def id(self):
        return self.uid

    @property
    def title(self):
        return self.client_name


class CreditModel(object):
    """Base credit model class.

    It encapsulates query mechanism and validation.
    """

    schema = CreditSchema

    engine = QueryManager(engine=db_engine).load(
        query_parent=path.dirname(path.abspath(__file__)),
        query_dir='db',
        query_file='credit.sql'
    )

    @classmethod
    def exists(cls, uid):
        """Check if credit record exists based on UID.

        Args:
            uid (str): Record UID

        Returns:
            True if record exists else False.
        """

        try:
            return cls.engine.exists(uid=uid, fetch_many=False).get('exists')

        except QueryManagerError as error:
            raise ModelError(error.args[0])

    @classmethod
    def create(cls, data):
        """Create a new Credit Model.

        Args:
            data (dict): New Model key/value data.

        Returns:
            A model schema instance.
        """
        try:
            cleaned_data = cls.schema(**data)

            record = cls.engine.create(
                uid=cleaned_data.id,
                start=cleaned_data.start,
                description=cleaned_data.description,
                client_name=cleaned_data.client_name,
                fetch_many=False
            )

        except (SchemaError, QueryManagerError) as error:
            raise ModelError(error.args[0])

        return cls.schema(**record).serialize()

    @classmethod
    def retrieve(cls, uid):
        """Retrieve Credit based on UID.

        Args:
            uid (str): Record UID.

        Returns:
            Record data.
        """

        if not cls.exists(uid):
            raise ModelError('Credit with UID {} does not exist!')

        try:
            record = cls.engine.retrieve(uid=uid, fetch_many=False)
            credit_model = cls.schema(**record).serialize()

        except (QueryManagerError, SchemaError) as error:
            raise ModelError(error.args[0])

        return credit_model

    @classmethod
    def update(cls, uid, data):
        """Update Credit Model.

        Args:
            uid (str): Record UID.
            data (dict): New key/value data for update.

        Returns:
            A model schema instance.
        """
        try:
            cleaned_data = cls.schema(uid=uid, **data)

            record = cls.engine.update(
                uid=cleaned_data.id,
                start=cleaned_data.start,
                description=cleaned_data.description,
                client_name=cleaned_data.client_name,
                fetch_many=False
            )

        except (SchemaError, QueryManagerError) as error:
            raise ModelError(error.args[0])

        return cls.schema(**record).serialize()

    @classmethod
    def delete(cls, uid):
        """Delete Credit based on UID.

        Args:
            uid (str): Record UID.

        Returns:
            Deleted Record data.
        """

        if not cls.exists(uid):
            raise ModelError('Credit with UID {} does not exist!')

        try:
            record = cls.engine.delete(uid=uid, fetch_many=False)
            credit_model = cls.schema(**record).serialize()

        except (QueryManagerError, SchemaError) as error:
            raise ModelError(error.args[0])

        return credit_model

    @classmethod
    def list(cls, start=None, stop=None):
        """Filter Credit model collection.

        Args:
            start (str): String formatted  date.
            stop (str): String formatted  date.

        Returns:
            A List of schema instances.
        """
        try:
            raw_records = cls.engine.list(start=start, stop=stop, fetch_many=True)
            credit_records = [cls.schema(**record).serialize() for record in raw_records]

        except (QueryManagerError, SchemaError) as error:
            raise ModelError(error.args[0])

        return credit_records
