# 🤖 Machine Learning Quiz - Streamlit

Aplicativo educativo desarrollado con Streamlit para practicar conceptos básicos de Machine Learning.

## Características

- Banco de 10 preguntas.
- Se muestran 5 preguntas aleatorias en cada intento.
- Las alternativas también se mezclan aleatoriamente.
- Evaluación automática del resultado.
- Explicación de cada respuesta.
- Animación de globos cuando el usuario obtiene 5/5.
- Botón para comenzar un nuevo intento.

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar desde GitHub con Streamlit Community Cloud

1. Crea un repositorio en GitHub, por ejemplo: `ml-quiz-streamlit`.
2. Sube estos archivos:
   - `app.py`
   - `requirements.txt`
   - `README.md`
3. Entra a https://share.streamlit.io/
4. Inicia sesión con GitHub.
5. Selecciona **Deploy an app**.
6. Elige tu repositorio, rama y archivo principal: `app.py`.
7. Pulsa **Deploy**.

El aplicativo quedará disponible mediante un enlace público de Streamlit Community Cloud.

