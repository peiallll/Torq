from main import MoveNode, TurnNode, WaitNode, IfNode, SetNode, UpdateNode
from main import variables

# ============================================================================
# GLOBAL VARIABLES & MAIN DICTIONARIES
# ============================================================================

user_lines = {}
program_nodes = []

statement_nodes = {
    "if": {
        "expressions": ["==", "!=", "+", "-", "*", "**", ">", "<", ">=", "=>", "=<", "<="],
        "logic_statements": ["and", "or"],
        "expects_variable": True,
        "expected_variables": 2,
        "expected_s_number_args": 0,
        "expected_expressions": 1
    }
}

command_nodes = { #dictionary to store valid commnds and subcommands (MOVE forward 10 would be valid here)
    "MOVE": {
        "subcommands": ["forward", "backward", "forwards", "backwards"],
        "optional_subcommands": [],
        "expected_number_args": 1,
        "expected_subcommands": 1,
        "expected_optional_subcommands": 0
    },
    "TURN": {
        "subcommands": ["left", "right", "clockwise", "anticlockwise", "anti-clockwise", "counterclockwise", "counter-clockwise"],
        "optional_subcommands": [],
        "expected_number_args": 1,
        "expected_subcommands": 1,
        "expected_optional_subcommands": 0
    },
    "WAIT": {
        "subcommands": [],
        "expected_number_args": 1,
        "expected_subcommands": 0,
        "optional_subcommands": [],
        "expected_optional_subcommands": 0
    },
}

special_command_nodes = {
    "SET",
    "UPDATE"
}
current_indent = 0
previous_indent = 0


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def is_number(token): ## helper function to check whether tokens are number while handling loat inputs
    try:
        float(token)
        return True
    except ValueError:
        return False

def is_variable(token):
    try:
        float(token)
        return False
    except ValueError:
        if token in command_nodes or token in statement_nodes:
            return False

        for node_dict in (statement_nodes, command_nodes):
            for key, value in node_dict.items():
                if isinstance(value, dict):
                    if token in value:
                        return False
    
    return True
            
def check_list_lengths(expected_args, current_args):
    if len(current_args) != expected_args:
        return False
    else:
        return True


def check_which_node_type(command): # helper function to determine node type (command, statement, or other (placeholder))
    if command.isupper() and command in command_nodes:
        return "command"
    elif command.isupper() and command in special_command_nodes:
        return "special_command"
    elif command.islower() and command in statement_nodes:
        return "statement"
    else:
        return "neither"


def checkForIndentation(current_indent, previous_indent):
    if current_indent > previous_indent:
        return "down_one_level"
    elif current_indent == previous_indent:
        return "same_block"
    elif current_indent < previous_indent:
        return "up_one_level"

def validate_commands(current_subcommands, current_valid_subcommands, expected_subcommands, current_number_args, expected_number_args, current_optional_args, current_valid_optional_args, expected_optional_args, command):
    if type_of_logic == "command":

        for token in tokenized[1:]: # loop through non-command (0 index) tokens.categorise and sort them into lists
            if token in current_valid_subcommands:
                current_subcommands.append(token)
            elif is_number(token):
                current_number_args.append(float(token))
            elif token in current_valid_optional_args:
                current_optional_args.append(token)
            else:
                print("Error: couldnt find at least one of those arguments.")
                return False
                
        print(current_subcommands); print(current_number_args); print(current_optional_args)
        ## to line 116: check whether user has inputted correct amount of subcommands, number arguments, and optional subcommands. f.e MOVE requires there to be NO optional subcommands ('MOVE forward 10')
        expected_number_args = command_nodes[command]["expected_number_args"]; expected_subcommands = command_nodes[command]["expected_subcommands"]; expected_optional_args = command_nodes[command]["expected_optional_subcommands"]
                
        current_lists = [current_subcommands, current_number_args, current_optional_args]
        expected_lists = [expected_number_args, expected_subcommands, expected_optional_args]

        for index in range(len(current_lists)):
            if check_list_lengths(expected_lists[index], current_lists[index]) != True: 
                print("Error: invalid amount of subcommands/args/numbers")
                return False
            
        return True
    
    else:
        print("thats not a command")
        return    

# ============================================================================
# COMMAND PARSING
# ============================================================================

def handle_commands(tokenized, command): ##  main function for if user inputs and COMMAND (e.g MOVE)
    
    current_subcommands = []
    current_number_args = []
    current_optional_args = []

    current_valid_subcommands = command_nodes[command]["subcommands"]
    expected_subcommands = command_nodes[command]["expected_subcommands"]

    expected_number_args = command_nodes[command]["expected_number_args"]

    current_valid_optional_args = command_nodes[command]["optional_subcommands"]
    expected_optional_args = command_nodes[command]["expected_optional_subcommands"]

    if command not in command_nodes:
        print("Error: invalid command")
        return
            
    validated = validate_commands(current_subcommands, current_valid_subcommands, expected_subcommands, current_number_args, expected_number_args, current_optional_args, current_valid_optional_args, expected_optional_args, command)
    
    if validated == False:
        print("ERROR")
        return
    
    if command == "MOVE":
        node = MoveNode(current_subcommands[0], current_number_args[0])
    elif command == "TURN":
        node = TurnNode(current_subcommands[0], current_number_args[0])
    elif command == "WAIT":
        node = WaitNode(current_number_args[0])
    elif command == "SET":
        node = SetNode()
    
    return node

# ============================================================================
# SPECIAL COMMAND PARSING
# ============================================================================

def handle_special_command(tokenized, command): # special commands: SET / UPDATE
    
    if "as" not in tokenized:
        print("Error, SET or UPDATE commands must have 'as' (e.g SET distance as 5")
        return
    
    as_index = tokenized.index("as")
    left = tokenized[1:as_index]
    right = tokenized[as_index + 1:] 
    ## SET x as 5 ; UPDATE x as 5
    if len(left) != 1 or is_variable(left[0]) == False:
        print("Error. left args count must equal to 1, and must be a new variable name.")
        return
    
    if len(right) != 1:
        print("Error. right args count must equal to 1. ")
        return
    
    if command == "SET":
        if is_variable(right[0]):
            if right[0] not in variables:
                print(f"Error. {right[0]} is not an existing variable. Define that using SET first.")
                return
        
        node = SetNode(left[0], right[0])
        
    elif command == "UPDATE":
        if left[0] not in variables:
            print(f"Error. Variable {left[0]} does not exist and so cannot be updated. Use SET to define a new variable.")
            return

        if is_variable(right[0]) == True and right[0] not in variables:
            print(f"Error. {right[0]} is not an existing variable. Define that using SET first.")
            return
    
        node = UpdateNode(left[0], right[0])
    

# ============================================================================
# STATEMENT/CONDITION PARSING
# ============================================================================

def token_sorter(tokenized, first_word):
    tokens_sorted = {}

    s_current_number_args = []
    current_variables = []
    current_expressions = []
    current_logic_statements = []

    for token in tokenized:
        if token in statement_nodes[first_word]["expressions"]:
            current_expressions.append(token)

        elif token in statement_nodes[first_word]["logic_statements"]:
            current_logic_statements.append(token)

        try:
            float(token)
            s_current_number_args.append(token)
        except ValueError:
            current_variables.append(token)
            
        else:
            print("ERROR")
            return

    tokens_sorted.update({
        "numbers": s_current_number_args,
        "expressions": current_expressions,
        "logic_statements": current_logic_statements,
        "variables": current_variables
    })

    return tokens_sorted


def condition_builder(tokens_sorted, tokenized, first_word):
    condition = ""

    node_dict = {}

    if len(tokens_sorted["logic_statements"]) > 0:
        condition = "logical"
    else:
        condition = "single"

    if condition == "single":
        node_dict.update({
            "type": "single",
            "left": tokens_sorted["variables"][0],
            "op": tokens_sorted["expressions"][0],
            "right": tokens_sorted["numbers"][0]
        })

    elif condition == "logical":
        logical_op = tokens_sorted["logic_statements"][0]
        op_index = tokenized.index(logical_op)

        left_tokens = tokenized[:op_index]
        right_tokens = tokenized[op_index + 1:]

        left_tokens_sorted = token_sorter(left_tokens, first_word)
        right_tokens_sorted = token_sorter(right_tokens, first_word)

        node_dict.update({
            "type": "logical",
            "op": logical_op,
            "left": condition_builder(left_tokens_sorted, left_tokens, first_word), ## dict = {"type", "logical", "op": and, "left": {x > 5}, "right": {x < 10}}
            "right": condition_builder(right_tokens_sorted, right_tokens, first_word)#                                               ^^^^^              ^^^^^^^ run token builder on these again to get type, op, left, right. 
        })
        
    return node_dict


def create_statement_node(tokenized, first_word, user_input):
    tokens_sorted = token_sorter(tokenized[1:], first_word)

    condition = condition_builder(tokens_sorted, tokenized[1:], first_word)
    
    if first_word == "if":
        node = IfNode(condition)
    
    return node


# ============================================================================
# MAIN PROGRAM LOOP
# ============================================================================

while True:
    user_input = input("> ")
    
    tokenized = user_input.split()

    if user_input.strip() == "": #ignore blank lines
        continue
    else:
        previous_indent = current_indent ## first pass: prev_indent = 0
        current_indent = 0

        for char in user_input:
            if char == " ":
                current_indent += 1
            elif char != " ":
                break
        
        if previous_indent % 4 != 0 or current_indent % 4 != 0:
            print(f"Error: indentation has to be 4,8,12,16,20 spaces etc, not {current_indent}")

        line_state = checkForIndentation(current_indent, previous_indent)

        line_length = len(tokenized)
        first_word = tokenized[0]
        command = first_word

        type_of_logic = check_which_node_type(first_word)

        if type_of_logic == "command":
            if current_indent == 0:
                program_nodes.append(create_statement_node(tokenized, first_word, user_input))
            
            if command in command_nodes:
                handle_commands(tokenized, first_word)
            
        elif type_of_logic == "statement":
            create_statement_node(tokenized, first_word, user_input)
            #TO-DO: statemenet parser + tokenizer
        elif type_of_logic == "special_command":
            handle_special_command(tokenized, first_word)

        elif type_of_logic == "neither":
            print("Error: invalid input")
            continue