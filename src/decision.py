
# ================================================
# Base class for all decision decisions
class Decision():
    def __init__(self, decision):
        self.decision = decision

    def toJson(self):
        return { 'decision': self.decision, }

# ================================================
class MessageableDecision(Decision):
    def __init__(self, decision, message = None):
        super().__init__(decision)
        self.message = message

    def toJson(self):
        return {
            **super().toJson(),
            **({ 'message': self.message, } if self.message else {})
        }

# ================================================
class WinnerDecision(MessageableDecision):
    def __init__(self, name, message = None):
        super().__init__("winner", message)
        self.name = name

    def toJson(self):
        return { **super().toJson(), 'name': self.name, }

# ================================================
class PrDecision(MessageableDecision):
    def __init__(self, id, decision, message = None):
        super().__init__(decision, message)
        self.id = id

    def toJson(self):
        return { **super().toJson(), 'id': self.id, }

# ================================================
class AcceptDecision(PrDecision):
    def __init__(self, id, message = None):
        super().__init__(id, "accept", message)

# ================================================
class RejectDecision(PrDecision):
    def __init__(self, id, message = None):
        super().__init__(id, "reject", message)

# ================================================
class DeferDecision(Decision):
  def __init__(self):
      super().__init__("defer")
