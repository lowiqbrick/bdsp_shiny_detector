import os
from twilio.rest import Client
import time


class SMSSender:
    # in seconds
    TIME_BETWEEN_SENDS = 30

    def __init__(self):
        self.account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.from_address = os.environ.get("TWILIO_NUMBER")
        self.to_address = os.environ.get("MY_NUMBER")
        self.client = Client(self.account_sid, self.auth_token)
        self.__time_last_sent = time.time() - self.TIME_BETWEEN_SENDS

    def is_timeout_over(self) -> bool:
        if (self.__time_last_sent + self.TIME_BETWEEN_SENDS) < time.time():
            self.__time_last_sent = time.time()
            return True
        else:
            return False

    def send(self, message: str):
        if self.to_address is None and "PYTEST_CURRENT_TEST" not in os.environ:
            print("\nno address given\n")

        assert self.to_address is not None

        if self.is_timeout_over():
            self.client.messages.create(
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
