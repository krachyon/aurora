import aurora
import notify2
import time

notify2.init("kde")
while True:

    probab = aurora.getProbabilityAt(aurora.getData(), 65, 26)
    if probab > 0:
        n = notify2.Notification("Aurora!",
                                 f"Probability: {probab}",
                                 "notification-message-im")
        n.show()
    time.sleep(120)
