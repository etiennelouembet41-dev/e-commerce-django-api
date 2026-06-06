import google.generativeai as genai

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from cars.models import Car
from .models import AIQuestion


class GeminiCarAssistantView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_message = request.data.get("message")

        if not user_message:
            return Response(
                {"error": "Message is required"},
                status=400
            )

        cars = Car.objects.filter(is_available=True).select_related(
            "origin_country"
        ).prefetch_related(
            "import_info"
        )[:20]

        car_context = ""

        for car in cars:
            import_info = car.import_info.first()

            import_cost = (
                import_info.estimated_import_cost
                if import_info
                else "Non défini"
            )

            import_days = (
                import_info.estimated_import_days
                if import_info
                else "Non défini"
            )

            car_context += f"""
Voiture:
- ID: {car.id}
- Marque: {car.brand}
- Modèle: {car.model}
- Année: {car.year}
- Prix voiture: {car.price} MYR
- Pays d'origine: {car.origin_country.name}
- Type de course: {car.race_type}
- Puissance: {car.power_hp} HP
- Kilométrage: {car.mileage} km
- État: {car.conditions}
- Transmission: {car.transmission}
- Carburant: {car.fuel}
- Frais import estimés: {import_cost} MYR
- Délai import estimé: {import_days} jours
"""

        prompt = f"""
Tu es un assistant expert pour une plateforme d'importation de voitures de course d'occasion en Malaisie.

Tu dois conseiller les clients selon:
- budget total estimé
- type d'utilisation: circuit, drift, rallye, drag race, compétition amateur
- pays d'origine
- puissance
- état
- frais d'import
- délai d'import
- disponibilité

Catalogue disponible:
{car_context}

Question client:
{user_message}

Réponds en français, de façon claire, utile et commerciale.
Si tu recommandes une voiture, donne son ID, marque, modèle, prix et raison.
"""

        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)

            model = genai.GenerativeModel("gemini-1.5-flash")

            response = model.generate_content(prompt)

            ai_answer = response.text

        except Exception as e:
            return Response(
                {
                    "error": "Erreur lors de la génération de la réponse IA.",
                    "details": str(e)
                },
                status=500
            )

        ai_question = AIQuestion.objects.create(
            user=request.user if request.user.is_authenticated else None,
            question=user_message,
            answer=ai_answer
        )

        return Response({
            "reply": ai_answer,
            "question_id": ai_question.id
        })