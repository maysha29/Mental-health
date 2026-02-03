import gradio as gr
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import random
import os
import pickle
import platform

# ---------------------------------------------------------
# Block 1: Load Resources (Models & Assets)
# ---------------------------------------------------------
print("🚀 Loading Models and Assets...")

tuned_models = {}

try:
    if os.path.exists("mental_health_models.pkl"):
        with open("mental_health_models.pkl", "rb") as f:
            tuned_models = pickle.load(f)
        print("✅ Model loaded successfully!")
    else:
        print("⚠️ Warning: 'mental_health_models.pkl' file not found. Prediction will not work properly.")
except Exception as e:
    print(f"❌ Error loading model: {e}")

# Column definitions
dep_cols = ['Q3A', 'Q5A', 'Q10A', 'Q13A', 'Q16A', 'Q17A', 'Q21A', 'Q24A', 'Q26A', 'Q31A', 'Q34A', 'Q37A', 'Q38A', 'Q42A']
anx_cols = ['Q2A', 'Q4A', 'Q7A', 'Q9A', 'Q15A', 'Q19A', 'Q20A', 'Q23A', 'Q25A', 'Q28A', 'Q30A', 'Q36A', 'Q40A', 'Q41A']
str_cols = ['Q1A', 'Q6A', 'Q8A', 'Q11A', 'Q12A', 'Q14A', 'Q18A', 'Q22A', 'Q27A', 'Q29A', 'Q32A', 'Q33A', 'Q35A', 'Q39A']

# Helper function to get fonts safely
def get_font(size, bold=False):
    try:
        system = platform.system()
        font_path = None
        
        if system == "Windows":
            font_path = "arialbd.ttf" if bold else "arial.ttf"
        elif system == "Linux":
            font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
        elif system == "Darwin": # MacOS
            font_path = "Arial Bold.ttf" if bold else "Arial.ttf"
            
        if font_path:
             return ImageFont.truetype(font_path, size)
        else:
             return ImageFont.load_default()
    except:
        return ImageFont.load_default()

def generate_premium_report(name, age, gender, depression, anxiety, stress):
    
    # --- DESIGN CONFIGURATION ---
    width, height = 1200, 1400
    
    COLOR_PRIMARY = "#00695C"      # Deep Teal
    COLOR_ACCENT = "#00897B"       # Lighter Teal
    COLOR_BG_HEADER = "#E0F2F1"    # Very Light Teal
    COLOR_TEXT_DARK = "#263238"    # Dark Slate Grey
    COLOR_TEXT_LIGHT = "#546E7A"   # Medium Slate
    COLOR_WHITE = "#FFFFFF"
    
    COLOR_SAFE = "#2E7D32"         # Medical Green
    COLOR_WARN = "#F57C00"         # Medical Orange
    COLOR_DANGER = "#C62828"       # Medical Red
    
    img = Image.new('RGBA', (width, height), color=COLOR_WHITE)
    draw = ImageDraw.Draw(img)

    f_header_main = get_font(55, bold=True)
    f_header_sub = get_font(28, bold=False)
    f_section = get_font(24, bold=True)
    f_label = get_font(24, bold=True)
    f_val = get_font(24, bold=False)
    f_footer = get_font(20, bold=False)

    # ---------------- HEADER DESIGN ----------------
    draw.rectangle([(0, 0), (width, 160)], fill=COLOR_PRIMARY)
    
    draw.ellipse([(50, 35), (140, 125)], fill=COLOR_WHITE)
    draw.rectangle([(85, 50), (105, 110)], fill=COLOR_PRIMARY)
    draw.rectangle([(65, 70), (125, 90)], fill=COLOR_PRIMARY)

    draw.text((170, 45), "MindBuddy Diagnostics", font=f_header_main, fill=COLOR_WHITE)
    draw.text((170, 105), "AI-Powered Psychometric Assessment Report", font=f_header_sub, fill="#B2DFDB")

    date_str = pd.Timestamp.now().strftime('%d %B, %Y')
    draw.text((width-280, 110), f"Date: {date_str}", font=f_val, fill="#B2DFDB")

    # ---------------- PATIENT INFO BOX ----------------
    box_top = 200
    box_h = 140
    draw.rectangle([(50, box_top), (width-50, box_top + box_h)], fill=COLOR_BG_HEADER, outline=COLOR_ACCENT, width=2)

    draw.text((80, box_top + 20), "PATIENT NAME", font=f_label, fill=COLOR_TEXT_LIGHT)
    draw.text((600, box_top + 20), "DEMOGRAPHICS", font=f_label, fill=COLOR_TEXT_LIGHT)
    draw.text((900, box_top + 20), "CASE ID", font=f_label, fill=COLOR_TEXT_LIGHT)

    draw.text((80, box_top + 70), str(name).upper(), font=get_font(40, bold=True), fill=COLOR_TEXT_DARK)
    draw.text((600, box_top + 75), f"{int(age)} Years  |  {gender}", font=f_val, fill=COLOR_TEXT_DARK)
    draw.text((900, box_top + 75), f"MB-{random.randint(10000,99999)}", font=f_val, fill=COLOR_TEXT_DARK)

    # ---------------- RESULTS TABLE ----------------
    y_start = 400
    
    draw.text((50, 370), "CLINICAL EVALUATION METRICS", font=f_section, fill=COLOR_PRIMARY)
    draw.line([(50, 395), (width-50, 395)], fill=COLOR_ACCENT, width=2)

    draw.rectangle([(50, y_start), (width-50, y_start+50)], fill=COLOR_TEXT_DARK)
    draw.text((80, y_start+10), "PARAMETER", font=f_label, fill=COLOR_WHITE)
    draw.text((500, y_start+10), "SEVERITY SCORE", font=f_label, fill=COLOR_WHITE)
    draw.text((900, y_start+10), "RISK STATUS", font=f_label, fill=COLOR_WHITE)

    results = [("DEPRESSION", depression), ("ANXIETY", anxiety), ("STRESS", stress)]
    row_y = y_start + 50
    row_height = 130

    for i, (disorder, result) in enumerate(results):
        bg = COLOR_WHITE if i % 2 == 0 else "#F5F7F8"
        draw.rectangle([(50, row_y), (width-50, row_y+row_height)], fill=bg)
        draw.line([(50, row_y+row_height), (width-50, row_y+row_height)], fill="#CFD8DC", width=1)

        if str(result) in ['Normal', 'Mild']:
            bar_color = COLOR_SAFE
            status_text = "LOW RISK"
            fill_pct = 0.25
        elif str(result) == 'Moderate':
            bar_color = COLOR_WARN
            status_text = "MONITORING REQ."
            fill_pct = 0.55
        else:
            bar_color = COLOR_DANGER
            status_text = "HIGH RISK"
            fill_pct = 0.90

        draw.text((80, row_y+45), disorder, font=get_font(30, bold=True), fill=COLOR_TEXT_DARK)
        draw.text((500, row_y+20), str(result).upper(), font=f_label, fill=bar_color)
        
        bar_x = 500
        bar_y_pos = row_y + 60
        draw.rectangle([(bar_x, bar_y_pos), (bar_x+300, bar_y_pos+12)], fill="#CFD8DC")
        draw.rectangle([(bar_x, bar_y_pos), (bar_x+(300*fill_pct), bar_y_pos+12)], fill=bar_color)

        draw.text((900, row_y+45), status_text, font=get_font(26, bold=True), fill=bar_color)

        row_y += row_height

    # ---------------- VERIFICATION STAMP ----------------
    stamp_size = 220
    stamp_img = Image.new('RGBA', (stamp_size, stamp_size), (0,0,0,0))

    try:
        if os.path.exists("verified.png"):
            icon = Image.open("verified.png").convert("RGBA")
            icon = icon.resize((190, 190))
            stamp_img.paste(icon, (15, 15), icon)
        else:
            ds = ImageDraw.Draw(stamp_img)
            ds.ellipse([(10, 10), (210, 210)], outline=COLOR_PRIMARY, width=6)
            ds.ellipse([(20, 20), (200, 200)], outline=COLOR_PRIMARY, width=2)
            ds.text((45, 90), "CLINICALLY", font=f_label, fill=COLOR_PRIMARY)
            ds.text((55, 120), "VERIFIED", font=f_label, fill=COLOR_PRIMARY)
    except:
        pass

    rot_stamp = stamp_img.rotate(-10, expand=True)
    center_x = (width - rot_stamp.width) // 2
    pos_y = height - 400
    img.paste(rot_stamp, (center_x, pos_y), rot_stamp)

    # ---------------- FOOTER & SIGNATURE ----------------
    try:
        if os.path.exists("signature.png"):
            sig_img = Image.open("signature.png").convert("RGBA")
            sig_width = 220
            w_percent = (sig_width / float(sig_img.size[0]))
            h_size = int((float(sig_img.size[1]) * float(w_percent)))
            sig_img = sig_img.resize((sig_width, h_size))
            img.paste(sig_img, (880, 1050), sig_img)
        else:
            draw.text((900, 1100), "Signed", font=f_section, fill=COLOR_TEXT_LIGHT)
    except Exception as e:
        draw.text((900, 1100), "Signed", font=f_section, fill=COLOR_TEXT_LIGHT)

    draw.line([(850, 1150), (1100, 1150)], fill=COLOR_TEXT_DARK, width=2)
    draw.text((870, 1160), "Authorized Psychologist", font=f_val, fill=COLOR_TEXT_DARK)

    draw.rectangle([(0, height-60), (width, height)], fill=COLOR_PRIMARY)
    footer_text = "Note: This report is generated by AI (MindBuddy) for preliminary screening. Consult a professional for clinical diagnosis."
    draw.text((60, height-40), footer_text, font=f_footer, fill=COLOR_WHITE)

    return img


def smart_assessment_final(name, age, gender, *args):
    try:
        if not name or age is None:
            return None
            
        d_scaled = [int(round(x)) for x in args[0:8]]
        a_scaled = [int(round(x)) for x in args[8:16]]
        s_scaled = [int(round(x)) for x in args[16:22]]

        avg_dep, avg_anx, avg_str = np.mean(d_scaled), np.mean(a_scaled), np.mean(s_scaled)

        if not tuned_models:
            print("Model not loaded, generating dummy report based on averages.")
            def get_status(val):
                if val < 2: return "Normal"
                elif val < 4: return "Mild"
                elif val < 6: return "Moderate"
                else: return "Severe"
            return generate_premium_report(name, age, gender, get_status(avg_dep), get_status(avg_anx), get_status(avg_str))

        sample_key = 'Depression'
        X_test_base = tuned_models[sample_key]['X_test']
        
        if isinstance(X_test_base, pd.DataFrame):
            base_row = X_test_base.iloc[0].copy()
        else:
            return None

        for col in base_row.index:
            base_row[col] = 0

        if 'age' in base_row.index: base_row['age'] = age
        
        for col in dep_cols:
            if col in base_row.index: base_row[col] = int(round(avg_dep))
        for col in anx_cols:
            if col in base_row.index: base_row[col] = int(round(avg_anx))
        for col in str_cols:
            if col in base_row.index: base_row[col] = int(round(avg_str))

        input_data = base_row.values.reshape(1, -1)
        preds = {}

        for disorder in ['Depression', 'Anxiety', 'Stress']:
            model = tuned_models[disorder]['model']
            le = tuned_models[disorder]['le']
            pred_num = model.predict(input_data)[0]

            if hasattr(le, 'inverse_transform'):
                pred_class = le.inverse_transform([pred_num])[0]
            else:
                classes = ['Extremely Severe', 'Mild', 'Moderate', 'Normal', 'Severe']
                if pred_num < len(classes):
                    pred_class = classes[int(pred_num)]
                else:
                    pred_class = str(pred_num)
            
            preds[disorder] = pred_class

        return generate_premium_report(name, age, gender, preds['Depression'], preds['Anxiety'], preds['Stress'])

    except Exception as e:
        print(f"Prediction Error: {e}")
        return None


# --- GRADIO DESIGN CONFIGURATION ---
theme = gr.themes.Soft(
    primary_hue="teal", 
    secondary_hue="gray",
    font=["Roboto", "sans-serif"]
).set(
    button_primary_background_fill="#00695C",
    button_primary_background_fill_hover="#004D40",
    block_title_text_color="#00695C"
)

# Removed theme=theme from gr.Blocks to satisfy Gradio 6.0 warning
with gr.Blocks(title="MindBuddy AI") as demo:
    gr.Markdown(
        """
        # 🧠 MindBuddy AI
        ### Professional Mental Health Screening System
        Complete the assessment below to generate a **Clinically Verified Report**. (Scale: 0-7)
        """
    )

    with gr.Row():
        with gr.Column(scale=4, variant="panel"):
            gr.Markdown("### 📋 1. Patient Registration")
            
            # FIXED: Removed 'prefix_icon' which caused the error
            i_name = gr.Textbox(label="Full Name", placeholder="e.g. Maysha Tabassum")
            
            with gr.Row():
                i_age = gr.Number(label="Age", value=25, precision=0)
                i_gender = gr.Dropdown(["Male", "Female"], label="Gender", value="Female")

            gr.Markdown("---")
            gr.Markdown("### 🩺 2. Clinical Assessment (DASS-21)")

            inputs_list = []

            with gr.Accordion("Depression Scale (D)", open=True):
                inputs_list.extend([gr.Slider(0, 7, step=1, label=l) for l in [
                    "Q1: No positive feeling", "Q2: Felt down-hearted", "Q3: Life meaningless", "Q4: No initiative",
                    "Q5: Felt worthless", "Q6: Nothing to look forward", "Q7: Felt sad/depressed", "Q8: No enthusiasm"]])

            with gr.Accordion("Anxiety Scale (A)", open=False):
                inputs_list.extend([gr.Slider(0, 7, step=1, label=l) for l in [
                    "Q1: Dry mouth", "Q2: Breathing difficulty", "Q3: Trembling hands", "Q4: Panic worry",
                    "Q5: Heart racing", "Q6: Scared w/o reason", "Q7: Fear of tasks", "Q8: Choking feeling"]])

            with gr.Accordion("Stress Scale (S)", open=False):
                inputs_list.extend([gr.Slider(0, 7, step=1, label=l) for l in [
                    "Q1: Hard to wind down", "Q2: Over-reactive", "Q3: Touchy/Sensitive",
                    "Q4: Intolerant of waiting", "Q5: Nervous energy", "Q6: Agitated"]])

            btn = gr.Button("Generate Verified Report", variant="primary", size="lg")

        with gr.Column(scale=5):
            gr.Markdown("### 📄 Diagnostic Report Preview")
            gr.Markdown("_Your professional report will appear here automatically._")

            out_img = gr.Image(label="Clinical Report", type="pil", elem_id="report_out", height=800)

    all_inputs = [i_name, i_age, i_gender] + inputs_list
    btn.click(fn=smart_assessment_final, inputs=all_inputs, outputs=out_img)

if __name__ == "__main__":
    # FIXED: Moved theme here for Gradio 6.0 compatibility
    demo.launch(theme=theme)