"""Invite repository interface"""
from abc import ABC, abstractmethod
from typing import List

from src.models.invite import Invite


class InviteRepositoryInterface(ABC):
    """
    Interface for class for manipulating with invite data

    Methods
    -------
    async get_invites_by_author_id(author_id)
        Returns invites that has matches with given author id.
    async get_invite_by_invite_id(invitee_id)
        Returns invite that has matches with given invite id.
    async get_all_invites()
        Returns all invites.
    async get_invites_by_invitee_id(invitee_id)
        Returns invites that has matches with given invitee id.
    async create_invite(invite)
        Creates new invite inside db or throws an exception.
    async update_invite(invite)
        Updates invite that has the same id as provided invite object inside db or throws an exception.
    async delete_invite(invite_id)
        Deletes invite that has matching id from database or throws an exception.

    """

    @abstractmethod
    async def get_invites_by_author_id(self, author_id: str) -> List[Invite]:
        """
        Get invites by author id.

        Parameters
        ----------
        author_id : str
            Author's id.

        Returns
        -------
        List[Invite]
            List of invites that matches by author id.

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
    async def get_all_invites(self) -> List[Invite]:
        """
        Get all invites.

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
    async def get_invites_by_invitee_id(self, invitee_id: str) -> List[Invite]:
        """
        Get invites by invitee id.

        Parameters
        ----------
        invitee_id : str
            invitee id object.

        Returns
        -------
        List[Invite]
            List of invites that matches by invitee id.

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
        Create an invite.

        Parameters
        ----------
        invite : Invite
            Invite object.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

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
    async def delete_invite(self, invite_id: str) -> None:
        """
        Delete the invite.

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
