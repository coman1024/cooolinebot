from config.dbConfig import Database
from config.lineBotConfig import LinbotConfig
from clock import SchdulerJob


def initialize():
  Database.initialize()
  LinbotConfig.initialize()
  SchdulerJob.initialize()

  