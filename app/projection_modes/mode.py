from abc import ABC, abstractmethod


class Mode(ABC):
    """
    An abstract base class for defining projection modes

    Subclasses of Mode must implement the abstract`trigger method,
    which specifies the behavior that is triggered when the mode is activated.

    Modes inherit from Mode and are instantiated in the modes_factory 

    Attributes:
        None

    Methods:
        trigger: Abstract method that must be implemented by subclasses.
            Defines the behavior that is triggered when the mode is activated.
    """
    
    @abstractmethod
    def trigger(self):
        """
        Trigger the behavior of the mode.

        This method must be implemented by all mode subclasses.

        Args:
            None

        Returns:
            None
        """
        pass

