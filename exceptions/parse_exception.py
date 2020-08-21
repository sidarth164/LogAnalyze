class ParseError(Exception):
  """
  A custom exception class that is thrown when there is a parsing error
  """
  def __init__(self, message):
    self.message = message
