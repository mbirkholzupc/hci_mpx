class lpf():
  def __init__(self, flt_len):
    self.length=flt_len
    self.reset()

  def reset(self):
    self.window=[0]*self.length

  def filter(self, val):
    self.window=[val]+self.window[0:self.length-1]
    return sum(self.window)/self.length

