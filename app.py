import random
import streamlit as st

st.set_page_config(
    page_title="ML Shooter Quiz",
    page_icon="🎯",
    layout="centered"
)

QUESTIONS = [
    {
        "question": "¿Qué significa Machine Learning?",
        "options": [
            "Una técnica para diseñar páginas web",
            "Una rama de la IA que aprende patrones a partir de datos",
            "Un lenguaje de programación",
            "Un sistema operativo"
        ],
        "answer": "Una rama de la IA que aprende patrones a partir de datos",
        "explanation": "Machine Learning permite aprender patrones a partir de datos."
    },
    {
        "question": "¿Cuál es un tipo principal de Machine Learning?",
        "options": [
            "Aprendizaje supervisado",
            "Aprendizaje manual",
            "Aprendizaje estático",
            "Aprendizaje visual únicamente"
        ],
        "answer": "Aprendizaje supervisado",
        "explanation": "Los tipos principales incluyen supervisado, no supervisado y por refuerzo."
    },
    {
        "question": "¿Qué caracteriza al aprendizaje supervisado?",
        "options": [
            "Trabaja con datos etiquetados",
            "Nunca necesita datos",
            "Solo utiliza imágenes",
            "No permite predicciones"
        ],
        "answer": "Trabaja con datos etiquetados",
        "explanation": "El modelo aprende con ejemplos que contienen una respuesta conocida."
    },
    {
        "question": "¿Cuál es un ejemplo de clasificación?",
        "options": [
            "Predecir el precio de una vivienda",
            "Agrupar clientes por similitud",
            "Determinar si un correo es spam o no spam",
            "Reducir la cantidad de columnas"
        ],
        "answer": "Determinar si un correo es spam o no spam",
        "explanation": "La clasificación predice categorías o clases."
    },
    {
        "question": "¿Cuál es un ejemplo de regresión?",
        "options": [
            "Predecir el precio de una vivienda",
            "Clasificar imágenes como gato o perro",
            "Agrupar documentos",
            "Detectar comunidades"
        ],
        "answer": "Predecir el precio de una vivienda",
        "explanation": "La regresión predice valores numéricos."
    },
    {
        "question": "¿Qué busca el aprendizaje no supervisado?",
        "options": [
            "Aprender exclusivamente con etiquetas",
            "Encontrar patrones en datos sin etiquetas",
            "Eliminar todos los datos",
            "Reemplazar la base de datos"
        ],
        "answer": "Encontrar patrones en datos sin etiquetas",
        "explanation": "Busca estructuras o grupos sin una respuesta etiquetada."
    },
    {
        "question": "¿Cuál de estos algoritmos se usa para clustering?",
        "options": [
            "K-Means",
            "Linear Regression",
            "Logistic Regression",
            "Naive Bayes"
        ],
        "answer": "K-Means",
        "explanation": "K-Means agrupa datos según su similitud."
    },
    {
        "question": "¿Qué es el overfitting?",
        "options": [
            "Cuando el modelo no aprende nada",
            "Cuando memoriza demasiado el entrenamiento y generaliza mal",
            "Cuando faltan columnas",
            "Cuando siempre obtiene 50% de precisión"
        ],
        "answer": "Cuando memoriza demasiado el entrenamiento y generaliza mal",
        "explanation": "El overfitting aparece cuando el modelo se adapta demasiado a los datos de entrenamiento."
    },
    {
        "question": "¿Para qué se divide un dataset en entrenamiento y prueba?",
        "options": [
            "Para evaluar el modelo con datos no usados en el entrenamiento",
            "Para duplicar los datos",
            "Para eliminar la variable objetivo",
            "Para evitar usar algoritmos"
        ],
        "answer": "Para evaluar el modelo con datos no usados en el entrenamiento",
        "explanation": "El conjunto de prueba permite evaluar la generalización."
    },
    {
        "question": "¿Qué es una feature?",
        "options": [
            "La predicción final",
            "Una variable de entrada utilizada por el modelo",
            "El nombre del archivo Python",
            "Un error de programación"
        ],
        "answer": "Una variable de entrada utilizada por el modelo",
        "explanation": "Una feature es una variable de entrada, como edad, precio o cantidad."
    }
]


def create_question():
    question = random.choice(QUESTIONS)
    options = question["options"].copy()
    random.shuffle(options)
    return {**question, "options": options}


def reset_game():
    st.session_state.question = create_question()
    st.session_state.score = 0
    st.session_state.shots = 0
    st.session_state.finished = False
    st.session_state.feedback = None


if "question" not in st.session_state:
    reset_game()

st.title("🎯 ML Shooter Quiz")
st.write("Dispara seleccionando la alternativa correcta. Cada respuesta es un disparo.")

st.progress(st.session_state.score / 5, text=f"Progreso: {st.session_state.score}/5 aciertos")
st.metric("🎯 Puntuación", f"{st.session_state.score}/5")
st.caption(f"Disparos realizados: {st.session_state.shots}")

question = st.session_state.question

st.subheader(f"🎯 Objetivo: {question['question']}")
st.write("Elige el objetivo correcto:")

with st.form("shooter_form"):
    selected = st.radio(
        "Alternativas",
        question["options"],
        index=None,
        key=f"answer_{st.session_state.shots}"
    )

    fire = st.form_submit_button("🔫 DISPARAR", type="primary")

if fire:
    if selected is None:
        st.warning("Selecciona un objetivo antes de disparar.")
    else:
        st.session_state.shots += 1

        if selected == question["answer"]:
            st.session_state.score += 1
            st.session_state.feedback = ("correct", question["explanation"])
        else:
            st.session_state.feedback = (
                "wrong",
                f"Respuesta correcta: {question['answer']}."
            )

        if st.session_state.score >= 5:
            st.session_state.finished = True
        else:
            st.session_state.question = create_question()

        st.rerun()

if st.session_state.feedback:
    status, message = st.session_state.feedback

    if status == "correct":
        st.success(f"💥 ¡Impacto! Respuesta correcta. {message}")
    else:
        st.error(f"❌ Fallaste el objetivo. {message}")

if st.session_state.finished:
    st.balloons()
    st.success("🏆 ¡Victoria! Has conseguido 5 respuestas correctas.")
    st.write("¡Excelente puntería, agente de Machine Learning!")

    if st.button("🔄 Reiniciar partida"):
        reset_game()
        st.rerun()
else:
    if st.button("🔄 Reiniciar partida"):
        reset_game()
        st.rerun()

st.divider()
st.caption("Nota: esta versión usa botones y selección de alternativas, compatible con Streamlit sin un motor de videojuegos.")
