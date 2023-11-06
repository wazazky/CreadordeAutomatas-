from igraph import Graph
from igraph import plot
from PIL import Image, ImageDraw, ImageFont

def generate_token_automaton(token_name, lexemes):
    automaton = Graph(directed=True)

    # Agregar nodos
    automaton.add_vertex('I', shape='point', pos=(-1, -1))  # Nodo inicial en la posición (0, 0)
    automaton.add_vertex('F', shape='doublecircle')  # Nodo final en la esquina superior derecha

    state_counter = 1
    for i in range(len(lexemes)):
        lexeme = lexemes[i]
        current_state = 'I'
        for j in range(len(lexeme)):
            state = f'S{i}_{j}'
            automaton.add_vertex(state, shape='circle')

            if automaton.get_eid(current_state, state, error=False) == -1:
                automaton.add_edge(current_state, state, label=lexeme[j])
                current_state = state
            else:
                existing_next_state = automaton.neighbors(current_state, mode='out', error=False)
                if existing_next_state and existing_next_state[0] != state:
                    automaton.add_edge(current_state, state, label=lexeme[j])
                    current_state = state
                else:
                    current_state = existing_next_state[0]

        automaton.add_edge(current_state, 'F', label='Fin')

    # Dibujar autómata
    visual_style = {
        'vertex_shape': 'circle',
        'vertex_size': 45,
        'edge_width': 1,
        'vertex_label': automaton.vs['name'],
        'edge_label': automaton.es['label'],
        'layout': automaton.layout('kk')
    }

    # Generar el dibujo del autómata
    image_path = f'{token_name}_automaton.png'
    plot(automaton, image_path, **visual_style, bbox=(0, 0, 800, 800))


    # Agregar título en la parte superior de la imagen
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial.ttf', 18)
    title = f'Token: {token_name}\nLexemas: {", ".join(lexemes)}'
    draw.text((10, 10), title, font=font, fill='black')

    # Guardar la imagen con el título agregado
    image.save(image_path)

file_name = input('Ingrese el nombre del archivo: ')

decoded_content = ""
try:
    with open(file_name, 'r', encoding='utf-8') as file:
        decoded_content = file.read()
except UnicodeDecodeError:
    print("Error: No se puede decodificar el archivo con UTF-8. Intentando con otra codificación...")
    try:
        with open(file_name, 'r', encoding='latin-1') as file:
            decoded_content = file.read()
    except UnicodeDecodeError:
        print("Error: No se puede decodificar el archivo con ninguna codificación conocida.")
        exit()

for line in decoded_content.splitlines():
    token_data = line.strip().split('\t')
    token_name = token_data[0]
    lexemes = token_data[1].split(', ')
    generate_token_automaton(token_name, lexemes)

    print(f'Se generó el autómata para el token {token_name}.')

print('Proceso de generación de autómatas completado.')
