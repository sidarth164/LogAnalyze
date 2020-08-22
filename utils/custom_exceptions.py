class ParseError(Exception):
  """
  A custom exception class that is thrown when there is a parsing error
  """
  def __init__(self, message):
    self.message = message


class StatusError(Exception):
  """
  A custom exception class that is thrown when the log contains an un-identifiable http status code
  """
  def __init__(self, message):
    self.message = message
