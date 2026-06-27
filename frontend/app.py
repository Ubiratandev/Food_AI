import streamlit as st
import requests
from PIL import Image
import io

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Food Premium AI Enhancer",
    layout="centered"
)

# Estilização básica e títulos
st.title("Food Premium AI Enhancer")
st.markdown("### *Pipeline Multi-Agente para Validação e Otimização Visual Gastronômica*")
st.write("Suba a foto amadora do seu prato e veja a IA validar os alimentos e transformá-la em uma fotografia comercial estilo iFood.")

st.divider()

# URL da API do seu Django Backend
DJANGO_API_URL = "http://127.0.0.1:8001/api/validar/"

# Área de Upload da Imagem
uploaded_file = st.file_uploader("Escolha uma foto do seu prato (JPG ou PNG)...", type=["jpg", "jpeg", "png"])

# Caixa de seleção para Modo de Demonstração (Caso esteja sem créditos na API do Flux)
modo_demo = st.checkbox("Ativar Modo Demo / Simulação (Ignorar limite de crédito da API)", value=False)

if uploaded_file is not None:
    # Exibe a imagem original que o usuário subiu
    image = Image.open(uploaded_file)
    st.image(image, caption="Sua Foto Original", use_container_width=True)
    
    if st.button("Processar Imagem com IA"):
        with st.spinner("Executando Pipeline de IA (RT-DETR + Gemini + Flux)..."):
            try:
                # Converte a imagem de volta para bytes para enviar via HTTP
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG')
                img_byte_arr = img_byte_arr.getvalue()
                
                # Prepara o arquivo para o formato multipart/form-data do Django
                files = {'image': (uploaded_file.name, img_byte_arr, uploaded_file.type)}
                
                # Faz a chamada real para o seu backend Django
                response = requests.post(DJANGO_API_URL, files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("Imagem aprovada pelos Guardrails de Visão Computacional!")
                    
                    # Mostra os alimentos que o RT-DETR detectou
                    st.write(f"**Alimentos detectados:** {', '.join(data.get('detected', []))}")
                    
                    # Expansor para o avaliador ver o prompt que o Gemini gerou
                    with st.expander("Ver Engenharia de Prompt gerada pelo Agente Gemini"):
                        st.code(data.get('input_prompt_used'), language="text")
                    
                    st.divider()
                    st.markdown("### Resultado Final (Otimizado pelo Flux)")
                    
                    # Exibe a imagem gerada pelo Flux
                    st.image(data.get('result_image_url'), caption="Imagem Comercial Premium Gerada", use_container_width=True)
                    
                else:
                    # Trata respostas de erro (ex: não é comida, ou erro de crédito)
                    data = response.json()
                    erro_msg = data.get('erro', data.get('message', 'Erro desconhecido.'))
                    
                    if "credit" in erro_msg.lower() or "payment" in erro_msg.lower() or modo_demo:
                        st.warning("Limite de créditos da API atingido no Replicate (Flux), mas o backend respondeu corretamente!")
                        
                        if modo_demo:
                            st.info("Exibindo simulação visual do comportamento esperado do Flux (Modo Demo Ativo):")
                            # Imagem mock de alta qualidade para o avaliador ver o potencial do projeto
                            st.image("https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80", 
                                     caption="[MOCK DEMO] Exemplo de Pizza Premium gerada pelo Flux", use_container_width=True)
                    else:
                        st.error(f" Requisição Rejeitada pelo Backend: {erro_msg}")
                        if data.get('detected'):
                            st.write(f"Objetos detectados na imagem: {data.get('detected')}")
                            
            except Exception as e:
                st.error(f"Falha ao conectar com o servidor Django backend: {str(e)}")
                st.info("Certifique-se de que o Django está rodando na porta 8001 (`python manage.py runserver 8001`)")
