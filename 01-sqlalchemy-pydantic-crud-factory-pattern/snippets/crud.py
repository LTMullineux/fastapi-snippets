from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from snippets.models import (
    SnippetModel,
    SnippetSchema,
    User,
    UserInSchema,
    UserSchema,
    UserUpdateSchema,
)


class SnippetException(Exception):
    pass


class IntegrityConflictException(Exception):
    pass


class NotFoundException(Exception):
    pass


def CrudFactory(model: SnippetModel):
    class AsyncCrud:
        @classmethod
        async def create(
            cls,
            session: AsyncSession,
            data: SnippetSchema,
        ) -> SnippetModel:
            """Accepts a Pydantic model, creates a new record in the database, catches
            any integrity errors, and returns the record.

            Args:
                session (AsyncSession): SQLAlchemy async session
                data (SnippetSchema): Pydantic model

            Raises:
                IntegrityConflictException: if creation conflicts with existing data
                SnippetException: if an unknown error occurs

            Returns:
                SnippetModel: created SQLAlchemy model
            """
            try:
                db_model = model(**data.model_dump())
                session.add(db_model)
                await session.commit()
                await session.refresh(db_model)
                return db_model
            except IntegrityError:
                raise IntegrityConflictException(
                    f"{model.__tablename__} conflicts with existing data.",
                )
            except Exception as e:
                raise SnippetException(f"Unknown error occurred: {e}") from e

        @classmethod
        async def create_many(
            cls,
            session: AsyncSession,
            data: list[SnippetSchema],
            return_models: bool = False,
        ) -> list[SnippetModel] | bool:
            """_summary_

            Args:
                session (AsyncSession): SQLAlchemy async session
                data (list[SnippetSchema]): list of Pydantic models
                return_models (bool, optional): Should the created models be returned
                    or a boolean indicating they have been created. Defaults to False.

            Raises:
                IntegrityConflictException: if creation conflicts with existing data
                SnippetException: if an unknown error occurs

            Returns:
                list[SnippetModel] | bool: list of created SQLAlchemy models or boolean
            """
            db_models = [model(**d.model_dump()) for d in data]
            try:
                session.add_all(db_models)
                await session.commit()
            except IntegrityError:
                raise IntegrityConflictException(
                    f"{model.__tablename__} conflict with existing data.",
                )
            except Exception as e:
                raise SnippetException(f"Unknown error occurred: {e}") from e

            if not return_models:
                return True

            for m in db_models:
                await session.refresh(m)

            return db_models

        @classmethod
        async def get_one_by_id(
            cls,
            session: AsyncSession,
            id_: str | UUID,
            column: str = "uuid",
            with_for_update: bool = False,
        ) -> SnippetModel:
            """Fetches one record from the database based on a column value and returns
            it, or returns None if it does not exist. Raises an exception if the column
            doesn't exist.

            Args:
                session (AsyncSession): SQLAlchemy async session
                id_ (str | UUID): value to search for in `column`.
                column (str, optional): the column name in which to search.
                    Defaults to "uuid".
                with_for_update (bool, optional): Should the returned row be locked
                    during the lifetime of the current open transactions.
                    Defaults to False.

            Raises:
                SnippetException: if the column does not exist on the model

            Returns:
                SnippetModel: SQLAlchemy model or None
            """
            try:
                q = select(model).where(getattr(model, column) == id_)
            except AttributeError:
                raise SnippetException(
                    f"Column {column} not found on {model.__tablename__}.",
                )

            if with_for_update:
                q = q.with_for_update()

            results = await session.execute(q)
            return results.unique().scalar_one_or_none()

        @classmethod
        async def get_many_by_ids(
            cls,
            session: AsyncSession,
            ids: list[str | UUID] = None,
            column: str = "uuid",
            with_for_update: bool = False,
        ) -> list[SnippetModel]:
            """Fetches multiple records from the database based on a column value and
            returns them. Raises an exception if the column doesn't exist.

            Args:
                session (AsyncSession): SQLAlchemy async session
                ids (list[str  |  UUID], optional): list of values to search for in
                    `column`. Defaults to None.
                column (str, optional): the column name in which to search
                    Defaults to "uuid".
                with_for_update (bool, optional): Should the returned rows be locked
                    during the lifetime of the current open transactions.
                    Defaults to False.

            Raises:
                SnippetException: if the column does not exist on the model

            Returns:
                list[SnippetModel]: list of SQLAlchemy models
            """
            q = select(model)
            if ids:
                try:
                    q = q.where(getattr(model, column).in_(ids))
                except AttributeError:
                    raise SnippetException(
                        f"Column {column} not found on {model.__tablename__}.",
                    )

            if with_for_update:
                q = q.with_for_update()

            rows = await session.execute(q)
            return rows.unique().scalars().all()

        @classmethod
        async def update_by_id(
            cls,
            session: AsyncSession,
            data: SnippetSchema,
            id_: str | UUID,
            column: str = "uuid",
        ) -> SnippetModel:
            """Updates a record in the database based on a column value and returns the
            updated record. Raises an exception if the record isn't found or if the
            column doesn't exist.

            Args:
                session (AsyncSession): SQLAlchemy async session
                data (SnippetSchema): Pydantic schema for the updated data.
                id_ (str | UUID): value to search for in `column`
                column (str, optional): the column name in which to search
                    Defaults to "uuid".
            Raises:
                NotFoundException: if the record isn't found
                IntegrityConflictException: if the update conflicts with existing data

            Returns:
                SnippetModel: updated SQLAlchemy model
            """
            db_model = await cls.get_one_by_id(
                session, id_, column=column, with_for_update=True
            )
            if not db_model:
                raise NotFoundException(
                    f"{model.__tablename__} {column}={id_} not found.",
                )

            values = data.model_dump(exclude_unset=True)
            for k, v in values.items():
                setattr(db_model, k, v)

            try:
                await session.commit()
                await session.refresh(db_model)
                return db_model
            except IntegrityError:
                raise IntegrityConflictException(
                    f"{model.__tablename__} {column}={id_} conflict with existing data.",
                )

        @classmethod
        async def update_many_by_ids(
            cls,
            session: AsyncSession,
            updates: dict[str | UUID, SnippetSchema],
            column: str = "uuid",
            return_models: bool = False,
        ) -> list[SnippetModel] | bool:
            """Updates multiple records in the database based on a column value and
            returns the updated records. Raises an exception if the column doesn't
            exist.

            Args:
                session (AsyncSession): SQLAlchemy async session
                updates (dict[str  |  UUID, SnippetSchema]): dictionary of id_ to
                    Pydantic update schema
                column (str, optional): the column name in which to search.
                    Defaults to "uuid".
                return_models (bool, optional): Should the created models be returned
                    or a boolean indicating they have been created. Defaults to False.
                    Defaults to False.

            Raises:
                IntegrityConflictException: if the update conflicts with existing data

            Returns:
                list[SnippetModel] | bool: list of updated SQLAlchemy models or boolean
            """
            updates = {str(id): update for id, update in updates.items() if update}
            ids = list(updates.keys())
            db_models = await cls.get_many_by_ids(
                session, ids=ids, column=column, with_for_update=True
            )

            for db_model in db_models:
                values = updates[str(getattr(db_model, column))].model_dump(
                    exclude_unset=True
                )
                for k, v in values.items():
                    setattr(db_model, k, v)
                session.add(db_model)

            try:
                await session.commit()
            except IntegrityError:
                raise IntegrityConflictException(
                    f"{model.__tablename__} conflict with existing data.",
                )

            if not return_models:
                return True

            for db_model in db_models:
                await session.refresh(db_model)

            return db_models

        @classmethod
        async def remove_by_id(
            cls,
            session: AsyncSession,
            id_: str | UUID,
            column: str = "uuid",
        ) -> int:
            """Removes a record from the database based on a column value. Raises an
            exception if the column doesn't exist.

            Args:
                session (AsyncSession): SQLAlchemy async session
                id (str | UUID): value to search for in `column` and delete
                column (str, optional): the column name in which to search.
                    Defaults to "uuid".

            Raises:
                SnippetException: if the column does not exist on the model

            Returns:
                int: number of rows removed, 1 if successful, 0 if not. Can be greater
                    than 1 if id_ is not unique in the column.
            """
            try:
                query = delete(model).where(getattr(model, column) == id_)
            except AttributeError:
                raise SnippetException(
                    f"Column {column} not found on {model.__tablename__}.",
                )

            rows = await session.execute(query)
            await session.commit()
            return rows.rowcount

        @classmethod
        async def remove_many_by_ids(
            cls,
            session: AsyncSession,
            ids: list[str | UUID],
            column: str = "uuid",
        ) -> int:
            """Removes multiple records from the database based on a column value.
            Raises an exception if the column doesn't exist.

            Args:
                session (AsyncSession): SQLAlchemy async session
                ids (list[str  |  UUID]): list of values to search for in `column` and
                column (str, optional): the column name in which to search.
                    Defaults to "uuid".

            Raises:
                SnippetException: if ids is empty to stop deleting an entire table
                SnippetException: if column does not exist on the model

            Returns:
                int: _description_
            """
            if not ids:
                raise SnippetException("No ids provided.")

            try:
                query = delete(model).where(getattr(model, column).in_(ids))
            except AttributeError:
                raise SnippetException(
                    f"Column {column} not found on {model.__tablename__}.",
                )

            rows = await session.execute(query)
            await session.commit()
            return rows.rowcount

    AsyncCrud.model = model
    return AsyncCrud


class UserCrud(CrudFactory(User)):

    @classmethod
    async def create_many(cls, *args, **kwargs) -> list[User]:
        raise NotImplementedError("Create many not implemented for users.")

    @classmethod
    async def update_many_by_ids(cls, *args, **kwargs) -> list[User] | bool:
        raise NotImplementedError("Update many not implemented for users.")

    @classmethod
    def format_user_with_password(cls, user: UserInSchema) -> UserSchema:
        """Take a Pydantic UserInSchema and return a UserSchema with the password
        hashed.

        Args:
            user (UserInSchema): Pydantic UserInSchema holding the user information

        Returns:
            UserSchema: Pydantic UserSchema with the password hashed
        """
        user_data = user.model_dump()
        password = user_data.pop("password")
        db_user = UserSchema(
            **user_data, hashed_password=cls.get_password_hash(password)
        )
        return db_user

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """Perform hashing of passwords. This is a simple example and should not be used
        in production. A simple example:

            ```python
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

            def verify_password(plain_password: str, hashed_password: str) -> bool:
                return pwd_context.verify(plain_password, hashed_password)

            def get_password_hash(password: str) -> str:
                return pwd_context.hash(password)
            ```

        Args:
            password (str): user's password

        Returns:
            str: user's hashed password
        """
        # NOTE: do not ever do this in production
        return password[::-1]

    @classmethod
    async def create(cls, session: AsyncSession, data: UserInSchema) -> User:
        """Create a user in the database. This method is overridden to hash the password
        and then calls the parent create method, with the hashed password.

        Args:
            session (AsyncSession): SQLAlchemy async session
            data (UserInSchema): Pydantic UserInSchema holding the user information

        Returns:
            User: SQLAlchemy User model
        """
        db_user = cls.format_user_with_password(data)
        return await super(cls, cls).create(session, data=db_user)

    @classmethod
    async def update_by_id(
        cls,
        session: AsyncSession,
        data: UserUpdateSchema,
        id_: str | UUID,
        column: str = "uuid",
    ) -> User:
        """Updates a user in the database based on a column value and returns the
        updated user. Raises an exception if the user isn't found or if the column
        doesn't exist.

        Overrides the parent method to hash the password if it is included in the
        update.

        Args:
            session (AsyncSession): SQLAlchemy async session
            data (UserUpdateSchema): Pydantic schema for the updated data.
            id_ (str | UUID): value to search for in `column`
            column (str, optional): the column name in which to search.
                Defaults to "uuid".

        Raises:
            NotFoundException: user not found in database given id_ and column
            IntegrityConflictException: update conflicts with existing data

        Returns:
            User: updated SQLAlchemy model
        """
        db_model = await cls.get_one_by_id(
            session, id_, column=column, with_for_update=True
        )
        if not db_model:
            raise NotFoundException(
                f"{User.__tablename__} id={id_} not found.",
            )

        values = data.model_dump(exclude_unset=True, exclude={"password"})
        for k, v in values.items():
            setattr(db_model, k, v)

        if data.password is not None:
            db_model.hashed_password = cls.get_password_hash(data.password)

        try:
            await session.commit()
            await session.refresh(db_model)
            return db_model
        except IntegrityError as e:
            raise IntegrityConflictException(
                f"{User.__tablename__} {column}={id_} conflict with existing data.",
            ) from e
