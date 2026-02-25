from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from app.validators.authentication_validator import AuthValidator
    from app.validators.index_validator import IndexValidator
    from app.dao.user_dao import UserDAO
    from app.services.authentication_service import AuthenticationService
    from app.services.index_service import IndexService

class AbstractDAOFactory(ABC):
    """Abstract DAO factory interface."""

    @staticmethod
    @abstractmethod
    def get_user_dao() -> Any:
        """Return a `UserDAO` instance."""


class AbstractServiceFactory(ABC):
    """Abstract Service factory interface."""

    @staticmethod
    @abstractmethod
    def get_index_service() -> Any:
        """Return an `IndexService` instance."""

    @staticmethod
    @abstractmethod
    def get_authentication_service() -> Any:
        """Return an `AuthenticationService` instance."""


class AbstractValidatorFactory(ABC):
    """Abstract Validator factory interface."""

    @staticmethod
    @abstractmethod
    def get_index_validator() -> Any:
        """Return an `IndexValidator` instance."""

    @staticmethod
    @abstractmethod
    def get_auth_validator() -> Any:
        """Return an `AuthValidator` instance."""


class DefaultFactory(AbstractDAOFactory, AbstractServiceFactory, AbstractValidatorFactory):
    """Default concrete factory that delegates to existing `factory.py` helpers.

    This class provides the concrete implementations by calling the
    static helpers defined in `app.pattern.factory` so existing code can
    depend on the abstract interfaces in this module.
    """

    # Accessor builders -------------------------------------------------

    class _ServiceAccessor:
        def index(self) -> IndexService:
            from app.pattern import factory as concrete_factory
            return concrete_factory.ServiceFactory.get_index_service()

        def authentication(self) -> AuthenticationService:
            from app.pattern import factory as concrete_factory
            return concrete_factory.ServiceFactory.get_authentication_service()

    class _ValidatorAccessor:
        def index(self) -> IndexValidator:
            from app.pattern import factory as concrete_factory
            return concrete_factory.ValidatorFactory.get_index_validator()

        def authentication(self) -> AuthValidator:
            from app.pattern import factory as concrete_factory
            return concrete_factory.ValidatorFactory.get_auth_validator()

    class _DAOAccessor:
        def user(self) -> UserDAO:
            from app.pattern import factory as concrete_factory
            return concrete_factory.DAOFactory.get_user_dao()

    @staticmethod
    def get_service() -> "DefaultFactory._ServiceAccessor":
        """Return a service accessor with builder-like methods.

        Example: DefaultFactory.get_service().index()
        """
        return DefaultFactory._ServiceAccessor()

    @staticmethod
    def get_validator() -> "DefaultFactory._ValidatorAccessor":
        """Return a validator accessor with builder-like methods.

        Example: DefaultFactory.get_validator().index()
        """
        return DefaultFactory._ValidatorAccessor()

    @staticmethod
    def get_dao() -> "DefaultFactory._DAOAccessor":
        """Return a dao accessor with builder-like methods.

        Example: DefaultFactory.get_dao().user()
        """
        return DefaultFactory._DAOAccessor()

    # Backwards-compatible wrappers ------------------------------------
    @staticmethod
    def get_user_dao() -> Any:
        return DefaultFactory.get_dao().user()

    @staticmethod
    def get_index_service() -> Any:
        return DefaultFactory.get_service().index()

    @staticmethod
    def get_authentication_service() -> Any:
        return DefaultFactory.get_service().authentication()

    @staticmethod
    def get_index_validator() -> Any:
        return DefaultFactory.get_validator().index()

    @staticmethod
    def get_auth_validator() -> Any:
        return DefaultFactory.get_validator().authentication()


def get_default_factory() -> DefaultFactory:
    """Helper to obtain the default concrete factory instance."""
    return DefaultFactory()


__all__ = [
    "AbstractDAOFactory",
    "AbstractServiceFactory",
    "AbstractValidatorFactory",
    "DefaultFactory",
    "get_default_factory",
]
