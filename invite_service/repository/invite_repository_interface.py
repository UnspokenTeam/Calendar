"""Invite repository interface"""
from abc import ABC, abstractmethod
from typing import List

from src.models.invite import Invite


class InviteRepositoryInterface(ABC):
    """
    Interface for class for manipulating with invite data

    Methods
    -------
    async get_invites(author_id)
        Returns invites that has matches with given author id.
    async create_invite(invite)
        Creates new invite inside db or throws an exception.
    async update_invite(invite)
        Updates invite that has the same id as provided invite object inside db or throws an exception.
    async delete_invite(invite_id)
        Deletes invite that has matching id from database or throws an exception.
    async get_all_invites()
        Returns all invites.
    async get_invites_by_invitee_id(invitee_id)
        Returns invites that has matches with given invitee id.

    """

    @abstractmethod
    async def get_invites(self, author_id: str) -> List[Invite]:
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
            No invites was found for given author id.

        """
        pass

    @abstractmethod
    async def get_all_invites(self) -> List[Invite]:
        """
        Get all invites.

        Parameters
        ----------
        invite : Invite
            invite object.

        Returns
        -------
        List[Invite]
            List of all invites.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No invites was found.

        """
        pass

    @abstractmethod
    async def get_invites_by_invitee_id(self, invitee_id: str) -> List[Invite]:
        """
        Get invites by invitee id.

        Parameters
        ----------
        invitee_id : str
            invitee_id object.

        Returns
        -------
        List[Invite]
            List of invites that matches by invitee id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No invites was found for given invitee id.

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
