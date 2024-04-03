"""Mock invite repository"""
from typing import List
from uuid import uuid4

from errors.value_not_found_error import ValueNotFoundError
from src.models.invite import Invite

from repository.invite_repository_interface import InviteRepositoryInterface


class MockInviteRepositoryImpl(InviteRepositoryInterface):
    """
    Mock class for manipulating with invites data

    Attributes
    ----------
    _invites: List[Invite]
        List of invites

    Methods
    -------
    async get_invites(author_id)
        Returns invites that has matches with given author id.
    async get_all_invites()
        Returns all invites.
    async get_invites_by_invitee_id(invitee_id)
        Returns invites that has matches with given list of invitee id.
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
        ValueNotFoundError
            No invites was found for given author id.

        """
        invites = [
            invite
            for invite in self._invites
            if invite.author_id == author_id and invite.deleted_at is None
        ]
        if invites is None or len(invites) == 0:
            raise ValueNotFoundError("Invites not found")
        return invites

    async def get_all_invites(self) -> List[Invite]:
        """
        Get all invites.

        Returns
        -------
        List[Invite]
            List of invites that matches by invite id.

        Raises
        ------
        ValueNotFoundError
            No invites was found for given author id.

        """
        if len(self._invites) != 0:
            return self._invites
        raise ValueNotFoundError("Invites not found")

    async def get_invites_by_invitee_id(self, invitee_id: List[str]) -> List[Invite]:
        """
        Get invites by invitee id.

        Parameters
        ----------
        invitee_id : List[str]
            List of invitee id.

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
            if invite.id in invitee_id and invite.deleted_at is None
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
        index = next(
            i for i in range(len(self._invites)) if self._invites[i].id == invite.id
        )
        if self._invites[index].author_id == invite.author_id:
            self._invites[index] = invite
        else:
            raise ValueNotFoundError("Invites authors must be same")

    async def delete_invite(self, invite_id: str) -> None:
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
        index = next(
            i for i in range(len(self._invites)) if self._invites[i].id == invite_id
        )
        self._invites.pop(index)
