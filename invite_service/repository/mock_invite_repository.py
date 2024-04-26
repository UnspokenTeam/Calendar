"""Mock invite repository"""
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from errors.value_not_found_error import ValueNotFoundError
from src.models.invite import Invite, InviteStatus
from utils.singleton import singleton

from repository.invite_repository_interface import InviteRepositoryInterface


@singleton
class MockInviteRepositoryImpl(InviteRepositoryInterface):
    """
    Mock class for manipulating with invites data

    Attributes
    ----------
    _invites: List[Invite]
        List of invites

    Methods
    -------
    async get_invite_by_invite_id(invite_id)
        Returns invite that has matching invite_id
    async get_invites_by_author_id(author_id, status)
        Returns invites that has matches with given author id.
    async get_all_invites(status)
        Returns all invites.
    async get_invites_by_invitee_id(invitee_id, status)
        Returns invites that has matches with given of invitee id.
    async create_invite(invite)
        Creates new invite inside db.
    async update_invite(invite)
        Updates invite that has the same id as provided invite object inside db.
    async delete_invite(invite_id)
        Deletes invite that has matching id from database.

    """

    _invites: List[Invite]

    def __init__(self) -> None:
        self._invites = []

    async def get_invite_by_invite_id(self, invite_id: str) -> Invite:
        """
        Get invite by invite id.

        Parameters
        ----------
        invite_id : str
            Invite's id

        Returns
        -------
        Invite
            Invite object

        Raises
        ------
        ValueNotFoundError
            Invite not found

        """
        try:
            return next(
                invite
                for invite in self._invites
                if invite.id == invite_id and invite.deleted_at is None
            )
        except StopIteration:
            raise ValueNotFoundError("Invite does not exist")

    async def get_invites_by_author_id(
        self, author_id: str, status: Optional[InviteStatus]
    ) -> List[Invite]:
        """
        Get invites by author id.

        Parameters
        ----------
        author_id : str
            Author's id.
        status : Optional[InviteStatus]
            Optional invite status. If present will filter the events by status

        Returns
        -------
        List[Invite]
            List of invites that matches by author id.

        Raises
        ------
        ValueNotFoundError
            No invites was found for given author id.

        """
        invites = [
            invite
            for invite in self._invites
            if invite.author_id == author_id
            and invite.deleted_at is None
            and (invite.status == status if status is not None else True)
        ]
        if invites is None or len(invites) == 0:
            raise ValueNotFoundError("Invites not found")
        return invites

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
            List of invites that matches by invite id.

        Raises
        ------
        ValueNotFoundError
            No invites was found for given author id.

        """
        result = [
            invite
            for invite in self._invites
            if status is None or invite.status == status
        ]
        if len(result) != 0:
            return result
        raise ValueNotFoundError("Invites not found")

    async def get_invites_by_invitee_id(
        self, invitee_id: str, status: Optional[InviteStatus]
    ) -> List[Invite]:
        """
        Get invites by invitee id.

        Parameters
        ----------
        status : Optional[InviteStatus]
            Optional invite status. If present will filter the events by status
        invitee_id : str
            Invitee id.

        Returns
        -------
        List[Invite]
            List of invitee that matches by invite id.

        Raises
        ------
        ValueNotFoundError
            No invites was found for given author id.

        """
        invites = [
            invite
            for invite in self._invites
            if invite.id == invitee_id
            and invite.deleted_at is None
            and (invite.status == status if status is not None else True)
        ]
        if invites is None or len(invites) == 0:
            raise ValueNotFoundError("Invites not found")
        return invites

    async def create_invite(self, invite: Invite) -> None:
        """
        Creates invite with matching data or throws an exception

        Parameters
        ----------
        invite : Invite
            Invite data

        """
        invite.id = str(uuid4())
        invite.created_at = datetime.now()
        self._invites.append(invite)

    async def update_invite(self, invite: Invite) -> None:
        """
        Updates invite with matching id or throws an exception

        Parameters
        ----------
        invite : Invite
            Invite data

        Raises
        ------
        ValueNotFoundError
            Can't update invite with provided data

        """
        try:
            index = next(
                i
                for i in range(len(self._invites))
                if self._invites[i].id == invite.id and invite.deleted_at is None
            )
            self._invites[index] = invite
        except StopIteration:
            raise ValueNotFoundError("Invite not found")

    async def delete_invite_by_invite_id(self, invite_id: str) -> None:
        """
        Deletes invite with matching id or throws an exception

        Parameters
        ----------
        invite_id : str
            Invite's id

        Raises
        ------
        ValueNotFoundError
            Can't delete invite with provided data

        """
        try:
            index = next(
                i
                for i in range(len(self._invites))
                if self._invites[i].id == invite_id
                and self._invites[i].deleted_at is None
            )
        except StopIteration:
            raise ValueNotFoundError("Invite not found")
        self._invites[index].deleted_at = datetime.now

    async def delete_invites_by_event_id(self, event_id: str) -> None:
        """
        Delete invites by event id

        Parameters
        ----------
        event_id : str
            Event id

        Raises
        ------
        ValueNotFoundError
            No invites not found

        """
        indexes = [
            i
            for i in range(len(self._invites))
            if self._invites[i].deleted_at is None
            and self._invites[i].event_id == event_id
        ]

        if len(indexes) == 0:
            raise ValueNotFoundError("No invites found")

        now = datetime.now()

        for index in indexes:
            self._invites[index].deleted_at = now

    async def delete_invites_by_author_id(self, author_id: str) -> None:
        """
        Delete invites by author id

        Parameters
        ----------
        author_id : str
            Author id

        Raises
        ------
        ValueNotFoundError
            No invites not found

        """
        indexes = [
            i
            for i in range(len(self._invites))
            if self._invites[i].deleted_at is None
            and self._invites[i].author_id == author_id
        ]

        if len(indexes) == 0:
            raise ValueNotFoundError("No invites found")

        now = datetime.now()

        for index in indexes:
            self._invites[index].deleted_at = now

    async def delete_invites_by_invitee_id(self, invitee_id: str) -> None:
        """
        Delete invites by invitee id

        Parameters
        ----------
        invitee_id : str
            Invitee id

        Raises
        ------
        ValueNotFoundError
            No invites not found

        """
        indexes = [
            i
            for i in range(len(self._invites))
            if self._invites[i].deleted_at is None
            and self._invites[i].invitee_id == invitee_id
        ]

        if len(indexes) == 0:
            raise ValueNotFoundError("No invites found")

        now = datetime.now()

        for index in indexes:
            self._invites[index].deleted_at = now
