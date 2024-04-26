"""Invite repository with data from database."""

from datetime import datetime
from typing import List, Optional

from prisma.models import Invite as PrismaInvite

from db.postgres_client import PostgresClient
from errors.value_not_found_error import ValueNotFoundError
from src.models.invite import Invite, InviteStatus
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
    async get_invites_by_author_id(author_id, status)
        Returns invites that has matches with given author id.
    async get_invite_by_invite_id(invite_id)
        Returns invite that has matches with given invite id.
    async get_all_invites(status)
        Returns all invites.
    async get_invites_by_invitee_id(invitee_id, status)
        Returns invites that has matches with given invitee id.
    async create_invite(invite)
        Creates new invite inside db or throws an exception.
    async update_invite(incite)
        Updates invite that has the same id as provided invite object inside db or throws an exception.
    async delete_invite(invite_id)
        Deletes invite that has matching id from database or throws an exception.

    """

    _db_client: PostgresClient

    def __init__(self) -> None:
        self._db_client = PostgresClient()

    async def get_invites_by_author_id(
        self, author_id: str, status: Optional[InviteStatus]
    ) -> List[Invite]:
        """
        Get invites by author id.

        Parameters
        ----------
        status : Optional[InviteStatus]
            Optional invite status. If present will filter the events by status
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
        db_invites: Optional[
            List[PrismaInvite]
        ] = await self._db_client.db.invite.find_many(
            where={
                "author_id": author_id,
                "deleted_at": None,
            }
            | ({"status": str(status)} if status is not None else {})
        )
        if db_invites is None or len(db_invites) == 0:
            raise ValueNotFoundError("Invites not found")
        return [
            Invite.from_prisma_invite(prisma_invite=db_invite)
            for db_invite in db_invites
        ]

    async def get_invite_by_invite_id(self, invite_id: str) -> Invite:
        """
        Get invite by invite id.

        Parameters
        ----------
        invite_id : str
            Invite's id.

        Returns
        -------
        Invite
            Invite that matches by invite id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No invite was found for given invite id.

        """
        db_invite: Optional[PrismaInvite] = await self._db_client.db.invite.find_first(
            where={"id": invite_id, "deleted_at": None}
        )
        if db_invite is None:
            raise ValueNotFoundError("Invite not found")
        return Invite.from_prisma_invite(prisma_invite=db_invite)

    async def get_all_invites(self, status: Optional[InviteStatus]) -> List[Invite]:
        """
        Get all invites.

        Attributes
        ----------
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
        db_invites: Optional[
            List[PrismaInvite]
        ] = await self._db_client.db.invite.find_many(
            where={"status": str(status)} if status is not None else None
        )
        if db_invites is None or len(db_invites) == 0:
            raise ValueNotFoundError("Invites not found")
        return [
            Invite.from_prisma_invite(prisma_invite=db_invite)
            for db_invite in db_invites
        ]

    async def get_invites_by_invitee_id(
        self, invitee_id: str, status: Optional[InviteStatus]
    ) -> List[Invite]:
        """
        Get invites by invitee id.

        Parameters
        ----------
        invitee_id : str
            Invitee's id object.
        status : Optional[InviteStatus]
            Optional invite status. If present will filter the events by status

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
        db_invites: Optional[
            List[PrismaInvite]
        ] = await self._db_client.db.invite.find_many(
            where={
                "invitee_id": invitee_id,
                "deleted_at": None,
            }
            | ({"status": str(status)} if status is not None else {})
        )
        if db_invites is None or len(db_invites) == 0:
            raise ValueNotFoundError("Invites not found")
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
        await self._db_client.db.invite.create(
            data=invite.to_dict(exclude=["created_at", "deleted_at"])
        )

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

    async def delete_invite_by_invite_id(self, invite_id: str) -> None:
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
        await self._db_client.db.invite.update_many(
            where={"event_id": event_id, "deleted_at": None},
            data={"deleted_at": datetime.now()},
        )

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
        await self._db_client.db.invite.update_many(
            where={"author_id": author_id, "deleted_at": None},
            data={"deleted_at": datetime.now()},
        )

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
        await self._db_client.db.invite.update_many(
            where={"invitee_id": invitee_id, "deleted_at": None},
            data={"deleted_at": datetime.now()},
        )
