def formatNumberList(numbers):
  try:
    return f'{numbers[0]}, {numbers[1]}, {numbers[2]}, {numbers[3]}, {numbers[4]}, {numbers[5]}'
  except Exception as e:
    return str(e)


def toIntList(strList):
  return [int(i) for i in strList]