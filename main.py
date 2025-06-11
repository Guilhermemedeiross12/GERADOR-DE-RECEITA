
import streamlit as st
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv
import os

# Configuração da API key e Modelo
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Utilizando o modelo especificado
try:
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    st.error(f"Erro ao carregar o modelo especificado: {e}")
    st.info("Verifique se o nome do modelo está correto e se sua chave API tem acesso a ele")
    st.stop()

def gerar_resposta_gemini(prompt_completo):
    try:
        response = model.generate_content(prompt_completo)

        if response.parts:
            return response.text
        else:
            if response.prompt_feedback:
                st.warning(f"O prompt foi bloqueado. Razão: {response.prompt_feedback.block_reason}")
                if response.prompt_feedback.safety_ratings:
                    for rating in response.prompt_feedback.safety_ratings:
                        st.caption(f"Categoria: {rating.category}, Probabilidade: {rating.probability}")
            return "A IA não pôde gerar uma resposta para esse prompt. Verifique as mensagens acima ou tente reformular seu pedido."
    except Exception as e:
        st.error(f"Erro ao gerar resposta da IA: {str(e)}")
        if hasattr(e, 'message'):
            st.error(f"Detalhe da API Gemini: {e.message}")

# Configuração da página
st.set_page_config(page_title="Gerador de Receitas Personalizadas - IA")

# Título do sistema
st.title("Gerador de Receitas Culinárias Personalizadas com IA")
st.markdown("Crie sua própria receita personalizada com a ajuda da Inteligência Artificial!")

# Entrada do usuário
lista_ingrediente = st.text_area(
    "Liste os Ingredientes Principais que possui:",
    placeholder="Ex: frango, tomate, cebola, arroz"
)

tipo_culinaria = st.selectbox(
    "Escolha o Tipo de Culinária desejado:",
    ["Italiana", "Brasileira", "Asiática", "Mexicana", "Qualquer uma"],
)

nivel_dificuldade = st.slider("Nível de Dificuldade", 1, 5, 3)

descricao_dificuldade = {
    1: "Muito fácil",
    2: "Fácil",
    3: "Moderado",
    4: "Difícil",
    5: "Desafiador"
}

texto_dificuldade = f"{descricao_dificuldade[nivel_dificuldade]}"

dificuldade = st.caption(f"Nível selecionado: {nivel_dificuldade} - {texto_dificuldade}")

restricao_alimentar = st.checkbox("Possui Restrição Alimentar?")

if restricao_alimentar:
    qual_restricao = st.text_input(
        "Informe a restrição:",
        placeholder="Ex: Sem glúten, vegetariana, sem lactose"
    )

if st.button("Sugerir Receita"):
    if not lista_ingrediente:
        st.warning("Por favor, informe a lista de ingredientes.")
    elif not tipo_culinaria:
        st.warning("Por favor, informe o tipo de culinária.")
    else:
        prompt_aluno = (
            f"Sugira uma receita {tipo_culinaria} com nível de dificuldade {nivel_dificuldade} sendo {texto_dificuldade}. Deve usar principalmente os seguintes ingredientes: {lista_ingrediente}, {qual_restricao if restricao_alimentar else "sem restrição alimentar"}. Apresente o nome da receita, uma lista de ingredientes adicionais se necessário, e um breve passo a passo."
        )

        st.markdown("---")
        st.markdown("*Prompt que será enviado para a IA (parra fins de aprendizado)*")
        st.text_area("", prompt_aluno, height=250)
        st.markdown("---")

        st.info("Aguarde, a IA está montando a receita...")
        resposta_ia = gerar_resposta_gemini(prompt_aluno)

        if resposta_ia:
            st.markdown("### Sugestão de receita da IA:")
            st.markdown(resposta_ia)
        else:
            st.error("Não foi possível gerar a receita. Verifique as mensagens acima ou tente novamente mais tarde.")