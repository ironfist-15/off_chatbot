from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from urllib.parse import quote

import requests

class ActionSearchByCategory(Action):
    def name(self) -> str:
        return "action_search_by_category"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        category = tracker.get_slot("category")
        if not category:
            dispatcher.utter_message(text="I couldn't find a category to search with.")
            return []

        try:
            encoded_category = quote(category)
            url = f"https://world.openfoodfacts.net/api/v2/search?categories_tags_en={quote(category)}"
            response = requests.get(url)
            response.raise_for_status()  # Raises HTTPError for bad responses
            data = response.json()
            products = data.get("products", [])
            if products:
                names = [p.get("product_name", "Unnamed") for p in products[:5]]
                dispatcher.utter_message(text="Top products:\n- " + "\n- ".join(names))
            else:
                dispatcher.utter_message(text="No products found for that category.")
            print("Category received:", category)

        except Exception as e:
            dispatcher.utter_message(text=f"Error fetching products: {str(e)}")
        return []


class ActionSearchByCategoryAndGrade(Action):
    def name(self) -> str:
        return "action_search_by_category_and_grade"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        category = tracker.get_slot("category")
        grade = tracker.get_slot("grade")
        if not category or not grade:
            dispatcher.utter_message(text="Both category and grade are needed.")
            return []

        try:
            encoded_category = quote(category)
            encoded_grade = quote(grade)
            url = f"https://world.openfoodfacts.net/api/v2/search?categories_tags_en={encoded_category}&nutrition_grades_tags={encoded_grade}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            products = data.get("products", [])
            if products:
                names = [p.get("product_name", "Unnamed") for p in products[:5]]
                dispatcher.utter_message(
                    text=f"Products in '{category}' with grade '{grade}':\n- " + "\n- ".join(names)
                )
            else:
                dispatcher.utter_message(text="No matching products found.")
        except Exception as e:
            dispatcher.utter_message(text=f"Error fetching data: {str(e)}")
        return []



class ActionSearchByBarcode(Action):
    def name(self) -> str:
        return "action_search_by_barcode"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        barcode = tracker.get_slot("barcode")
        if not barcode:
            dispatcher.utter_message(text="Please provide a barcode.")
            return []

        try:
            url = f"https://world.openfoodfacts.net/api/v2/product/{barcode}"
            response = requests.get(url)
            data = response.json()
            product = data.get("product")
            if product:
                name = product.get("product_name", "Unnamed")
                grade = product.get("nutrition_grade_fr", "Unknown")
                dispatcher.utter_message(text=f"Product: {name}\nNutrition Grade: {grade}")
            else:
                dispatcher.utter_message(text="No product found with that barcode.")
        except Exception as e:
            dispatcher.utter_message(text=f"Error during lookup: {str(e)}")
        return []
