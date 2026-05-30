from django.shortcuts import render

import google.generativeai as genai

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from cars.models import Car

from .models import AIQuestion


# Create your views here.

class GeminiCarAssistantView(APIView):
    permission_classes=[AllowAny]
    
    def post(self, request):
        user_message=request.data.get("message")
        
        if not user_message:
            return Response(
                {"error": "Message is required"},
                status=400
            )
            
        cars=Car.objects.filter(is_available=True).select_related(
            "origin_country"
        )[:20]
        
        car_context=""

        for car in cars:
            import_info=getattr(car, "import_info", None)

            import_cost=(
                import_info.estimated_import_cost
                if import_info
                else "Non défini"
            )
            
            import_days=(
                import_info.estimated_import_days
                if import_info
                else "Non défini"
            )
            
            car_context += f"""
Voiture:
-ID:{car.id}
-Marque:{car.brand}
-Modèle: {car.model}
-Année: {car.year}
-Prix Voiture: {car.price}$
-Pays d'origine:{car.origin_country.name}
-Type de course:{car.race_type}
-Puissance : {car.power_hp}HP
-kilométrage: {car.mileage}Km
-Etat:{car.conditions}
-Transmission:{car.transmission}
-Carburant:{car.fuel}
-Frais import estimés:{import_cost}$
-Délai import estimé:{import_days} jours
"""

        if not car_context:
                car_context = "Aucune voiture disponible actuellement."
                
        prompt=f"""
Tu es un assistant expert pour une plateforme d'importation de voitures de course d'occasion en Malaisie.

Tu dois conseiller les clients selon:
-budget total estimé
-type d'utilisation: circuit, drift, rallye, drag race, compétition amateur
-pays d'origine
-puissance
-état
-frais d'import
-délai d'import
-disponibilité 


Catalogue disponible : {car_context}

Question clients:{user_message}

Réponds en français de façon claire, utile et commerciale.
Si tu recommande un voiture, donne son ID, marque, modèle, prix et raison.
"""     

        ai_question=AIQuestion.objects.create(
            user=request.user if request.user.is_authenticated else None,
            question=user_message,
            answer=response.text
            
        )
        
        try: 
            genai.configure(api_key=settings.GEMINI_API_KEY)

            model=genai.GenerativeModel("gemini-2.0-flash")

            response=model.generate_content(prompt)

            return Response(
                    {"reply":response.text}
                )

        except Exception as e:
            return Response(
                {
                    "reply": "L'assistant IA est momentanément indisponible.",
                    "error": str(e)
                },
                status=503
            )