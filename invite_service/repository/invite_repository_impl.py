"""Invite repository with data from database."""

from datetime import datetime
from typing import List, Optional

from prisma.models import Invite as PrismaInvite

from db.postgres_client import PostgresClient
from errors.unique_error import UniqueError
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

    _db_client: PostgresClient

    def __init__(self) -> None:
        self._db_client = PostgresClient()

    async def get_invites_by_event_id(
        self,
        event_id: str,
        page_number: int,
        items_per_page: int,
        status: Optional[InviteStatus],
    ) -> List[Invite]:
        """
        Get invites with matching event id

        Parameters
        ----------
        event_id : str
            Event id.
        page_number : int
            Number of page to get.
        items_per_page : int
            Number of items per page to load.
        status : Optional[InviteStatus]
            Optional invite status. If present will filter the events by status

        Returns
        -------
        List[Invite]
            Invites that have matching event id.

        Raises
        ------
        ValueNotFoundError
            Invites not found.
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        invites: Optional[
            List[PrismaInvite]
        ] = await self._db_client.db.invite.find_many(
            where={
                "event_id": event_id,
                "deleted_at": None,
            }
            | ({"status": str(status)} if status is not None else {}),
            skip=(items_per_page * (page_number - 1) if items_per_page != -1 else None),
            take=items_per_page if items_per_page != -1 else None,
        )
        if invites is None or len(invites) == 0:
            raise ValueNotFoundError("Invites not found")
        return invites

    async def get_invites_by_author_id(
        self,
        author_id: str,
        page_number: int,
        items_per_page: int,
        status: Optional[InviteStatus],
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
        db_invites: Optional[
            List[PrismaInvite]
        ] = await self._db_client.db.invite.find_many(
            where={
                "author_id": author_id,
                "deleted_at": None,
            }
            | ({"status": str(status)} if status is not None else {}),
            skip=(items_per_page * (page_number - 1) if items_per_page != -1 else None),
            take=items_per_page if items_per_page != -1 else None,
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
            Invite that has matching invite id.

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
        db_invites: Optional[
            List[PrismaInvite]
        ] = await self._db_client.db.invite.find_many(
            where={"status": str(status)} if status is not None else None,
            skip=(items_per_page * (page_number - 1) if items_per_page != -1 else None),
            take=items_per_page if items_per_page != -1 else None,
        )
        if db_invites is None or len(db_invites) == 0:
            raise ValueNotFoundError("Invites not found")
        return [
            Invite.from_prisma_invite(prisma_invite=db_invite)
            for db_invite in db_invites
        ]

    async def get_invites_by_invitee_id(
        self,
        invitee_id: str,
        page_number: int,
        items_per_page: int,
        status: Optional[InviteStatus],
    ) -> List[Invite]:
        """
        Get invites by invitee id.

        Parameters
        ----------
        invitee_id : str
            Invitee's id object.
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
        db_invites: Optional[
            List[PrismaInvite]
        ] = await self._db_client.db.invite.find_many(
            where={
                "invitee_id": invitee_id,
                "deleted_at": None,
            }
            | ({"status": str(status)} if status is not None else {}),
            skip=(items_per_page * (page_number - 1) if items_per_page != -1 else None),
            take=items_per_page if items_per_page != -1 else None,
        )
        if db_invites is None or len(db_invites) == 0:
            raise ValueNotFoundError("Invites not found")
        return [
            Invite.from_prisma_invite(prisma_invite=db_invite)
            for db_invite in db_invites
        ]

    async def create_invite(self, invite: Invite) -> Invite:
        """
        Create an invite with matching data if not exist or update existing one.

        Parameters
        ----------
        invite : Invite
            Invite object.

        Returns
        -------
        Invite
            Created invite.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        UniqueError
            Invite already exists.

        """
        prisma_db_invite = await self._db_client.db.invite.find_first(
            where={"author": invite.author_id, "invitee_id": invite.invitee_id}
        )

        if prisma_db_invite is None:
            return await self._db_client.db.invite.create(
                data=invite.to_dict(exclude=["created_at", "deleted_at"])
            )

        db_invite = Invite.from_prisma_invite(prisma_db_invite)

        if db_invite.status == InviteStatus.PENDING and db_invite.deleted_at is None:
            raise UniqueError("Invite already exists")

        db_invite.deleted_at = None
        db_invite.status = InviteStatus.PENDING
        return await self.update_invite(db_invite)

    async def create_multiple_invites(self, invites: List[Invite]) -> List[Invite]:
        """
        Create multiple invites with matching data if not exist.

        Parameters
        ----------
        invites : List[Invite]
            List of invites to create.

        Returns
        -------
        List[Invite]
            List of invites that have been created.

        Raises
        -------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        UniqueError
            Some invites already exist.

        """
        db_invites = await self._db_client.db.invite.find_many(
            where={"id": {"in": [invite.id for invite in invites]}}
        )

        if db_invites is not None and len(db_invites) > 0:
            if any(
                [
                    db_invite.status == InviteStatus.PENDING
                    and db_invite.deleted_at is None
                    for db_invite in db_invites
                ]
            ):
                raise UniqueError("Some invites already exist")

            ids = [db_invite.id for db_invite in db_invites]
            invites = [invite for invite in invites if invite.id not in ids]

            await self._db_client.db.invite.update_many(
                where={"id": {"in": [db_invite.id for db_invite in db_invites]}},
                data={
                    "deleted_at": None,
                    "status": InviteStatus.PENDING,
                },
            )

        await self._db_client.db.invite.create_many(
            data=[invite.to_dict() for invite in invites]
        )
        return invites

    async def update_invite(self, invite: Invite) -> Invite:
        """
        Update invite data.

        Parameters
        ----------
        invite : Invite
            invite object.

        Returns
        -------
        Invite
            Updated invite.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        return await self._db_client.db.invite.update(
            where={"id": invite.id}, data=invite.to_dict()
        )

    async def delete_invite_by_invite_id(self, invite_id: str) -> None:
        """
        Delete the invite with matching invite id.

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
        Delete invites with matching event id

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
        Delete invites with matching author id.

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
        Delete invites with matching invitee id

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
