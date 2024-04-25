from abc import ABC, abstractmethod


class CRUDRepository(ABC):

    @abstractmethod
    async def get_one(*args, **kwargs):
        """
        Get one record in table
        """

        pass

    @abstractmethod
    async def get_all_records(*args, **kwargs):
        """
        Get all records in table
        """

        pass

    @abstractmethod
    async def add_record(*args, **kwargs):
        """
        Add a new record in table
        """

        pass

    @abstractmethod
    async def update_record(*args, **kwargs):
        """
        Update data about of record in table
        """

        pass

    @abstractmethod
    async def del_record(*args, **kwargs):
        """
        Delete record in table
        """

        pass