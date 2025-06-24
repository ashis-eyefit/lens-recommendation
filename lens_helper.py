import os

def resolve_dual_static_images(lens_file_name: str, coating_file_name: str):

    lens_image = f"/lens_image_folder/{lens_file_name}"
    coating_image = f"/lens_image_folder/{coating_file_name}"

    return lens_image, coating_image

## prompt generator for dynamic user prompt
def generate_user_prompt(data):
    return f"""
        User Profile:
        - User's Age: {data.age}
        - Uses Any Glasses/Contacts: {data.usesGlassesOrContacts}
        - Doctor Consultation Frequency: {data.consultationFrequency}
        - Symptoms: {', '.join(data.symptoms or ['None'])}
        - Sleep Hours Per Day: {data.sleepHours}
        - Hydration Quality: {data.hydrationFrequency}
        - Screen Time: {data.screenTime} hrs/day
        - Screen Break per hour of using screen: {data.screenBreakTime} mins
        - Screen Dark Mode: {data.isScreenDarkMode}
        - Screen Brightness Level: {data.screenBrightness}
        - User Reading Time: {data.readingTime} hrs/day
        - User Outdoor Time: {data.outdoorTime} hrs/day
        - Earlier Diagnosed Conditions: {', '.join(data.diagnosedConditions or ['None'])}
        - Family History with Diagnosed Conditions: {', '.join(data.familyHistory or ['None'])}
        """


# Fixed system prompt
def generate_system_prompt():
    return """
        You are an expert optometrist with extensive domain knowledge in lens prescription and coating technology. Based on the provided user profile, suggest the most suitable type of lens and protective coating feature.


        STATIC FILE MAPPINGS:
        Use only the filenames below — do not invent new paths or image names.
        - lens_file_name: ["Digital_Focal_Lens.jpg", "Progressive_Lens.jpg", "Bifocal_Lens.jpg", "Single_Vision_Lens.jpg", "Normal_Lens.jpg"]
        - coating_file_name: ["Achromatic.jpg", "Anti_Reflective.jpg", "Anti_Static.jpg", "Blue_Light_Protection.jpg", "Scratch_Resistant.jpg", "Super_Hydrophobic.jpg", "UV_Protection.jpg", "Driving_Lens.jpg", "Photochromic_Lens.jpg"]

        RULES:
        - Choose the most clinically suitable **lens_name** [with required coating] based on symptoms, age, screen time, vision history, and risk factors.
        - If you cannot match any known lens type, fallback to: `"lens_file_name": "Normal_Lens.jpg"`
        - If coating not clear, fallback to: `"coating_file_name": "Blue_Light_Protection.jpg"`
        - Keep image filenames exactly as shown. Case-sensitive. No spaces.
        - Make point wise output and use new line with bullet point for each section benefits and explanation.
        - return only one most prior relevant file name for each of  len_file_name and coating_file_name
        - Respond only with strict JSON — no explanations or extra text outside the code block and do not hallucinate.
        - Output Example:
            {{
            "lens_name": "Progressive Anti Reflective Lens",
            "lens_file_name": "Progressive_Lens.jpg",
            "coating_file_name": "Anti_Reflective.jpg",
            "description": "- Progressive lenses offer seamless focus at all distances 
                            - ideal for age-related focus changes.",
            "benefits": "- No need for multiple glasses
                         - Natural transition for near to far
                         - Anti-reflective coating improves night driving"
            }}
        """
