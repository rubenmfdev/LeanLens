from openai import AzureOpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/generate-plan": {"origins": "*"}})

client = AzureOpenAI(
    api_key="YOUR_AZURE_OPENAI_API_KEY",
    api_version="2023-05-15",
    azure_endpoint="https://YOUR_OPENAI_RESOURCE_NAME.openai.azure.com/"
)

deployment_name = "gpt-4"

# === Azure Vision Setup ===
VISION_KEY = "YOUR_AZURE_VISION_API_KEY"
VISION_ENDPOINT = "https://YOUR_VISION_RESOURCE_NAME.cognitiveservices.azure.com/"
VISION_URL = VISION_ENDPOINT + "vision/v3.2/analyze?visualFeatures=Tags"

@app.route('/generate-plan', methods=['POST'])
def generate_plan():
    try:
        if "photo" not in request.files:
            return jsonify({"error": "Missing photo file"}), 400

        goal_fat = request.form.get("goal_fat")
        goal_type = request.form.get("goal_type")
        photo = request.files["photo"]

        # Step 1: Use Vision to get the tags of the photo
        vision_headers = {
            "Ocp-Apim-Subscription-Key": VISION_KEY,
            "Content-Type": "application/octet-stream"
        }

        vision_response = requests.post(
            VISION_URL,
            headers=vision_headers,
            data=photo.read()
        )

        vision_data = vision_response.json()
        print("🧠 Vision tags:", vision_data.get("tags", []))

        # Step 2: Let GPT interpret Vision tags
        tag_list = ", ".join([tag["name"] for tag in vision_data.get("tags", [])])

        fat_prompt = f"""
        You are a fitness coach. Based on these image tags: {tag_list}, estimate the person's body fat percentage. Give only the number. ONLY THE NUMBER!
        """

        fat_response = client.chat.completions.create(
            model=deployment_name,
            messages=[{"role": "user", "content": fat_prompt}],
            temperature=0.2,
            max_tokens=10
        )

        current_fat = float(fat_response.choices[0].message.content.strip())
        print("💪 Estimated fat % by GPT:", current_fat)

        # Step 3: Ask ChatGPT to generate a plan 
        prompt = f"""
        You are a certified fitness and nutrition expert. A user currently has {current_fat}% body fat and wants to reduce it to {goal_fat}% with a goal of achieving a '{goal_type}' body type.

        Please generate a personalized fat-loss plan and format the output in clean, readable HTML using headers (<h2>, <h3>), bullet points (<ul>, <li>), and paragraphs (<p>) where appropriate. Avoid Markdown.

        The plan should include:
        1. A short summary of their current state
        2. Weekly body fat loss goal
        3. Caloric intake and macronutrient split
        4. Weekly workout plan (with rest days)
        5. Estimated timeline to goal
        6. Friendly motivational tips
        """

        print(f"📝 Prompt:\n{prompt}")
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful fitness and health coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=700
        )
        ai_response = response.choices[0].message.content
        print("🧠 GPT Response:", ai_response)
        return jsonify({
            "plan": ai_response,
            "estimated_fat": current_fat
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)
