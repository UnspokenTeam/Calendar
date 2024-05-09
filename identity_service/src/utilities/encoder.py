"""Encoder class"""

from bcrypt import checkpw, gensalt, hashpw


class Encoder:
    """
    Encoder class

    Methods
    -------
    encode(password)
        Returns hashed password
    compare(password, hashed_password)
        Returns True if passwords match and False if not

    """

    @staticmethod
    def encode(password: str) -> str:
        """
        Hash password

        Parameters
        ----------
        password
            Unhashed password

        Returns
        -------
        str
            Hashed password

        """
        salt = gensalt()
        return str(hashpw(password=password.encode("UTF-8"), salt=salt).decode("UTF-8"))

    @staticmethod
    def compare(password: str, hashed_password: str) -> bool:
        """
        Compares hashed and unhashed passwords

        Parameters
        ----------
        password
            Unhashed password
        hashed_password
            Hashed password

        Returns
        -------
        bool
            Flag if passwords are matching

        """
        return bool(
            checkpw(
                password=password.encode("UTF-8"),
                hashed_password=hashed_password.encode("UTF-8"),
            )
        )
