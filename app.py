import cv2
import mediapipe as mp
import gradio as gr
import time
import utils # !!!

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=1
)

last_api_call_time = 0
last_gesture = "Bilinmiyor"
cached_response = "Kameraya bir hareket yapın..."
COOLDOWN_SECONDS = 5.0

def process_pipeline(image):
    global last_api_call_time, last_gesture, cached_response

    # mirror the image
    image = cv2.flip(image, 1)
    
    # BGR -> RGB Dönüşümü (MediaPipe için)
    image.flags.writeable = False
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    results = hands.process(image_rgb)
    
    image.flags.writeable = True
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    
    current_gesture = "El Yok"
    
    # Eğer el tespit edildiyse
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            
            # hand skeleton
            mp_drawing.draw_landmarks(
                image_bgr,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

            # ----- RULE BASED CLASSIFICATION OF GESTURES -----
            fingers = utils.count_fingers(hand_landmarks)

            if fingers == 0: current_gesture= "Yumruk (Rock)"
            elif fingers == 1: current_gesture= "Isaret (Point)"
            elif fingers == 2: current_gesture= "Baris (Peace)"
            elif fingers == 5: current_gesture= "Selam (Hello)"
            else : current_gesture = f"{fingers} Parmak"
            

            cv2.putText(image_bgr, f"Tespit: {current_gesture}", (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
    # ----- LLM COOLDOWN AND EVENT DRIVEN LOGIC -----

    current_time = time.time()
    if current_gesture != "El Yok":
        if (current_gesture != last_gesture) or (current_time - last_api_call_time > COOLDOWN_SECONDS):

            print(f"LLM isteği gönderiliyor... {current_gesture}")
            cached_response = utils.get_llm_response(current_gesture)

            last_gesture = current_gesture
            last_api_call_time = current_time

    final_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)    #gradio için

    return final_image, cached_response


custom_css = """
textarea {
    font-size: 12px !important;
    line-height: 2.0 !important;
    font-family: 'Arial', sans-serif;
    font-weight: bold;
}
"""

with gr.Interface(
    fn=process_pipeline,
    inputs=gr.Image(sources=["webcam"], streaming=True, type="numpy"),
    outputs=[
        gr.Image(label="Vision Feed"), 
        gr.Textbox(label="AI Response (Real-Time)")
    ],
    live=True,
    title="Beyond Text: Yapay Zekâya Göz Kazandırmak",
    description="Python, MediaPipe ve LLM kullanarak el hareketlerini anlayan yapay zeka.",
    css=custom_css
) as demo:
    demo.launch()
