from main import MoveNode, TurnNode, WaitNode, IfNode

user_lines = {}
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
        "units": ["ms", "s"],
        "optional_subcommands": [],
        "expected_optional_subcommands": 0
    },
    "SET": {
        "subcommands": ["moveSpeed", "turnSpeed"],
        "expected_subcommands": 1,
        "expected_number_args": 1,
        "optional_subcommands": [],
        "expected_optional_subcommands": 0
    }
}

def is_number(token): ## helper function to check whether tokens are number while handling loat inputs
    try:
        float(token)
        return True
    except ValueError:
        return False


def tokenizer_commands(tokenized, command):
    
    current_subcommands = []
    current_number_args = []
    current_optional_args = []

    if command not in command_nodes:
        print("Error: invalid command")
        return
            
    current_valid_subcommands = command_nodes[command]["subcommands"]
    current_valid_optional_subcommands = command_nodes[command]["optional_subcommands"]


    for token in tokenized[1:]: # loop through non-command (0 index) tokens.categorise and sort them into lists
        if token in current_valid_subcommands:
            current_subcommands.append(token)
        elif is_number(token):
            current_number_args.append(float(token))
        elif token in current_valid_optional_subcommands:
            current_optional_args.append(token)
        else:
            print("Error: couldnt find at least one of those arguments.")
            return
            
    print(current_subcommands); print(current_number_args); print(current_optional_args)
    ## to line 91: check whether user has inputted correct amount of subcommands, number arguments, and optional subcommands. f.e MOVE requires there to be NO optional subcommands ('MOVE forward 10')
    expected_number_args = command_nodes[command]["expected_number_args"]; expected_subcommands = command_nodes[command]["expected_subcommands"]; expected_optional_subcommands = command_nodes[command]["expected_optional_subcommands"]
            
    current_lists = [current_subcommands, current_number_args, current_optional_args]
    expected_lists = [expected_number_args, expected_subcommands, expected_optional_subcommands]

    for index in range(len(current_lists)):
        if check_list_lengths(expected_lists[index], current_lists[index]) != True: 
            print("invalid amount of subcommands/args/numbers")
            return
    
    print("RUN THE COMMAND")### TO-DO, create a node, execute the commands, link to rasberry pi
            


def check_which_node_type(command): # helper function to determine node type (command, statement, or other (placeholder))
    if command.isupper() and command in command_nodes:
        return "command"
    elif command.islower() and command in statement_nodes:
        return "statement"
    else:
        return "neither"
    
def check_list_lengths(expected_args, current_args):
    if len(current_args) != expected_args:
        return False
    else:
        return True
    

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
            "left": condition_builder(left_tokens_sorted, left_tokens, first_word),
            "right": condition_builder(right_tokens_sorted, right_tokens, first_word)
        })
        
    return node_dict

def tokenizer_statements(tokenized, first_word, user_input):
    expectIndentation = True
    const_indentation = 4

    #condition = 

    #IfNode(condition)
    ################ complete this


while True:
    user_input = input("> ")
    
    tokenized = user_input.split()

    if user_input.strip() == "": #ignore blank lines
        continue
    else:
        line_length = len(tokenized)
        first_word = tokenized[0]

        type_of_logic = check_which_node_type(first_word)

        if type_of_logic == "command":
            tokenizer_commands(tokenized, first_word)

        elif type_of_logic == "statement":
            tokenizer_statements(tokenized, first_word, user_input)
            #TO-DO: statemenet parser + tokenizer

        elif type_of_logic == "neither":
            print("Error: invalid input")
            continue