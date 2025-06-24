
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from lens_schema import LensRequest, LensResponse
from lens_helper import generate_user_prompt, generate_system_prompt, resolve_dual_static_images
import mysql.connector
import openai
import os
import json

# === Load .env ===
load_dotenv()
client = openai.OpenAI(api_key = os.getenv("OPENAI_API_KEY"))


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
         "https://eyefit-lens-recommendation.netlify.app"
     ],                                                          # Adding Netlify frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Serve lens and coating images statically ===
app.mount("/lens_image_folder", StaticFiles(directory="lens_image_folder"), name="lens_image")


# === MySQL Connection ===
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),   # Railway requires explicit port
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# === API Route ===
@app.post("/recommend", response_model=LensResponse)
async def recommend_lens(payload: LensRequest):
    #conn = get_db_connection()
    #cursor = conn.cursor()

    try:
        """
        insert_query = 
            INSERT INTO lens_recommendation_user_data (
                name, age, contact_number, email_id, uses_glasses, consultation_freq, symptoms,
                sleep_hours, hydration, screen_time, screen_break_time,
                dark_mode, brightness, reading_time, outdoor_time,
                diagnosed_conditions, family_history
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        
        cursor.execute(insert_query, (
            payload.name,
            payload.age,
            payload.contactNumber,
            payload.emailID,
            payload.usesGlassesOrContacts,
            payload.consultationFrequency,
            json.dumps(payload.symptoms),
            payload.sleepHours,
            payload.hydrationFrequency,
            payload.screenTime,
            payload.screenBreakTime,
            payload.isScreenDarkMode,
            payload.screenBrightness,
            payload.readingTime,
            payload.outdoorTime,
            json.dumps(payload.diagnosedConditions),
            json.dumps(payload.familyHistory),
        ))
        conn.commit()
        form_id = cursor.lastrowid
        """
        user_prompt = generate_user_prompt(payload)
        system_prompt = generate_system_prompt()
        gpt_output = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7
        )
        content = gpt_output.choices[0].message.content.strip()
        try:
            result = json.loads(content)
            # fallback image logic
            lens_slug, coating_slug = resolve_dual_static_images(lens_file_name=result["lens_file_name"], coating_file_name=result["coating_file_name"])
            # Try all sources
            result["lens_image_url"] = f"https://lens-recommendation.onrender.com{lens_slug}"
            result["coating_image_url"] = f"https://lens-recommendation.onrender.com{coating_slug}"
            


        except Exception as e:
            result = {
                "lens_name": result["lens_name"],
                "lens_image_url": "https://lens-recommendation.onrender.com/lens_image_folder/Normal_Lens.jpg",
                "coating_image_url":"https://lens-recommendation.onrender.com/lens_image_folder/Blue_Light_Protection.jpg",
                "description":result["description"],
                "benefits": result["benefits"]
            }

        #### debugging
        #print(result["lens_image_url"])
        #print("================")
        #print(result["coating_image_url"])

        """insert_response = 
            INSERT INTO lens_recommendation_response (
                form_id, lens_name, description, benefits
            ) VALUES (%s, %s, %s, %s)
        
        cursor.execute(insert_response, (
            form_id,
            result['lens_name'],
            result['description'],
            result['benefits']
        ))
        conn.commit()
        """
    except Exception as e:
        return {
            "image_url": "Fail to generate image",
            "description": "Failed to generate lens recommendation.",
            "error": str(e)
        }
    """finally:
        cursor.close()
        conn.close()
"""
    return result