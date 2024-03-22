"""User Model"""
from dataclasses import dataclass
from generated.get_user_pb2 import User as GrpcUser


@dataclass
class User:
    """
    Data class that stores user information

    Attributes
    ----------
    id : str
        ID of the user
    username : str
        User's name
    email : str
        Email of the user
    _password : str
        Hashed password of the user


    Methods
    -------
    to_grpc_user()
        Returns user's information as a GrpcUser class instance

    """

    id: str
    username: str
    email: str
    _password: str

    def to_grpc_user(self) -> GrpcUser:
        """
        Converts user information to GrpcUser

        Returns
        -------
        User data in GrpcUser instance
        """
        return GrpcUser(
            id=self.id,
            username=self.username,
            email=self.email,
        )
