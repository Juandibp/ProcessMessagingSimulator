class config:
  class __config:
    def __init__(self, psend, precieve, pdir, pformat, pqueues):
      self.send = psend #sync
      self.recieve = precieve #sync
      self.dir = pdir #lista de parametros
      self.format = pformat
      self. queues = pqueues
  instance = None
  def __init__(self, psend, precieve, pdir, pformat, pqueues):
    if not config.instance:
      config. instance = config.__config(psend, precieve, pdir, pformat, pqueues)
    else:
      config.instance.send = psend #sync
      config.instance.recieve = precieve #sync
      config.instance.dir = pdir #lista de parametros
      config.instance.format = pformat
      config.instance. queues = pqueues
  def __getattribute__(self, name):
    return getattr(self.instance, name)