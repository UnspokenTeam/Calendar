"""Invite repository with data from database."""
from datetime import datetime
from typing import List, Optional

from prisma.models import Invite as PrismaInvite

from db.postgres_client import PostgresClient
from errors.value_not_found_error import ValueNotFoundError
from src.models.invite import Invite
from utils.singleton import singleton

from repository.invite_repository_interface import InviteRepositoryInterface


@singleton
class InviteRepositoryImpl(InviteRepositoryInterface):
    """
    Class for manipulating with invite data

    Attributes
    ----------
    _db_client : prisma.Client
        Postgres db client.

    Methods
    -------
    async get_invites(author_id)
        Returns invites that has matches with given author id.
    async create_invite(invite)
        Creates new invite inside db or throws an exception.
    async update_invite(incite)
        Updates invite that has the same id as provided invite object inside db or throws an exception.
    async delete_invite(invite_id)
        Deletes invite that has matching id from database or throws an exception.
    async get_all_invites()
        Returns all invites.
    async get_invites_by_invitee_id(invitee_id)
        Returns invites that has matches with given invitee id.

    """

    _db_client: PostgresClient

    def __init__(self) -> None:
        self._db_client = PostgresClient()

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
        db_invites: Optional[
            List[PrismaInvite]
        ] = await self._db_client.db.invite.find_many(
            where={"id": author_id, "deleted_at": None}
        )
        if db_invites is None or len(db_invites) == 0:
            raise ValueNotFoundError("Invites not found")
        return [
            Invite.from_prisma_invite(prisma_invite=db_invite)
            for db_invite in db_invites
        ]

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
        db_invites: Optional[
            List[PrismaInvite]
        ] = await self._db_client.db.invite.find_many()
        if db_invites is None or len(db_invites) == 0:
            raise ValueNotFoundError("Invites not found")
        return [
            Invite.from_prisma_invite(prisma_invite=db_invite)
            for db_invite in db_invites
        ]

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
        db_invites: Optional[
            List[PrismaInvite]
        ] = await self._db_client.db.invite.find_many(
            where={
                "id": {"in": [invite_id for invite_id in invitee_id]},
                "deleted_at": None,
            }
        )
        if db_invites is None or len(db_invites) == 0:
            raise ValueNotFoundError("Events not found")
        return [
            Invite.from_prisma_invite(prisma_invite=db_invite)
            for db_invite in db_invites
        ]

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
        await self._db_client.db.invite.create(data=invite.to_dict())

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
        await self._db_client.db.invite.update(
            where={"id": invite.id}, data=invite.to_dict()
        )

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
        await self._db_client.db.invite.update_many(
            where={"id": invite_id, "deleted_at": None},
            data={"deleted_at": datetime.now()},
        )
