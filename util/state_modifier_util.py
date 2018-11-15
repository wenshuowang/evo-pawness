from model.pawn import Pawn


def mirror_coordinates(x,y, y_axis_coor = 4):
    y -= y_axis_coor
    y *= -1
    y += y_axis_coor
    return (x,y)

def object_change_coordinates(pawn):
    (x_new,y_new) = mirror_coordinates(pawn.x, pawn.y)
    pawn.x = x_new
    pawn.y = y_new


def mirror_state(input_state):
    """

    :param state: State
        Test
    :return:
    """
    from copy import deepcopy
    # iterate through pawn
    state = deepcopy(input_state)
    state.turn += 5

    black_list_pawn = state.black_pawn_list
    white_list_pawn = state.white_pawn_list
    white_king = state.white_king
    black_king = state.black_king
    state.black_pawn_list = state.white_pawn_list
    state.white_pawn_list = black_list_pawn
    state.black_king = state.white_king
    state.white_king = black_king
    list_total_pawn = black_list_pawn + white_list_pawn + [white_king] + [black_king]

    for pawn in list_total_pawn:
        assert isinstance(pawn, Pawn)
        pawn.player = state.player_list[(pawn.player.color + 1) % 2]
        object_change_coordinates(pawn)
    state.refresh_board()
    return state

def get_key_mirror_action(input_key_action:str):
    """

    :param input_key_action:
    :return:
    """

    # case of attack action
    # format attack input : mp*<y coor>,<x coor>*<y direction>,<x direction>
    # case of move action
    # format move input : mp*<y coor>,<x coor>*<y direction>,<x direction>
    if input_key_action[0:2] == 'mp':
        input_key_action_split = input_key_action.split('*')
        coor_string = input_key_action_split[1]
        y_coor = coor_string.split(",")[0]
        x_coor = coor_string.split(",")[1]
        (x_coor, y_coor) = mirror_coordinates(int(x_coor), int(y_coor))
        coor_dir_string = input_key_action_split[2]
        y_coor_dir = coor_dir_string.split(",")[0]
        x_coor_dir = coor_dir_string.split(",")[1]
        (x_coor_dir, y_coor_dir) = mirror_coordinates(int(x_coor_dir), int(y_coor_dir),0)

        return input_key_action_split[0] + "*" + \
               str(y_coor) + ',' + str(x_coor) + "*" + \
                str(y_coor_dir) + ',' + str(x_coor_dir)



    # case of activate action
    # format activate input : a*<y coor>,<x coor>

    if input_key_action[0:2] == "a*":
        input_key_action_split = input_key_action.split("*")
        coor_string = input_key_action_split[1]
        y_coor = coor_string.split(",")[0]
        x_coor = coor_string.split(",")[1]
        (x_coor, y_coor) = mirror_coordinates(int(x_coor), int(y_coor))
        return input_key_action_split[0] + "*" + \
               str(y_coor) + ',' + str(x_coor)

    # case of promote action
    # format promote input : p*<y coor>,<x coor>*<class choice first character example:S>
    elif input_key_action[0:2] == "p*":
        input_key_action_split = input_key_action.split("*")
        coor_string = input_key_action_split[1]
        y_coor = coor_string.split(",")[0]
        x_coor = coor_string.split(",")[1]
        (x_coor, y_coor) = mirror_coordinates(int(x_coor), int(y_coor))
        return input_key_action_split[0] + "*" + \
               str(y_coor) + ',' + str(x_coor) + "*" + \
                str(input_key_action_split[2])
    
    elif input_key_action == "pass":
        return "pass"
