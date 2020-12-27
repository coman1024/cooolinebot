from ..messages.help_message import HelpMessage


class HelpReply:
    def get_reply_message(self, type):
        if type == 'All':
            return HelpMessage().get_message()
