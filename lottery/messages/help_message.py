from linebot.models import TextSendMessage


class HelpMessage:
    def get_message(self):
        return TextSendMessage(text="hint 1; hint 2")
