import random
import streamlit as st

st.set_page_config(
    page_title="ML Quiz",
    page_icon="🤖",
    layout="centered"
)

QUESTIONS = [
    {
        "question": "¿Qué significa Machine Learning?",
        "options": [
            "Una técnica para diseñar páginas web",
            "Una rama de la IA que permite aprender patrones a partir de datos",
            "Un lenguaje de programación",
            "Un sistema operativo"
        ],
        "answer": "Una rama de la IA que permite aprender patrones a partir de datos",
        "explanation": "Machine Learning permite que los sistemas aprendan patrones usando datos, sin programar cada regla manualmente."
    },
    {
        "question": "¿Cuál es un tipo principal de Machine Learning?",
        "options": [
            "Aprendizaje supervisado",
            "Aprendizaje visual únicamente",
            "Aprendizaje manual",
            "Aprendizaje estático"
        ],
        "answer": "Aprendizaje supervisado",
        "explanation": "Los tipos más conocidos son supervisado, no supervisado y por refuerzo."
    },
    {
        "question": "¿Qué caracteriza al aprendizaje supervisado?",
        "options": [
            "Trabaja con datos etiquetados",
            "Nunca necesita datos",
            "Solo utiliza imágenes",
            "No permite hacer predicciones"
        ],
        "answer": "Trabaja con datos etiquetados",
        "explanation": "En el aprendizaje supervisado, el modelo aprende usando ejemplos que incluyen una respuesta o etiqueta conocida."
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
        "explanation": "La clasificación predice categorías o clases, como spam/no spam."
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
        "explanation": "La regresión se utiliza para predecir valores numéricos continuos."
    },
    {
        "question": "¿Qué busca el aprendizaje no supervisado?",
        "options": [
            "Aprender exclusivamente con etiquetas",
            "Encontrar patrones o estructuras en datos sin etiquetas",
            "Eliminar todos los datos",
            "Reemplazar la base de datos"
        ],
        "answer": "Encontrar patrones o estructuras en datos sin etiquetas",
        "explanation": "El aprendizaje no supervisado identifica estructuras, grupos o patrones sin una variable objetivo etiquetada."
    },
    {
        "question": "¿Cuál de estos algoritmos se usa comúnmente para clustering?",
        "options": [
            "K-Means",
            "Linear Regression",
            "Logistic Regression",
            "Naive Bayes"
        ],
        "answer": "K-Means",
        "explanation": "K-Means es un algoritmo de agrupamiento que divide los datos en grupos según su similitud."
    },
    {
        "question": "¿Qué es el overfitting?",
        "options": [
            "Cuando el modelo no aprende nada",
            "Cuando el modelo memoriza demasiado los datos de entrenamiento y generaliza mal",
            "Cuando faltan columnas en un dataset",
            "Cuando el modelo siempre obtiene 50% de precisión"
        ],
        "answer": "Cuando el modelo memoriza demasiado los datos de entrenamiento y generaliza mal",
        "explanation": "El overfitting ocurre cuando el modelo se adapta demasiado al conjunto de entrenamiento y funciona peor con datos nuevos."
    },
    {
        "question": "¿Para qué se divide un dataset en entrenamiento y prueba?",
        "options": [
            "Para evaluar el rendimiento con datos no usados durante el entrenamiento",
            "Para duplicar los datos",
            "Para eliminar la variable objetivo",
            "Para evitar usar algoritmos"
        ],
        "answer": "Para evaluar el rendimiento con datos no usados durante el entrenamiento",
        "explanation": "El conjunto de prueba ayuda a medir qué tan bien generaliza el modelo a datos no vistos."
    },
    {
        "question": "¿Qué es una feature o característica?",
        "options": [
            "La predicción final del modelo",
            "Una variable de entrada utilizada por el modelo",
            "El nombre del archivo Python",
            "Un error de programación"
        ],
        "answer": "Una variable de entrada utilizada por el modelo",
        "explanation": "Una feature es una variable de entrada, por ejemplo edad, precio o cantidad de compras."
    }
]


def create_quiz():
    selected_questions = random.sample(QUESTIONS, 5)
    quiz = []

    for question in selected_questions:
        shuffled_options = question["options"].copy()
        random.shuffle(shuffled_options)

        quiz.append({
            **question,
            "options": shuffled_options
        })

    return quiz


if "quiz" not in st.session_state:
    st.session_state.quiz = create_quiz()

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "score" not in st.session_state:
    st.session_state.score = 0


st.title("🤖 Machine Learning Quiz")
st.write("Pon a prueba tus conocimientos básicos sobre Machine Learning.")
st.info("Cada intento contiene 5 preguntas seleccionadas aleatoriamente de un banco de 10.")

with st.form("ml_quiz_form"):
    answers = {}

    for index, question in enumerate(st.session_state.quiz, start=1):
        st.subheader(f"{index}. {question['question']}")

        answers[index - 1] = st.radio(
            "Selecciona una alternativa:",
            ["Selecciona una opción"] + question["options"],
            key=f"question_{index}"
        )

    submitted = st.form_submit_button("Comprobar respuestas", type="primary")

if submitted:
    score = 0

    for index, question in enumerate(st.session_state.quiz):
        if answers[index] == question["answer"]:
            score += 1

    st.session_state.score = score
    st.session_state.submitted = True

if st.session_state.submitted:
    score = st.session_state.score

    st.divider()
    st.header(f"Resultado: {score}/5")

    if score == 5:
        st.success("¡Excelente! Respondiste todas correctamente.")
        st.balloons()
    elif score >= 3:
        st.success("¡Buen trabajo! Sigue practicando para conseguir 5/5.")
    else:
        st.warning("Puedes mejorar. Revisa las explicaciones y vuelve a intentarlo.")

    for index, question in enumerate(st.session_state.quiz, start=1):
        user_answer = st.session_state.get(f"question_{index}", "Sin respuesta")

        if user_answer == question["answer"]:
            st.markdown(f"✅ **Pregunta {index}: correcta**")
        else:
            st.markdown(
                f"❌ **Pregunta {index}: incorrecta**  \n"
                f"Respuesta correcta: **{question['answer']}**"
            )

        st.caption(question["explanation"])

    if st.button("🔄 Nuevo intento"):
        st.session_state.quiz = create_quiz()
        st.session_state.submitted = False
        st.session_state.score = 0

        for index in range(1, 6):
            st.session_state.pop(f"question_{index}", None)

        st.rerun()
