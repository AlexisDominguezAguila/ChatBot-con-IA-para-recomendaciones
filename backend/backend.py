import sqlite3
import re
from openai import APIError

formato = """
Tu nombre sera IA TEC, Las consultas se hacen a la tabla productos.
La tabla productos cuenta con los campos de nombre, precio, stock, categoria, fabricante, url_imagen, sku.
Las categorias de la tabla productos son: Parlantes, Audifonos, Celulares, Laptops, Tablets, Camaras, Componentes, Consolas, Smartwatch y Televisores.
En la tabla productos la informacion de fabricante, tambien hace referencia a la marca u otros sinonimos. Ademas, toda la informacion de fabricate esta en MAYUSCULAS.
Interpreta la necesidad de la siguiente peticion y crea una consulta SQLite3 que cumpla con:
{question}
Despues de interpretarla y crear la consulta, en el caso de que la consulta trate sobre algun producto, modificala para solo mostrar el nombre, precio y fabricante.
en caso contrario, eres libre de modificar la consulta teniendo en cuenta la informacion principal sobre la base de datos y puedes crear la cosulta que cumpla con la interpretación que hiciste.
Finalmente, escribe solo y únicamente la consulta SQLite3 que creaste. Como informacion adicional, si la pregunta del cliente no es sobre alguna pregunta, eres libre de inventar una consulta para obtener algun producto de tu eleccion.
"""

formato_nuevo = """
La consulta entiendas es la solicitud del cliente y la respuesta es el resultado a esa consulta {producto_consulta}.
Tu rol es describir solamente la respuesta, si se trata de algún producto, puedes describirlo y ofrecerle información convincente para que lo elija, y si en la respuesta hay más de un producto,
puedes explicarle cuáles son los mejores, pero si la consulta no es sobre productos, puedes generar el contexto para argumentar la respuesta.
No olvides de siempre ofrecer ayuda.
"""

def crear_consulta(user_input, client):
    prompt = formato.format(question=user_input)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            messages=[
                {"role": "system", "content": "Eres un asistente virtual encargado de crear consultas SQLite3 basadas en las preguntas del usuario."},
                {"role": "user", "content": prompt}
            ]
        )
        consulta = response.choices[0].message.content.strip()
        return consulta
    except APIError as e:
        return f"Error al procesar la solicitud: {str(e)}"

def limpiar_consulta(consulta):
    consulta_limpia = re.sub(r'```sql|```', '', consulta).strip()
    return consulta_limpia

def ejecutar_consulta(consulta):
    try:
        conn = sqlite3.connect('data/bd_productos.db')
        cursor = conn.cursor()
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados
    except sqlite3.Error as e:
        return f"Error al ejecutar la consulta: {str(e)}"

def respuesta_cliente(resultados, client):
    prompt_cliente = formato_nuevo.format(producto_consulta=resultados)
    try:
        response_cliente = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.8,
            messages=[
                {"role": "system", "content": "Eres un asistente virtual, Tu nombre es IA Tec y estás encargado de generar recomendaciones y dar información de productos tecnológicos."},
                {"role": "user", "content": prompt_cliente}
            ]
        )
        nueva_respuesta = response_cliente.choices[0].message.content.strip()
        return nueva_respuesta
    except APIError as e:
        return f"Error al procesar la solicitud: {str(e)}"