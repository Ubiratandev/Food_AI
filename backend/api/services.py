import os
import replicate

def gerar_imagem_ia_flux(prompt, negative_prompt):
    """
    Envia o prompt estruturado para a API do Replicate (Flux) 
    e retorna a URL da imagem gerada de alta qualidade.
    """
    try:
        # Pega o token automaticamente do ambiente (carregado pelo dotenv no settings.py)
        token = os.getenv("REPLICATE_API_TOKEN")
        if not token:
            raise ValueError("Token do Replicate nao encontrado no arquivo .env")

        # Inicializa o cliente do Replicate com o token
        client = replicate.Client(api_token=token)

        print(f"Enviando para o Flux. Prompt: {prompt[:60]}...")

        # Executa o modelo Flux via API
        output = client.run(
            "black-forest-labs/flux-1.1-pro",
            input={
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "aspect_ratio": "1:1",  # Formato quadrado perfeito para o feed do app
                "output_format": "jpg",
                "output_quality": 95
            }
        )

        # O Replicate costuma retornar um objeto que pode ser convertido em string (a URL direta)
        # ou uma lista contendo a URL da imagem. Tratamos os dois casos abaixo:
        if isinstance(output, list) and len(output) > 0:
            url_final = output[0]
        else:
            url_final = str(output)

        print(f"Imagem gerada com sucesso pelo Flux: {url_final}")
        return url_final

    except Exception as e:
        print(f"🚨 Erro na conexão com o Replicate/Flux: {str(e)}")
        raise RuntimeError(f"Falha na geracao de imagem pelo Flux: {str(e)}")
