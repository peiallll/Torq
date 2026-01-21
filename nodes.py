
# ============================================================================
# GLOBAL VARIABLES
# ============================================================================

variables = {}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def is_number(token):
    """Helper function to check whether tokens are numbers while handling float inputs"""
    try:
        float(token)
        return True
    except ValueError:
        return False


def is_variable(token):
    """Check if token is a variable name (not a keyword or number)"""
    try:
        float(token)
        return False
    except ValueError:
        # Note: keywords check happens at parser level
        return True

# ============================================================================
# NODE CLASSES
# ============================================================================

class Node:
    def __init__(self, node_type, args=None):
        self.type = node_type
        self.args = args or {}
        self.children = []

    def add_children(self, child_node):
        self.children.append(child_node)

    def execute(self):
        pass

class ProgramNode(Node):
    def __init__(self):
        super().__init__("PROGRAM")

    def execute(self):
        for child in self.children:
            child.execute()

class MoveNode(Node):
    def __init__(self, direction, distance):
        super().__init__("MOVE", args={"direction": direction, "distance": distance})

    def execute(self):
        direction = self.args["direction"]
        distance = self.args["distance"]
        print(f"Moving {direction} for {distance}")


class TurnNode(Node):
    def __init__(self, direction, angle):
        super().__init__("TURN", args={"direction": direction, "angle": angle})

    def execute(self):
        direction = self.args["direction"]
        angle = self.args["angle"]


class WaitNode(Node):
    def __init__(self, time):
        super().__init__("WAIT", args={"time": time})

    def execute(self):
        time = self.args["time"]
            
class SetNode(Node):
    def __init__(self, user_variable, value):
        super().__init__("SET", args={"user_variable": user_variable, "value": value})

    def execute(self):
        variable_name = self.args["user_variable"]
        value = self.args["value"]

        if isinstance(value, (int, float)):
            variables[variable_name] = value
        else:
            variables[variable_name] = variables[value]

class UpdateNode(Node):
    def __init__(self, user_variable, value):
        super().__init__("SET", args={"user_variable": user_variable, "value": value})

    def execute(self):
        variable_name = self.args["user_variable"]
        value = self.args["value"]

        if isinstance(value, (int, float)):
            variables[variable_name] = value
        else:
            variables[variable_name] = variables[value]

class IfNode(Node):
    def __init__(self, condition):
        super().__init__("IF")
        self.condition = condition
        self.elifs = []
        self.else_node = None

    def execute(self):
        from main import evaluate
        if evaluate(self.condition) == True:
            for child in self.children:
                child.execute()

class ElseIfNode(Node):
    def __init__(self, condition):
        super().__init__("ELSEIF")
        self.condition = condition
    
    def execute(self):
        from main import evaluate
        if evaluate(self.condition) == True:
            for child in self.children:
                child.execute()

class ElseNode(Node):
    def __init__(self, condition):
        super().__init__("ELSE")
        
    def execute(self):
        for child in self.children:
            child.execute()
        