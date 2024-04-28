"""Invite repository interface"""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.invite import Invite, InviteStatus


class InviteRepositoryInterface(ABC):
    """
    Interface for class for manipulating with invite data

    Methods
    -------
    async get_invites_by_author_id(author_id, status)
        Returns invites that have matches with given author id.
    async get_invites_by_event_id(event_id, status)
        Returns invites that have matches with given event id.
    async get_invite_by_invite_id(invite_id)
        Returns invite that has matches with given invite id.
    async get_all_invites(status)
        Returns all invites.
    async get_invites_by_invitee_id(invitee_id, status)
        Returns invites that have matches with given invitee id.
    async create_invite(invite)
        Creates new invite if does not exist or update the existing one.
    async create_multiple_invites(invites)
        Create multiple invites.
    async update_invite(invite)
        Updates invite that has the same id as provided invite object inside db.
    async delete_invite_by_invite_id(invite_id)
        Deletes invite that has matching id.
    async delete_invite_by_event_id(event_id)
        Deletes invites that have matching event id.
    async delete_invite_by_author_id(author_id)
        Deletes invites that have matching author id.
    async delete_invite_by_invitee_id(invitee_id)
        Deletes invites that have matching invitee id.

    """

    @abstractmethod
    async def get_invites_by_event_id(self, event_id: str, status: Optional[InviteStatus]) -> List[Invite]:
        """
        Returns invites that have matching event id.

        Parameters
        ----------
        event_id : str
            Event id.
        status : Optional[InviteStatus]
            Optional invite status. If present will filter the events by status

        Returns
        -------
        List[Invite]
            Invites that have matching event id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No invites were found for given event id.

        """

    @abstractmethod
    async def get_invites_by_author_id(
        self, author_id: str, page_number: int, items_per_page: int, status: Optional[InviteStatus]
    ) -> List[Invite]:
        """
        Get invites by author id.

        Parameters
        ----------
        status : Optional[InviteStatus]
            Optional invite status. If present will filter the events by status
        author_id : str
            Author's id.
        page_number : int
            Number of page to get.
        items_per_page : int
            Number of items per page to load.

        Returns
        -------
        List[Invite]
            List of invites that have matching author id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No invites were found for given author id.

        """
        pass

    @abstractmethod
    async def get_invite_by_invite_id(self, invite_id: str) -> Invite:
        """
        Get invite by invite id.

        Parameters
        ----------
        invite_id : str
            invite's id.

        Returns
        -------
        Invite
            Invite that has matches with given invite id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No invite was found for given invite id.

        """
        pass

    @abstractmethod
    async def get_all_invites(
        self, page_number: int, items_per_page: int, status: Optional[InviteStatus]
    ) -> List[Invite]:
        """
        Get all invites.

        Parameters
        ----------
        page_number : int
            Number of page to get.
        items_per_page : int
            Number of items per page to load.
        status : Optional[InviteStatus]
            Optional invite status. If present will filter the events by status

        Returns
        -------
        List[Invite]
            List of all invites.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No invites were found.

        """
        pass

    @abstractmethod
    async def get_invites_by_invitee_id(
        self, invitee_id: str, page_number: int, items_per_page: int, status: Optional[InviteStatus]
    ) -> List[Invite]:
        """
        Get invites by invitee id.

        Parameters
        ----------
        invitee_id : str
            Invitee's id.
        page_number : int
            Number of page to get.
        items_per_page : int
            Number of items per page to load.
        status : Optional[InviteStatus]
            Optional invite status. If present will filter the events by status

        Returns
        -------
        List[Invite]
            List of invites that have matching invitee id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No invites were found for given invitee id.

        """
        pass

    @abstractmethod
    async def create_invite(self, invite: Invite) -> None:
        """
        Create an invite if does not exist or update the existing one.

        Parameters
        ----------
        invite : Invite
            Invite object.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        UniqueError
            Invite already exists.

        """
        pass

    async def create_multiple_invites(self, invites: List[Invite]) -> None:
        """
        Create multiple invites.

        Parameters
        ----------
        invites : List[Invite]
            Invite objects to create

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        UniqueError
            Some invites already exist.

        """
        pass

    @abstractmethod
    async def update_invite(self, invite: Invite) -> None:
        """
        Update invite data.

        Parameters
        ----------
        invite : Invite
            invite object.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        pass

    @abstractmethod
    async def delete_invite_by_invite_id(self, invite_id: str) -> None:
        """
        Delete the invite by invite id.

        Parameters
        ----------
        invite_id : str
            Invite id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        pass

    @abstractmethod
    async def delete_invites_by_event_id(self, event_id: str) -> None:
        """
        Delete invites by event id

        Parameters
        ----------
        event_id : str
            Event id

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        pass

    @abstractmethod
    async def delete_invites_by_author_id(self, author_id: str) -> None:
        """
        Delete invites by author id.

        Parameters
        ----------
        author_id : str
            Author id

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        pass

    @abstractmethod
    async def delete_invites_by_invitee_id(self, invitee_id: str) -> None:
        """
        Delete invites by invitee id

        Parameters
        ----------
        invitee_id : str
            Invitee id

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        pass
