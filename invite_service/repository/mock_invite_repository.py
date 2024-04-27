"""Mock invite repository"""
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from errors.unique_error import UniqueError
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
        Creates new invite if it does not exist or update the existing one.
    async update_invite(invite)
        Updates invite that has the same id as provided invite object.
    async delete_invite_by_invite_id(invite_id)
        Deletes invite that has matching id.
    async delete_invite_by_event_id(event_id)
        Deletes invites that have matching event id.
    async delete_invite_by_author_id(author_id)
        Deletes invites that have matching author id.
    async delete_invite_by_invitee_id(invitee_id)
        Deletes invites that have matching invitee id.

    """

    _invites: List[Invite]

    def __init__(self) -> None:
        self._invites = []

    async def get_invites_by_event_id(
            self, event_id: str, status: Optional[InviteStatus]
    ) -> List[Invite]:
        """
        Get invites by event id.

        Parameters
        ----------
        event_id : str
            Event id.
        status : Optional[InviteStatus]
            Optional invite status. If present will filter the events by status

        Returns
        -------
        List[Invite]
            Invites with matching event id.

        """
        invites = [invite for invite in self._invites if invite.event_id == event_id and (True if status is None else invite.status == status) and invite.deleted_at is not None]
        return invites

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
            Invite object with matching invite id

        Raises
        ------
        ValueNotFoundError
            Invite was not found

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
            self, author_id: str, page_number: int, items_per_page: int, status: Optional[InviteStatus]
    ) -> List[Invite]:
        """
        Get invites by author id.

        Parameters
        ----------
        author_id : str
            Author's id.
        status : Optional[InviteStatus]
            Optional invite status. If present will filter the events by status
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
        ValueNotFoundError
            No invites were found for given author id.

        """
        invites = [
            invite
            for invite in self._invites
            if invite.author_id == author_id
               and invite.deleted_at is None
               and (invite.status == status if status is not None else True)
        ]
        invites = (
            invites[items_per_page * (page_number - 1): items_per_page * page_number]
            if items_per_page != -1
            else invites
        )
        if invites is None or len(invites) == 0:
            raise ValueNotFoundError("Invites not found")
        return invites

    async def get_all_invites(
            self, page_number: int, items_per_page: int, status: Optional[InviteStatus]
    ) -> List[Invite]:
        """
        Get all invites.

        Parameters
        -------
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
        ValueNotFoundError
            No invites were found for given author id.

        """
        result = [
                     invite
                     for invite in self._invites
                     if status is None or invite.status == status
                 ][
                 items_per_page * (page_number - 1): items_per_page * page_number
                 ]
        if len(result) != 0:
            return result
        raise ValueNotFoundError("Invites not found")

    async def get_invites_by_invitee_id(
            self, invitee_id: str, page_number: int, items_per_page: int, status: Optional[InviteStatus]
    ) -> List[Invite]:
        """
        Get invites by invitee id.

        Parameters
        ----------
        status : Optional[InviteStatus]
            Optional invite status. If present will filter the events by status
        invitee_id : str
            Invitee id.
        page_number : int
            Number of page to get.
        items_per_page : int
            Number of items per page to load.

        Returns
        -------
        List[Invite]
            List of invitee that have matching invite id.

        Raises
        ------
        ValueNotFoundError
            No invites were found for given author id.

        """
        invites = [
            invite
            for invite in self._invites
            if invite.id == invitee_id
               and invite.deleted_at is None
               and (invite.status == status if status is not None else True)
        ]
        invites = (
            invites[items_per_page * (page_number - 1): items_per_page * page_number]
            if items_per_page != -1
            else invites
        )
        if invites is None or len(invites) == 0:
            raise ValueNotFoundError("Invites not found")
        return invites

    async def create_invite(self, invite: Invite) -> None:
        """
        Creates invite with matching data

        Parameters
        ----------
        invite : Invite
            Invite data

        Raises
        ------
        UniqueError
            Invite already exists

        """
        try:
            old_invite_index = next(
                i
                for i in range(len(self._invites))
                if self._invites[i].author_id == invite.author_id and self._invites[i].invitee_id == invite.invitee_id
            )

            if self._invites[old_invite_index].status == InviteStatus.PENDING:
                raise UniqueError("Invite already exists")

            self._invites[old_invite_index] = invite
        except StopIteration:
            invite.id = str(uuid4())
            invite.created_at = datetime.now()
            invite.deleted_at = None
            self._invites.append(invite)

    async def update_invite(self, invite: Invite) -> None:
        """
        Updates invite with matching id

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
        Deletes invite with matching id

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
        Delete invites with matching event id

        Parameters
        ----------
        event_id : str
            Event id

        Raises
        ------
        ValueNotFoundError
            Invites were not found

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
        Delete invites with matching author id

        Parameters
        ----------
        author_id : str
            Author id

        Raises
        ------
        ValueNotFoundError
            Invites were not found

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
        Delete invites with matching invitee id

        Parameters
        ----------
        invitee_id : str
            Invitee id

        Raises
        ------
        ValueNotFoundError
            Invites were not found

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
