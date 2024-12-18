import matplotlib.pyplot as plt

def graficar_entrenamiento(retornos, titulos, filename):
    ruta_imagen = 'generar_graficas/imagenes_entrenamiento/' + filename
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Graficar en el subplot
    ax.plot(retornos[0])
    ax.set_title(titulos[0])
    
    # Etiquetar ejes
    ax.set_xlabel('Iteración')
    ax.set_ylabel('Retorno')
    
    # Ajustar diseño
    plt.tight_layout()
    
    # Guardar figura
    plt.savefig(ruta_imagen)
    plt.close()