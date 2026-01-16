class Node:
    def __init__(self, node_type, args=None):
        self.type = node_type
        self.args = args or {}
        self.children = []

    def add_children(self, child_node):
        self.children.append(child_node)

    def execute(self):
        pass


class MoveNode(Node):
    def __init__(self, direction, distance):
        super().__init__("MOVE", args={"direction": direction, "distance": distance})

    def execute(self):
        direction = self.args["direction"]
        distance = self.args["distance"]
        print(f"Moving {direction} for {distance}")


class TurnNode(Node):
    def __init__(self, speed, angle, direction):
        super().__init__("TURN", args={"direction": direction, "angle": angle})

    def execute(self):
        direction = self.args["direction"]
        angle = self.args["angle"]


class WaitNode(Node):
    def __init__(self, time):
        super().__init__("WAIT", args={"time": time})

    def execute(self):
        time = self.args["time"]
            

class IfNode(Node):
    def __init__(self, condition):
        super().__init__("IF")
        self.condition = condition

    def execute(self):
        if evaluate(self.condition):
            for child in self.children:
                child.execute()
            

def evaluate(condition):
    pass