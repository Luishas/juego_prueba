# 🎯 ML Shooter Quiz - Streamlit

Quiz gamificado de Machine Learning básico. El usuario debe seleccionar la alternativa correcta y pulsar "DISPARAR".

## Características

- Banco de 10 preguntas.
- Preguntas aleatorias.
- Alternativas mezcladas.
- Sistema de disparos y puntuación.
- Feedback inmediato.
- Victoria al conseguir 5 respuestas correctas.
- Animación de globos al ganar.

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar en Streamlit Community Cloud

1. Crea un repositorio de GitHub.
2. Sube `app.py` y `requirements.txt`.
3. Ingresa a https://share.streamlit.io/
4. Selecciona el repositorio.
5. Usa `app.py` como archivo principal.
6. Pulsa Deploy.

## Nota técnica

Streamlit no es un motor de videojuegos. Esta versión simula el shooter mediante selección de objetivos y un botón de disparo. Para un juego con movimiento, balas, enemigos y colisiones en tiempo real, sería mejor usar Pygame, Godot o Unity.
