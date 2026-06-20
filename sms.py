import os
from twilio.rest import Client
import time

import utils


class SMSSender:
    # in seconds
    TIME_BETWEEN_SENDS = 30

    def __init__(self):
        self.account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.from_address = os.environ.get("TWILIO_NUMBER")
        self.to_address = os.environ.get("MY_NUMBER")
        self.__time_last_sent = time.time() - self.TIME_BETWEEN_SENDS

    def is_timeout_over(self) -> bool:
        if (self.__time_last_sent + self.TIME_BETWEEN_SENDS) < time.time():
            self.__time_last_sent = time.time()
            return True
        else:
            return False

    def is_sending_impossible(self) -> bool:
        if utils.is_regular_operation():
            if self.account_sid is None:
                print("\naccount sid not given\n")
            if self.auth_token is None:
                print("\n authentication token not given\n")
            if self.from_address is None:
                print("\nsending address not given\n")
            if self.to_address is None:
                print("\nreceiving address not given\n")

        return (
            self.account_sid is None
            or self.auth_token is None
            or self.from_address is None
            or self.to_address is None
        )

    def send(self, message: str):
        if self.is_sending_impossible():
            return

        if utils.is_regular_operation():
            return

        assert self.to_address is not None

        if self.is_timeout_over():
            Client(self.account_sid, self.auth_token).messages.create(
                body=message, from_=self.from_address, to=self.to_address
            )
        else:
            print(
                "\n"
                + str(self.TIME_BETWEEN_SENDS)
                + " seconds have not passed since the last send"
            )


if __name__ == "__main__":
    # costs couple cents
    sender = SMSSender()
    sender.send("message from me to me")
    time.sleep(5)
    sender.send("message won't be send")
