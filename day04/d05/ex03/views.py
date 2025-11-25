from django.shortcuts import render

def ex03_view(request):
    
    columns = ['Noir', 'Rouge', 'Bleu', 'Vert']

    def generate_shades(base_rgb):
        shades = []
        for i in range(50):
            factor = i / 49  
            r = int(base_rgb[0] * (1 - factor) + 255 * factor)
            g = int(base_rgb[1] * (1 - factor) + 255 * factor)
            b = int(base_rgb[2] * (1 - factor) + 255 * factor)
            shades.append(f'rgb({r},{g},{b})')
        return shades

    shades_noir = generate_shades((0, 0, 0))
    shades_rouge = generate_shades((255, 0, 0))
    shades_bleu = generate_shades((0, 0, 255))
    shades_vert = generate_shades((0, 255, 0))
    table_data = list(zip(shades_noir, shades_rouge, shades_bleu, shades_vert))
    context = {
        'columns': columns,
        'table_data': table_data
    }
    
    return render(request, 'ex03/ex03.html', context)
