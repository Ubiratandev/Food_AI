


import os
from google import genai
from google.genai import types
from .prompts2 import gerar_prompt2

def gerar_prompt_premium_com_agente(alimentos_detectados):
    """
    Agente de IA que consome a API do Gemini para transformar classes brutas
    detectadas em prompts hiper-realistas comerciais para o Flux.
    """
    try:
        # Inicializa o cliente do Gemini usando a chave do .env
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Chave GEMINI_API_KEY nao encontrada no arquivo .env")
            
        client = genai.Client(api_key=api_key)
        
        ingredientes_brutos = ", ".join(alimentos_detectados)
        
        # Engenharia de Prompt: Definimos o papel (Persona) e as regras do Agente
        system_instruction = """
        You are an expert AI Prompt Engineer specializing in commercial food photography for premium delivery apps like iFood and Uber Eats.
        Your job is to receive a list of detected food items and write a highly detailed, professional prompt in English for an image generation model (FLUX).
        
        CRITICAL RULES:
        1. Focus strictly on ultra-realistic commercial food photography (DSLR, 8k, studio lighting, restaurant quality).
        2. Describe the specific textures, appetizing details, and freshness of the detected items.
        3. If 'bowl' is detected, interpret it contextually as a premium Brazilian Açaí bowl or a rich dessert with fresh toppings (strawberries, banana, granola).
        4. If local or generic items are passed, make them look premium and artisan.
        5. DO NOT include meta-text, introductions, or explanations. Return ONLY the final prompt text.
        """
        
        prompt_usuario = f"""
        Generate a premium FLUX prompt for these detected food items: {ingredientes_brutos}.
        
        Follow this structural template:
        - Transform this amateur photo into premium iFood-style food photography of [Main Item].
        - Preserve the original layout, ingredients, and proportions exactly. Do not add random external elements.
        - Commercial restaurant advertising, ultra realistic, premium presentation.
        - [Describe the rich natural textures, cheese melt, gloss, or freshness specific to these items].
        - Soft studio lighting, dark neutral background, shallow depth of field, DSLR 8k photography.
        - Center composition, clean professional presentation, food magazine quality.
        - Remove visual distractions, remove clutter, remove amateur lighting, remove blur.
        """

        # Executa a chamada do Agente de Linguagem
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_usuario,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.4, # Temperatura mais baixa para manter o agente focado e profissional
            )
        )
        
        prompt_gerado_pela_llm = response.text.strip()
        
        # O prompt negativo padrão que você validou e que funciona muito bem
        negative_prompt = "cartoon, CGI, fake fruit, plastic appearance, extra ingredients, duplicated toppings, unrealistic shine, melted appearance, oversaturated colors, low quality, blur, watermark, logo, text, AI artifacts."
        
        return prompt_gerado_pela_llm, negative_prompt

    except Exception as e:
        print(f"Erro no Agente Gemini: {str(e)}")
        # Fallback de segurança caso a API do Gemini falhe por falta de internet/crédito
        return gerar_prompt2(alimentos_detectados);