class config:
  def __init__(self, psend, precieve, pdir, pformat, pqueues):
    self.send = psend #sync
    self.recieve = precieve #sync
    self.dir = pdir #lista de parametros
    self.format = pformat
    self. queues = pqueues