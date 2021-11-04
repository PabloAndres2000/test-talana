from django.core import mail

from adventure.models import Journey


class Notifier:
    def send_notifications(self, journey: Journey) -> None:
        mail.send_mail(
            "Subject here",
            f"Journey start: {journey.start}",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        )
