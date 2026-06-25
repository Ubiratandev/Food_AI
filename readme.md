# Food Premium AI Enhancer 🍲
### Pipeline Assíncrono Multi-Agente com Guardrails de Visão Computacional e Arquitetura Resiliente

Este projeto apresenta o desenvolvimento de um pipeline inteligente ponta a ponta voltado para a validação, otimização semântica e transformação visual gastronômica. Projetado sob a ótica de engenharia de software robusta, o sistema mitiga o desperdício de recursos computacionais (tokens) em nuvem através de filtros síncronos locais e implementa tolerância a falhas via mecanismos de *Graceful Degradation*.

---

## 📊 O Pipeline em Ação (Antes vs. Depois)

Abaixo está o exemplo real do ecossistema processando uma imagem de baixa qualidade enviada pelo usuário, gerando o contexto semântico ideal e transformando-a em um ativo comercial de alto padrão.

| 📸 Foto Amadora (Input Original do Usuário) | 🚀 Resultado Comercial (Output Otimizado por IA) |
| :---: | :---: |
| <img src="backend/fotoRuim.jpg" width="380" alt="Foto Original Amadora"> | <img src="backend/fotoPremium.jpg" width="380" alt="Resultado Profissional Estilo iFood"> |

### 🤖 Prompt Gerado pelo Agente Gemini para o Modelo de Difusão (FLUX):
> "flux_prompt":"Transform this amateur sandwich photo into premium iFood-style food photography.\n\nPreserve the original sandwich layout, ingredients, toppings, proportions and colors exactly as photographed. Do not add ingredients. Do not redesign the product.\n\nProfessional food photography, commercial restaurant advertising, ultra realistic, premium presentation.\n\nEnhance natural texture of the burger, fresh melted cheese, juicy meat appearance, and soft bun texture. Improve lighting with soft studio lighting while maintaining realism.\n\nFresh sandwich with natural color and texture. Natural highlights and shadows.\n\nDark neutral background, shallow depth of field, DSLR photography, premium advertising, restaurant menu quality.\n\nCenter composition, product occupying 80-90% of the frame, clean     "flux_negative_prompt":"cartoon, CGI, fake fruit, plastic fruit, artificial appearance, extra ingredients, duplicated toppings, unrealistic shine, melted appearance, oversaturated colors, low quality, blur"flux_negative_prompt":"cartoon, CGI, fake fruit, plastic fruit, artificial appearance, extra ingredients, duplicated toppings, unrealistic shine, melted appearance, oversaturated colors, low quality, blurprofessional presentation, food magazine quality, ultra photorealistic, 8k.\n\nRemove visual distractions, remove clutter, remove amateur lighting, remove blur, remove noise, remove harsh flash reflections."

---

## 🏗️ Arquitetura do Sistema e Pipeline de Dados
O ecossistema é dividido em uma arquitetura desacoplada (Backend API e Frontend de Prototipagem Rápida) operando de forma linear através de camadas especializadas:

*   **Camada de Percepção e Guardrail (RT-DETR):** O input do usuário (imagem) é interceptado por um modelo de Visão Computacional de tempo real executado localmente. Se o objeto detectado não pertencer à classe gastronômica permitida, a requisição é abortada na borda, economizando processamento e custos de API.
*   **Camada de Orquestração Semântica (Agente LLM - Gemini):** Uma vez validado, os metadados das classes detectadas são injetados em um agente especialista em Engenharia de Prompt Gastronômico, que traduz inputs amadores em descrições comerciais hiper-realistas de alta fidelidade.
*   **Camada de Geração Visual (Modelos de Difusão - FLUX):** O prompt otimizado alimenta o modelo de fundação visual para a renderização final do produto comercial.

---

## 🛡️ Destaques Técnicos e Padrões de Projeto (Design Patterns)

*   **AI Guardrails:** Implementação de regras de segurança rígidas na camada de entrada utilizando `ultralytics` (RT-DETR). O sistema autogerencia threads de CPU (`torch.set_num_threads(1)`) e memória através do modo de inferência otimizado `@torch.inference_mode()` para garantir performance concorrente estável no ambiente web.
*   **Graceful Degradation (Fallback Automático):**
    *   **No Prompting:** Caso a API do Gemini sofra timeout ou indisponibilidade, o backend intercepta a exceção e activa um mapeamento estático local heurístico para manter a geração ativa.
    *   **Na Geração:** Caso o provedor de nuvem principal (Replicate/Flux Pro) atinja limites de cota ou créditos, o pipeline rotaciona dinamicamente a requisição para a API aberta do Pollinations AI, garantindo Alta Disponibilidade (HA) ao usuário final.
*   **Desacoplamento de Serviços:** Toda a lógica de comunicação externa e tratamento de streams de bytes HTTP foi isolada em camadas de serviços (`services.py`), blindando os controladores do framework web (`views.py`).

---

## 🛠️ Tecnologias Utilizadas

### Backend (API & AI Pipeline)
*   Python 3.10+
*   Django & Django REST Framework (DRF)
*   PyTorch / Ultralytics (Modelo Real-Time DEtection TRansformer - RT-DETR)
*   Google GenAI SDK (Modelos `gemini-2.5-flash`)
*   Replicate API / Pollinations AI Gateway

### Frontend (Interface de Operações)
*   Streamlit (Interface ágil integrada para validação de protótipos de P&D)
*   Requests / Pillow (Manipulação e transmissão de I/O de imagem em buffers de memória)

---

## 🚀 Como Executar o Projeto

### 1. Clonar o Repositório e Configurar o Ambiente
```bash
git clone [https://github.com/seu-usuario/food-premium-ai-pipeline.git](https://github.com/seu-usuario/food-premium-ai-pipeline.git)
cd food-premium-ai-pipeline/backend
python3 manage.py runserver 8001
cd ../frontend
streamlit run app.py




