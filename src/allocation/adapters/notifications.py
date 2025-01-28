# pylint: disable=too-few-public-methods
import abc
import smtplib
from allocation import config


class AbstractNotifications(abc.ABC):
    @abc.abstractmethod
    def send(self, destination, message):
        """
        Send a notification message to the specified destination.

        This method is part of the Unit of Work pattern, as it ensures
        that notifications are sent as part of the unit of work's
        commit process. This helps maintain consistency and ensures
        that notifications are only sent if the unit of work is
        successfully committed.
        """
        raise NotImplementedError


DEFAULT_HOST = config.get_email_host_and_port()["host"]
DEFAULT_PORT = config.get_email_host_and_port()["port"]


class EmailNotifications(AbstractNotifications):
    def __init__(self, smtp_host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.server = smtplib.SMTP(smtp_host, port=port)
        self.server.noop()

    def send(self, destination, message):
        """
        Send an email notification to the specified destination.

        This method is part of the Unit of Work pattern, as it ensures
        that notifications are sent as part of the unit of work's
        commit process. This helps maintain consistency and ensures
        that notifications are only sent if the unit of work is
        successfully committed.
        """
        msg = f"Subject: allocation service notification\n{message}"
        self.server.sendmail(
            from_addr="allocations@example.com",
            to_addrs=[destination],
            msg=msg,
        )
