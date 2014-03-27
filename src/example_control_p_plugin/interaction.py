# yanked from: http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
def calculate_edit_distance(s1, s2):
    oneago = None
    thisrow = range(1, len(s2) + 1) + [0]
    for x in xrange(len(s1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(s2) + [x + 1]
        for y in xrange(len(s2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (s1[x] != s2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(s2) - 1]


def sort_files(s, files):
    files = [(k, v, calculate_edit_distance(k, s)) for k, v in files]
    files = sorted(files, key= lambda x: x[2])
    return files

# plugins have access to all state variables in the text editor
def draw_matching_file_names(graphics_state, local_state, global_state):
    dims = graphics_state.get_dimensions()
    graphics_state.draw_rectangle_absolute(0, 0, dims['screen_width'], graphics_state.get_grid_y(21), '#657b83')

    _, vy, _ = local_state.get_visual_anchors()
    graphics_state.draw_rectangle_absolute(0, graphics_state.get_grid_y(vy - 1), dims['screen_width'], graphics_state.get_grid_y(vy), '#dc322f')

    files = sort_files(global_state.command_buffer, local_state.get_meta_data()['fuzzy_file_select'].items())

    graphics_state.write_text_grid(0, 0, global_state.command_buffer, color='#002B36')

    for i in range(20):
        graphics_state.write_text_grid(0, i + 1, files[i][0], color='#002B36')

# router calls this logic
def fuzzy_file_select(s, graphics_state, local_state, global_state):
    post = [lambda:draw_matching_file_names(graphics_state, local_state, global_state)]
    render_page([], post, graphics_state, local_state, global_state)

# router calls this logic
def fuzzy_file_enter(graphics_state, local_state, global_state):
    _, vy, _ = local_state.get_visual_anchors()
    filename = sort_files(global_state.command_buffer, local_state.get_meta_data()['fuzzy_file_select'].items())[vy - 2][0]

    global_state.start_instance(filename)
    global_state.curr_instance += 1
    global_state.set_GUI_reference(graphics_state)
