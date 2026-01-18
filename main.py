variables = []

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

    def execute(self):
        if evaluate(self.condition):
            for child in self.children:
                child.execute()
            

def evaluate(condition):
    if condition["type"] == "single": # f.e MOVE forward 10
        left = condition["left"]
        op = condition["op"]
        right = condition["right"]

        try:
            left_value = variables[left]
        except:
            print("Error")
        
        right_value = int(right)

        if op == "<":
            boolVal = (left_value < right_value)
        elif op == ">":
            boolVal = (left_value > right_value)
        elif op == "==":
            boolVal = (left_value == right_value)
        elif op == "!=":
            boolVal = (left_value != right_value)
        elif op == ">=" or op == "=>":
            boolVal = (left_value >= right_value)
        elif op == "=<" or op == "<=":
            boolVal = (left_value =< right_value)