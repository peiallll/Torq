import operator as o
from parser import Interpreter
from nodes import variables, is_variable

# ============================================================================
# GLOBAL VARIABLES & OPERATORS
# ============================================================================

ops = {
    ">": o.gt,
    "<": o.lt,
    "==": o.eq,
    "=/=": o.ne,
    ">/=": o.ge,
    "</=": o.le
}

# ============================================================================
# EVALUATE FUNCTION
# ============================================================================

def evaluate(condition):
    """Evaluate a condition (single or logical) and return boolean result"""
    if condition["type"] == "single": # f.e MOVE forward 10
        left = condition["left"]
        op = condition["op"]
        right = condition["right"]

        try:
            left_value = variables[left]
        except:
            print("Error")
            return 
        
        right_value = right
            
        if is_variable(right_value):
            if right_value in variables:
                right_value = variables[right_value]
            else:
                print(f"Error. {right_value} not in defined variables list. Define it using the SET command first.")
        else:
            right_value = float(right_value)

        bool_val = ops[op](left_value, right_value) # if x (15) > 10: True
        if bool_val == True:
            return True
        elif bool_val == False:
            return False
        
    elif condition["type"] == "logical":
        left = condition["left"]
        op = condition["op"]
        right = condition["right"]

        bool_left = evaluate(left)
        bool_right = evaluate(right)

        if op == "and":
            if bool_left == True and bool_right == True:
                return True
        elif op == "or":
            if bool_left == True or bool_right == True:
                return True
            
        return False
# ============================================================================
# RUN IT
# ============================================================================

if __name__ == "__main__":
    print("type 'help' for a list of commands.")
    interpreter = Interpreter()
    interpreter.run()