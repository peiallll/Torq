from nodes import Node, ProgramNode, MoveNode, TurnNode, WaitNode, IfNode, ElseNode, ElseIfNode, SetNode, UpdateNode
from nodes import variables, is_number, is_variable

# ============================================================================
# GLOBAL VARIABLES & MAIN DICTIONARIES
# ============================================================================

user_lines = {}
program_node = ProgramNode()
stack = [program_node]
current_indent = 0
previous_indent = 0

statement_nodes = {
    "if": {
        "expressions": ["==", "=/=", ">", "<", ">/=", "</="],
        "logic_statements": ["and", "or"],
        "expects_variable": True,
        "expected_variables": 2,
        "expected_s_number_args": 0,
        "expected_expressions": 1
    },

    "elseif": {
        "expressions": ["==", "=/=", ">", "<", ">/=", "</="],
        "logic_statements": ["and", "or"],
        "expects_variable": True,
        "expected_variables": 2,
        "expected_s_number_args": 0,
        "expected_expressions": 1
    },

    "else": {
        "expressions": None,
        "logic_statements": None,
        "expects_variable": False,
        "expected_s_number_args": 0,
        "expected_expressions": 0
    }
}

command_nodes = {
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

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def check_list_lengths(expected_args, current_args):
    if len(current_args) != expected_args:
        return False
    else:
        return True


def check_which_node_type(command):
    """Determine node type (command, statement, special_command, or neither)"""
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
        return "indent"
    elif current_indent == previous_indent:
        return "same_block"
    elif current_indent < previous_indent:
        return "dedent"

def validate_commands(current_subcommands, current_valid_subcommands, expected_subcommands, current_number_args, expected_number_args, current_optional_args, current_valid_optional_args, expected_optional_args, command, tokenized, type_of_logic):
    if type_of_logic == "command":

        for token in tokenized[1:]:
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
        
        expected_number_args = command_nodes[command]["expected_number_args"]
        expected_subcommands = command_nodes[command]["expected_subcommands"]
        expected_optional_args = command_nodes[command]["expected_optional_subcommands"]
                
        current_lists = [current_subcommands, current_number_args, current_optional_args]
        expected_lists = [expected_subcommands, expected_number_args, expected_optional_args]

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

def handle_commands(tokenized, command):
    """Main function for handling COMMAND inputs (e.g MOVE)"""
    
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
            
    validated = validate_commands(current_subcommands, current_valid_subcommands, expected_subcommands, current_number_args, expected_number_args, current_optional_args, current_valid_optional_args, expected_optional_args, command, tokenized, type_of_logic)
    
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

def handle_special_command(tokenized, command):
    """Handle special commands: SET / UPDATE"""
    
    if "as" not in tokenized:
        print("Error, SET or UPDATE commands must have 'as' (e.g SET distance as 5")
        return
    
    as_index = tokenized.index("as")
    left = tokenized[1:as_index]
    right = tokenized[as_index + 1:] 
    
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
    
    return node

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

    for logic_statement in current_logic_statements:
        if logic_statement not in statement_nodes["if"]["expressions"]:
            print("Error. Expression not found.")
            return

    tokens_sorted.update({
        "numbers": s_current_number_args,
        "expressions": current_expressions,
        "logic_statements": current_logic_statements,
        "variables": current_variables
    })

    return tokens_sorted


def condition_builder(tokens_sorted, tokenized, first_word):
    """Returns a condition dict to be used in evaluate()"""
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
            "left": condition_builder(left_tokens_sorted, left_tokens, first_word),
            "right": condition_builder(right_tokens_sorted, right_tokens, first_word)
        })
        
    return node_dict


def create_statement_node(tokenized, first_word, user_input):

    try:
        then_index = tokenized.index("THEN")
    except ValueError:
        print("Error. missing THEN")
        return

    condition_tokens = tokenized[1:then_index]

# 3. Parse condition normally
    tokens_sorted = token_sorter(condition_tokens, first_word)
    condition = condition_builder(tokens_sorted, condition_tokens, first_word)

    if first_word == "if":
        node = IfNode(condition)
    
    return node


# ============================================================================
# MAIN PROGRAM LOOP
# ============================================================================

def run_program():
    while True:
        user_input = input("> ")
        
        tokenized = user_input.split()

        if user_input.strip() == "":
            continue
        else:
            previous_indent = current_indent
            current_indent = 0

            for char in user_input:
                if char == " ":
                    current_indent += 1
                elif char != " ":
                    break
            
            if previous_indent % 4 != 0 or current_indent % 4 != 0:
                print(f"Error: indentation has to be 0,4,8,12,16,20 spaces etc, not {current_indent}")

            line_length = len(tokenized)
            first_word = tokenized[0]
            command = first_word

            type_of_logic = check_which_node_type(first_word)

            node = None

            if type_of_logic == "command":
                node = handle_commands(tokenized, first_word)
                
            elif type_of_logic == "statement":
                node = create_statement_node(tokenized, first_word, user_input)
                
            elif type_of_logic == "special_command":
                node = handle_special_command(tokenized, first_word)

            elif type_of_logic == "neither":
                print("Error: invalid input")
                continue

            indentation_type = checkForIndentation(current_indent, previous_indent)
            if indentation_type == "dedent":
                indent_levels_up = (previous_indent - current_indent) // 4

                for _ in range(indent_levels_up):
                    stack.pop()
            
            if node is not None:
                stack[-1].add_children(node)

                if isinstance(node, IfNode):
                    stack.append(node)

                if isinstance(node, ElseIfNode):
                    stack.pop()
                    parent_if = stack[-1]
                    parent_if.add_children(node)
                elif isinstance(node, ElseNode):
                    stack.pop()
                    parent_if = stack[-1]
                    parent_if.add_children(node)




                        


                   