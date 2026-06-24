DETALHES_TEXTURA_ALIMENTOS = {'sandwich': 'Enhance natural texture of the burger, fresh melted cheese, juicy meat appearance, and soft bun texture.',
    'burger': 'Enhance natural texture of the burger, fresh melted cheese, juicy meat appearance, and soft bun texture.',
    'pizza': 'Enhance natural texture of the pizza crust, bubbly melted cheese, vibrant tomato sauce, and glistening toppings.',
    'hot dog': 'Enhance sausage texture, soft bun detail, and glossy sauce/condiments shine.',
    'cake': 'Enhance rich cake texture, creamy frosting detail, fluffy layers, and sweet syrup shine.',
    'ice cream': 'Enhance creamy ice cream consistency, smooth texture, and rich topping details.',
    'donut': 'Enhance soft dough texture, glossy glaze shine, and crunchy sprinkle details.',
    'soup': 'Enhance rich broth consistency, fresh vegetable detail, and natural steam warmth.',
    'salad': 'Enhance crisp leaf texture, fresh fruit/vegetable appearance, and glossy dressing shine.',
    'sushi': 'Enhance fresh fish texture, glistening glaze, and distinct rice grain details.',
}

def gerar_prompt2(detected_food):
    main_food = detected_food[0] if detected_food else "food dish"

    especific_details = DETALHES_TEXTURA_ALIMENTOS.get(main_food, f"Enhance natural texture of the {main_food}, fresh ingredients appearance, and natural food shine.")
    ingredientes_str = ", ".join(detected_food)

    prompt = f"""Transform this amateur {main_food} photo into premium iFood-style food photography.

Preserve the original {main_food} layout, ingredients, toppings, proportions and colors exactly as photographed. Do not add ingredients. Do not redesign the product.

Professional food photography, commercial restaurant advertising, ultra realistic, premium presentation.

{especific_details} Improve lighting with soft studio lighting while maintaining realism.

Fresh {ingredientes_str} with natural color and texture. Natural highlights and shadows.

Dark neutral background, shallow depth of field, DSLR photography, premium advertising, restaurant menu quality.

Center composition, product occupying 80-90% of the frame, clean professional presentation, food magazine quality, ultra photorealistic, 8k.

Remove visual distractions, remove clutter, remove amateur lighting, remove blur, remove noise, remove harsh flash reflections."""

    negative_prompt = """cartoon, CGI, fake fruit, plastic fruit, artificial appearance, extra ingredients, duplicated toppings, unrealistic shine, melted appearance, oversaturated colors, low quality, blur, watermark, logo, text, AI artifacts."""

    return prompt, negative_prompt

