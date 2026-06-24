# from .prompts import gerar_prompt_premium_com_agente
# from .services import gerar_imagem_ia_flux
# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import importlib
# from PIL import Image
# import io
# import torch

# torch.set_num_threads(1)
# try:
#     ultralytics_module = importlib.import_module("ultralytics")
#     RTDETR = getattr(ultralytics_module, "RTDETR")
# except (ImportError, AttributeError) as err:
#     raise ImportError(
#         "Unable to import RTDETR from ultralytics. "
#         "Install the ultralytics package and ensure /it exposes RTDETR."
#     ) from err


# # Create your views here.
# print("Carregando modelo RT-DETR comercial...")
# MODELO_DETECCAO = RTDETR("rtdetr-l.pt")

# CLASS_FOOD_ALLOWED ={
#     'sandwich', 'sandwich', 'bakery', 'fast food', 'pizza', 'burger', 
#     'hot dog', 'ice cream', 'cake', 'donut', 'soup', 'salad', 'sushi', 
#     'broccoli', 'carrot', 'apple', 'banana', 'orange', 'bowl'
# }

# class ValidateFoodView(APIView):
#     @torch.inference_mode()
#     def post(self, request, *args, **kwargs):
#         if 'image' not in request.FILES:
#             return Response(
#                 {"erro":"Nenhuma imagem foi enviada no campo imagnes"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         file_image = request.FILES['image']
#         try:
#             image_pil = Image.open(io.BytesIO(file_image.read())).convert("RGB")
#             results = MODELO_DETECCAO(image_pil, conf=0.25, verbose=False)

#             objetos_detectados = []
#             e_food = False

#             for result in results:
#                 if result.boxes is None or len(result.boxes)== 0:
#                     continue
#                 names_class = result.names

#                 ids_detected = result.boxes.cls.cpu().int().tolist()
                
#                 for id_class in ids_detected:
#                     name_class = names_class[id_class]
#                     if name_class not in objetos_detectados:
#                         objetos_detectados.append(name_class)
#                     if name_class in CLASS_FOOD_ALLOWED:
#                         e_food = True
             
#             if not e_food:
#                 return Response({
#                     "valid": False,
#                     "mensage":"imagem rejeitada o sistema identificou a imagem como nao pertencente a classe de comida",
#                     "detectd":objetos_detectados
#                     }, status=status.HTTP_400_BAD_REQUEST)            
#             prompt_final, negative_final = gerar_prompt_premium_com_agente(objetos_detectados)
#             return Response({
#                     "valid":True,
#                     "message":"Imagem Vlidada com sucesso",
#                     "flux_prompt":prompt_final,
#                     "flux_negative_prompt":negative_final,
#                     "detectd":objetos_detectados
#             },status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"erro": f"falha ao processar a imagem:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import importlib
from PIL import Image
import io
import torch

# IMPORTAÇÕES DOS NOSSOS AGENTES ISOLADOS:
from .prompts import gerar_prompt_premium_com_agente
from .services import gerar_imagem_ia_flux

# Força o PyTorch a rodar em uma única thread por requisição na CPU (Evita travamentos)
torch.set_num_threads(1)

try:
    ultralytics_module = importlib.import_module("ultralytics")
    RTDETR = getattr(ultralytics_module, "RTDETR")
except (ImportError, AttributeError) as err:
    raise ImportError(
        "Unable to import RTDETR from ultralytics. "
        "Install the ultralytics package and ensure it exposes RTDETR."
    ) from err

print("Carregando modelo RT-DETR comercial...")
MODELO_DETECCAO = RTDETR("rtdetr-l.pt")

CLASS_FOOD_ALLOWED = {
    'sandwich', 'bakery', 'fast food', 'pizza', 'burger', 
    'hot dog', 'ice cream', 'cake', 'donut', 'soup', 'salad', 'sushi', 
    'broccoli', 'carrot', 'apple', 'banana', 'orange', 'bowl'
}

class ValidateFoodView(APIView):
    
    @torch.inference_mode()
    def post(self, request, *args, **kwargs):
        if 'image' not in request.FILES:
            return Response(
                {"erro": "Nenhuma imagem foi enviada no campo 'image'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file_image = request.FILES['image']
        
        try:
            if not file_image.content_type.startswith('image/'):
                return Response(
                    {"erro": "O arquivo enviado nao e uma imagem valida."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            dados_da_imagem = file_image.read()
            if not dados_da_imagem:
                return Response(
                    {"erro": "Arquivo de imagem vazio ou corrompido."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                image_pil = Image.open(io.BytesIO(dados_da_imagem))
                image_pil.verify()
                image_pil = Image.open(io.BytesIO(dados_da_imagem)).convert("RGB")
            except Exception:
                return Response(
                    {"erro": "Imagem corrompida ou formato nao suportado (Use JPG ou PNG)."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 1. Executa a inferência do Detector de Objetos (RT-DETR)
            results = MODELO_DETECCAO(image_pil, conf=0.25, verbose=False)

            objetos_detectados = []
            e_food = False

            for result in results:
                if result.boxes is None or len(result.boxes) == 0:
                    continue
                
                names_class = result.names
                ids_detected = result.boxes.cls.cpu().int().tolist()
                
                for id_class in ids_detected:
                    name_class = names_class[id_class]
                    if name_class not in objetos_detectados:
                        objetos_detectados.append(name_class)
                    if name_class in CLASS_FOOD_ALLOWED:
                        e_food = True

            if not e_food:
                return Response({
                    "valid": False,
                    "message": "Imagem rejeitada. O sistema identificou a imagem como nao pertencente a classe de comida.",
                    "detected": objetos_detectados
                }, status=status.HTTP_400_BAD_REQUEST)            
            
            # --- PIPELINE DE IA CONECTADO AQUI ---
            
            # 2. O Agente de Prompt (Gemini) analisa as classes e cria a engenharia de prompt premium
            prompt_final, negative_final = gerar_prompt_premium_com_agente(objetos_detectados)
            
            # 3. O Agente de Geração (Flux) recebe o prompt e faz a requisição HTTP real para a API do Replicate
            url_imagem_gerada = gerar_imagem_ia_flux(prompt_final, negative_final)
            
            # 4. Resposta Final da nossa Super API: Retorna a URL real gerada pelo Flux!
            return Response({
                "valid": True,
                "message": "Imagem Validada e gerada com sucesso pelo Flux!",
                "detected": objetos_detectados,
                "input_prompt_used": prompt_final,
                "result_image_url": url_imagem_gerada  # ◄── A URL FINAL ENTRA AQUI
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"erro": f"falha interna ao processar a imagem: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )