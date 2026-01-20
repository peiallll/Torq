import operator as o
from parser import run_program
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
# EVALUATION FUNCTIONS
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
            right_value = int(right_value)

        boolVal = ops[op](left_value, right_value) # if x (15) > 10: True
        if boolVal == True:
            return True
        elif boolVal == False:
            return False
        
    