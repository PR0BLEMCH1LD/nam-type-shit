import sys
import pygame
import math
from shapely.geometry import Polygon, Point, LineString
from custom_input import CustomInput
from checkbox import CheckBox
from button import Button
from graph import Graph

width = 800
height = 600
screen_color = (255, 255, 255)
scale = 30
move_offset = (20, 20)

base_vertices = [(0, 0), (1, 0), (1, 6), (2, 6), (2, 0), (5, 0), (5, 1), (3, 1), (3, 3), (5, 3), (5, 4), (3, 4), (3, 6), (6, 6), (6, 0), (9, 0), (9, 1), (7, 1), (7, 3), (9, 3), (9, 4), (7, 4), (7, 6), (10, 6), (10, 8), (9, 8), (9, 7), (0, 7)]
             
def draw_line(screen, start, end, line_color, line_width=1):
    pygame.draw.line(screen, line_color, (start[0] * scale + move_offset[0], start[1] * scale + move_offset[1]), (end[0] * scale + move_offset[0], end[1] * scale + move_offset[1]), line_width)

def draw_lines(screen, lines, color, line_width=1):
    for line in lines:
        draw_line(screen, line[0], line[1], color, line_width)

def line_intersect_poly(line, edges):
    intersect = False
    for edge in edges:
        if LineString(line).intersects(LineString(edge)) and len(set([*line, *edge])) == 4:
            intersect = True
    return intersect

def create_base_edges():
    base = [(base_vertices[i], base_vertices[i + 1]) for i in range(len(base_vertices) - 1)] + [(base_vertices[-1], base_vertices[0])]
    base[24], base[-1] = base[-1], base[24]
    return base

def create_base_vis():
    base = []
    for i in range(len(base_vertices)):
        for j in range(i + 1, len(base_vertices)):
            line = (base_vertices[i], base_vertices[j])
            if not line_intersect_poly(line, base_edges) and Polygon(base_vertices).contains(Point((base_vertices[i][0] + base_vertices[j][0]) / 2, (base_vertices[i][1] + base_vertices[j][1]) / 2)):
                base.append(line)
    base[38], base[-2] = base[-2], base[38]
    return base

base_edges = create_base_edges()
base_vis = create_base_vis()

def create_vertices(mul):
    if mul == 0:
        return []
    
    vertices = [(0, 0)]
    for i in range(mul):
        w, h = 9 * i, 8 * i
        vertices.append((base_vertices[27][0] + w, base_vertices[27][1] + h))
        vertices.append((base_vertices[26][0] + w, base_vertices[26][1] + h))

    vertices.append((base_vertices[25][0] + 9 * (mul - 1), base_vertices[25][1] + 8 * (mul - 1)))
    vertices.append((base_vertices[24][0] + 9 * (mul - 1), base_vertices[24][1] + 8 * (mul - 1)))

    for i in range(mul - 1, -1, -1):
        w, h = 9 * i, 8 * i
        for j in range(23, 1, -1):
            vertices.append((base_vertices[j][0] + w, base_vertices[j][1] + h))

    vertices.append(base_vertices[1])
    return vertices

def create_edges(mul):    
    edges = []
    for i in range(mul):
        w, h = 9 * i, 8 * i
        for j in range(i != 0, len(base_edges) - (i != mul - 1)):                
            edges.append(((base_edges[j][0][0] + w, base_edges[j][0][1] + h), (base_edges[j][1][0] + w, base_edges[j][1][1] + h)))
    return edges

def from_point_add_vis(point, vis, vertices):
    quad = int(point[1] / 8)
    search_vertices = vertices[2 * quad:2 * quad + 4] + vertices[-22 * quad - 24:-22 * quad - 1] + [vertices[-22 * quad - 1]]
    search_edges = [(search_vertices[i], search_vertices[i + 1]) for i in range(len(search_vertices) - 1)] + [(search_vertices[-1], search_vertices[0])]
    for vertex in search_vertices:
        line = (point, vertex)
        if not line_intersect_poly(line, search_edges):
            vis.append(line)

def get_edges_for_region(edges, start, end, mul):
    start_quad, end_quad = int(start[1] / 8), int(end[1] / 8)

    if start_quad > end_quad:
        start_quad, end_quad = end_quad, start_quad

    return edges[start_quad * 26 + 1 - (start_quad == 0):(end_quad + 1) * 27 + (end_quad + 1 == mul) - end_quad]

def create_vis(vertices, edges, start, end, mul):
    if not mul:
      return []

    vis = []
    for i in range(mul):
        w, h = 9 * i, 8 * i
        for j in range(len(base_vis) - 2 * (i != mul - 1)):
            vis.append(((base_vis[j][0][0] + w, base_vis[j][0][1] + h - (j + 1 if j < 2 and i else 0)), (base_vis[j][1][0] + w, base_vis[j][1][1] + h)))
    
    if start:
        from_point_add_vis(start, vis, vertices)
    if end:
        from_point_add_vis(end, vis, vertices)
    
    if start and end:
        line = (start, end)

        if not line_intersect_poly(line, get_edges_for_region(edges, start, end, mul)):
            vis.append(line)    

    return vis

def create_graph(edges, vis):
    graph = Graph()
    for edge in edges:
        graph.addEdge(edge[0], edge[1], math.sqrt((edge[1][0] - edge[0][0]) ** 2 + (edge[1][1] - edge[0][1]) ** 2))

    for line in vis:
        graph.addEdge(line[0], line[1], math.sqrt((line[1][0] - line[0][0]) ** 2 + (line[1][1] - line[0][1]) ** 2))
    return graph

def main():
    global scale, move_offset
    
    pygame.init()

    font = pygame.font.SysFont('Consolas', 30)
    font_height = font.get_height()
    screen = pygame.display.set_mode((width, height))

    mul = 1

    k_x, k_y = 10, height - 10 - font_height
    k_indicator = font.render('K = ', False, (0, 0, 0))
    kinp_inner_pad_x = 8
    k_input = CustomInput(font, str(mul), (k_x + k_indicator.get_width() + kinp_inner_pad_x, k_y), inner_pad_x=kinp_inner_pad_x)

    vis_x, vis_y = 10, height - 6 * font_height - 10
    vis_indicator = font.render('Graph', False, (0, 0, 0))
    vis_cbox_size = 20
    vis_cbox = CheckBox(False, vis_cbox_size, (vis_x + vis_indicator.get_width() + 15, vis_y + (font_height - vis_cbox_size) / 2), (255, 0, 0))

    sb_inner_pad_x, sb_inner_pad_y = 10, 7
    sb_text = "START"
    start_button = Button(False, font, sb_text, (width - font.size(sb_text)[0] - sb_inner_pad_x - 10, 10 + sb_inner_pad_y), (0, 255, 0), inner_pad_x=sb_inner_pad_x, inner_pad_y=sb_inner_pad_y)

    cb_inner_pad_x, cb_inner_pad_y = 10, 7
    cb_text = "CLEAR"
    clear_button = Button(False, font, cb_text, (width - font.size(cb_text)[0] - cb_inner_pad_x - 10, 10 + 2 * sb_inner_pad_y + font_height + cb_inner_pad_y + 10), (255, 255, 153), inner_pad_x=cb_inner_pad_x, inner_pad_y=cb_inner_pad_y)
    
    scale_x, scale_y = 10, height - 7 * font_height - 10
    scale_indicator = font.render('Scale = ', False, (0, 0, 0))
    sinp_inner_pad_x = 8
    scale_input = CustomInput(font, str(scale), (scale_x + scale_indicator.get_width() + sinp_inner_pad_x, scale_y), inner_pad_x=sinp_inner_pad_x)

    m_start, m_end, start, end = None, None, None, None
    pickable = True
    
    vertices = create_vertices(mul)
    edges = create_edges(mul)
    vis = create_vis(vertices, edges, start, end, mul)
    poly = Polygon(vertices)
    shortest_path = None

    last_m_pos = None
    m_down = False
    m_delta = (0, 0)

    new_scale = scale

    while True:
        screen.fill(screen_color)

        for i in range(math.ceil(width / scale) + 1):
            draw_line(screen, (i - math.ceil(move_offset[0] / scale), -math.ceil(move_offset[1] / scale)), (i - math.ceil(move_offset[0] / scale), math.ceil((height - move_offset[1]) / scale)), (192, 192, 192))

        for i in range(math.ceil(height / scale) + 1):
            draw_line(screen, (-math.ceil(move_offset[0] / scale), i - math.ceil(move_offset[1] / scale)), (math.ceil(width / scale), i - math.ceil(move_offset[1] / scale)), (192, 192, 192))

        try:
            new_mul = int(k_input.value)
        except:
            new_mul = 0

        if mul != new_mul:
            mul = new_mul
            m_start, m_end, start, end = None, None, None, None
            vertices = create_vertices(mul)
            edges = create_edges(mul)
            vis = create_vis(vertices, edges, start, end, mul)
            poly = Polygon(vertices)
            shortest_path = None
            pickable = True

        draw_lines(screen, edges, (0, 0, 0), 2)

        if vis_cbox.checked:
            draw_lines(screen, vis, (105, 105, 105))

        if shortest_path:
            shortest_path_path = shortest_path[0]
            for i in range(len(shortest_path_path) - 1):
                draw_line(screen, shortest_path_path[i], shortest_path_path[i + 1], (255, 0, 0), 2)

        if m_start:
            pygame.draw.circle(screen, (0, 255, 0), (m_start[0] + move_offset[0], m_start[1] + move_offset[1]), scale / 6)

        if m_end:
            pygame.draw.circle(screen, (0, 0, 255), (m_end[0] + move_offset[0], m_end[1] + move_offset[1]), scale / 6)

        start_button.disabled = not start or not end
        clear_button.disabled = not start and not end

        screen.blit(k_indicator, (k_x, k_y))

        v_indicator = font.render(f'V = {len(vertices)}', False, (0, 0, 0))
        screen.blit(v_indicator, (10, height - 2 * font_height - 10))

        e_indicator = font.render(f'E = {len(edges)}', False, (0, 0, 0))
        screen.blit(e_indicator, (10, height - 3 * font_height - 10))

        d_indicator = font.render(f'D = {round(shortest_path[1], 2) if shortest_path else 0}', False, (0, 0, 0))
        screen.blit(d_indicator, (10, height - 4 * font_height - 10))

        t_indicator = font.render(f'T = {round(shortest_path[2], 5) if shortest_path else 0}s', False, (0, 0, 0))
        screen.blit(t_indicator, (10, height - 5 * font_height - 10))

        screen.blit(vis_indicator, (vis_x, vis_y))
        
        screen.blit(scale_indicator, (scale_x, scale_y))

        events = pygame.event.get()
        k_input.render(screen, events)
        vis_cbox.render(screen, events)
        scale_input.render(screen, events)

        start_button.render(screen, events)
        clear_button.render(screen, events)

        if start_button.pressed:
            start_quad, end_quad = int(start[1] / 8), int(end[1] / 8)

            if start_quad > end_quad:
                start_quad, end_quad = end_quad, start_quad
            
            graph = create_graph(get_edges_for_region(edges, start, end, mul), vis[start_quad * 40:(end_quad + 1) * 40 + 2 * (end_quad + 1 == mul)] + vis[(mul - 1) * 40 + 42:])
            shortest_path = graph.findShortestPath(start, end)
            pickable = False

        if clear_button.pressed:
            m_start, m_end, start, end = None, None, None, None
            vis = create_vis(vertices, edges, start, end, mul)
            shortest_path = None
            pickable = True

        for event in events:                
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                last_m_pos = pygame.mouse.get_pos()
                m_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                m_down = False
            if event.type == pygame.MOUSEMOTION and m_down:
                m_pos = pygame.mouse.get_pos()
                m_delta = (m_pos[0] - last_m_pos[0], m_pos[1] - last_m_pos[1])
                move_offset = (move_offset[0] + m_delta[0], move_offset[1] + m_delta[1])
                last_m_pos = m_pos
            if event.type == pygame.MOUSEMOTION:
                if not k_input.cursor_in_area and not vis_cbox.cursor_in_area and not start_button.cursor_in_area and not clear_button.cursor_in_area and not scale_input.cursor_in_area:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if event.type == pygame.MOUSEBUTTONDOWN and pickable and not k_input.cursor_in_area and not vis_cbox.cursor_in_area and not start_button.cursor_in_area and not clear_button.cursor_in_area and not scale_input.cursor_in_area:
                m_state = pygame.mouse.get_pressed()
                m_pos = pygame.mouse.get_pos()
                m_pos = (m_pos[0] - move_offset[0], m_pos[1] - move_offset[1])
                pos = (m_pos[0] / scale, m_pos[1] / scale)

                if poly.contains(Point(pos)):
                    if m_state[0] == True and m_state[2] == False:
                        m_start = m_pos
                        start = pos
                    
                    if m_state[2] == True and m_state[0] == False:
                        m_end = m_pos
                        end = pos

                    vis = create_vis(vertices, edges, start, end, mul)
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    new_scale = scale ** 1.02
                else:
                    new_scale = scale ** 0.98
                    
                ratio = new_scale / scale

                m_pos = pygame.mouse.get_pos()
                pos = (m_pos[0] / scale, m_pos[1] / scale)
                new_pos = (m_pos[0] / new_scale, m_pos[1] / new_scale)

                if m_start:
                    m_start = (m_start[0] * ratio, m_start[1] * ratio)
                if m_end:
                    m_end = (m_end[0] * ratio, m_end[1] * ratio)

                move_offset = (move_offset[0] * ratio - (pos[0] - new_pos[0]) * new_scale, move_offset[1] * ratio - (pos[1] - new_pos[1]) * new_scale)
                scale = new_scale
              
        pygame.display.update()
        
if __name__ == '__main__':
    main()