from config.dbConfig import Database
from config.lineBotConfig import LinbotConfig


def initialize():
  Database.initialize()
  LinbotConfig.initialize()