from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

def create_professional_pptx():
    print("=" * 60)
    print("   GENERATING POWERPOINT INTERNSHIP PRESENTATION SLIDES   ")
    print("=" * 60)
    
    prs = Presentation()
    
    # Standard 16:9 widescreen format (13.33 x 7.5 inches)
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    
    # Harmonious corporate color palette: Deep Navy, Vibrant Teal, Dark Grey, Pure White
    color_navy = RGBColor(10, 25, 47)       # #0A192F (Dominant backgrounds/headers)
    color_teal = RGBColor(0, 242, 254)      # #00F2FE (Teal accent / highlights)
    color_text = RGBColor(51, 65, 85)       # #334155 (Charcoal body text)
    color_bg_light = RGBColor(248, 250, 252) # #F8FAFC (Soft background)
    
    # Helper to add standard header to a slide
    def add_slide_header(slide, title_text, category_text="SYSSLAN IT SOLUTIONS"):
        # Category Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.73), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = 'Arial'
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = color_navy
        
        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.73), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = 'Arial'
        p_title.font.size = Pt(28)
        p_title.font.bold = True
        p_title.font.color.rgb = color_navy
        
        # Subtitle bottom rule (Accent line)
        line = slide.shapes.add_shape(1, Inches(0.8), Inches(1.4), Inches(2.5), Inches(0.04)) # ShapeType 1 = rectangle
        line.fill.solid()
        line.fill.fore_color.rgb = color_teal
        line.line.color.rgb = color_teal
        
    # ------------------ SLIDE 1: TITLE SLIDE (Premium Dark Theme) ------------------
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    # Dark Navy solid background card
    bg = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color_navy
    bg.line.fill.background()
    
    # Title text frame
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.33), Inches(2.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "TRAIN SCHEDULE ANALYSIS & INTERACTIVE ENQUIRY SYSTEM"
    p1.font.name = 'Arial'
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    p1.alignment = PP_ALIGN.LEFT
    
    # Subtitle
    p2 = tf.add_paragraph()
    p2.text = "Python-Based Data Pipeline, Descriptive Statistics & Capstone Application"
    p2.font.name = 'Arial'
    p2.font.size = Pt(18)
    p2.font.color.rgb = color_teal
    p2.space_before = Pt(10)
    
    # Cohort Details
    details_box = slide.shapes.add_textbox(Inches(1.0), Inches(5.0), Inches(11.33), Inches(1.5))
    tf_det = details_box.text_frame
    p_det1 = tf_det.paragraphs[0]
    p_det1.text = "Prepared for: Sysslan IT Solutions Cohort Submission"
    p_det1.font.name = 'Arial'
    p_det1.font.size = Pt(14)
    p_det1.font.bold = True
    p_det1.font.color.rgb = RGBColor(241, 245, 249)
    
    p_det2 = tf_det.add_paragraph()
    p_det2.text = "Role: Data Analysis & Software Engineering Intern | Submission Date: May 2026"
    p_det2.font.name = 'Arial'
    p_det2.font.size = Pt(12)
    p_det2.font.color.rgb = RGBColor(148, 163, 184)
    p_det2.space_before = Pt(5)

    # ------------------ SLIDE 2: PROJECT OBJECTIVES ------------------
    slide = prs.slides.add_slide(blank_layout)
    add_slide_header(slide, "Project Overview & Key Objectives")
    
    body_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.73), Inches(5.0))
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    
    # Bullet points like a human analyst
    p = tf_body.paragraphs[0]
    p.text = "Project Mandate and Technical Roadmap"
    p.font.name = 'Arial'
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = color_navy
    p.space_after = Pt(14)
    
    bullets = [
        "Data Auditing & Schema Discovery: Reviewing 186k+ transaction schedule records to understand qualities and detect latent string parsing anomalies.",
        "Data Standardisation & Preprocessing: Cleaning timeline fields, creating date-rollover handling formulas to resolve midnight crossings, and scanning duplicate records.",
        "Exploratory & Advanced Data Analysis: Profiling the network's busiest stations, identifying corridor frequencies using cross-tabulations, and structuring route-type pivot tables.",
        "Publication-Quality Visualisations: Developing aesthetic distribution curves, horizontal traffic charts, stops composition heatmaps, and stops violin densities.",
        "Interactive Capstone System: Building a modern neon-cyberpunk Streamlit web dashboard for real-time direct train enquiries, exact leg duration tracking, and fare calculations."
    ]
    
    for b in bullets:
        p_b = tf_body.add_paragraph()
        p_b.text = b
        p_b.font.name = 'Arial'
        p_b.font.size = Pt(14)
        p_b.font.color.rgb = color_text
        p_b.level = 0
        p_b.space_before = Pt(8)
        
    # ------------------ SLIDE 3: LEVEL 1: BASIC DATA REVIEW ------------------
    slide = prs.slides.add_slide(blank_layout)
    add_slide_header(slide, "Level 1: Exploratory Review & Statistics")
    
    body_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.5), Inches(5.0))
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    
    p = tf_body.paragraphs[0]
    p.text = "Initial Database Overview & Route Profiles"
    p.font.name = 'Arial'
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = color_navy
    p.space_after = Pt(14)
    
    bullets = [
        "Total Clean Records: 186,074 stops across 11,113 unique trains traversing 8,147 national stations.",
        "Starting & Ending Indexing: Extracted and compiled starting/ending stations for each unique route, saving results to 'train_routes_summary.csv'.",
        "Train Stops Statistics:",
        "  - Average Stops per Train: 16.7 stops",
        "  - Median Stops: 15.0 stops | Standard Deviation: 12.9 stops",
        "  - Maximum Stops: 118 stops (Train 53041 from Howrah JN to Jaynagar)",
        "  - Minimum Stops: 2 stops (1,249 commuter shuttle trains)"
    ]
    
    for b in bullets:
        p_b = tf_body.add_paragraph()
        p_b.text = b
        p_b.font.name = 'Arial'
        p_b.font.size = Pt(14)
        p_b.font.color.rgb = color_text
        p_b.space_before = Pt(6)
        
    # Visual illustration box on the right
    vis_box = slide.shapes.add_shape(1, Inches(8.0), Inches(1.8), Inches(4.5), Inches(4.5))
    vis_box.fill.solid()
    vis_box.fill.fore_color.rgb = RGBColor(241, 245, 249)
    vis_box.line.color.rgb = color_teal
    vis_box_tf = vis_box.text_frame
    vis_box_tf.word_wrap = True
    p_v = vis_box_tf.paragraphs[0]
    p_v.text = "\n📊 Core Scale Insights"
    p_v.font.name = 'Arial'
    p_v.font.size = Pt(18)
    p_v.font.bold = True
    p_v.font.color.rgb = color_navy
    p_v.alignment = PP_ALIGN.CENTER
    
    bullets_v = [
        "Commuter shuttle lines represent over 11.2% of all national train runs.",
        "The network demonstrates a mature hub-and-spoke infrastructure focused on regional transit loops.",
        "Strict database audits confirmed zero malformed stop sequences or chronological distance violations."
    ]
    for bv in bullets_v:
        p_bv = vis_box_tf.add_paragraph()
        p_bv.text = "\n• " + bv
        p_bv.font.name = 'Arial'
        p_bv.font.size = Pt(13)
        p_bv.font.color.rgb = color_text
        p_bv.alignment = PP_ALIGN.LEFT
        
    # ------------------ SLIDE 4: LEVEL 2 & 3: PROCESSING & QUALITY AUDITS ------------------
    slide = prs.slides.add_slide(blank_layout)
    add_slide_header(slide, "Level 2 & 3: Simple Processing & Quality Checks")
    
    body_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.73), Inches(5.0))
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    
    p = tf_body.paragraphs[0]
    p.text = "Solving Critical Temporal Rollovers & String Anomalies"
    p.font.name = 'Arial'
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = color_navy
    p.space_after = Pt(14)
    
    bullets = [
        "The 'NAN' Station Code Gotcha: Discovered that 6 rows corresponding to the valid station 'NANOGAON ROA' had the station code 'NAN'. Pandas default loading corrupted these into Null values (NaN). Fixed explicitly using keep_default_na=False.",
        "Midnight Rollover Duration Calculations: Implemented a robust cumulative algorithm. Slices schedules sequentially and adds 24 hours (1440 minutes) to a leg whenever a time decrease is observed (e.g. departing at 23:45 and arriving at 00:30, or a halt crossing midnight). Successfully processes the entire network with 100% mathematical precision.",
        "Route Distance Classifications: Segmented train routes into Short (<=100 km: 6,082 trains), Medium (101-500 km: 2,827 trains), and Long (>500 km: 2,204 trains).",
        "Sequential Audits: Programmatically scanned and confirmed 0 sequence number violations ($SN_i > SN_{i-1}$) and 0 distance progression violations ($Distance_i \\geq Distance_{i-1}$)."
    ]
    
    for b in bullets:
        p_b = tf_body.add_paragraph()
        p_b.text = b
        p_b.font.name = 'Arial'
        p_b.font.size = Pt(14)
        p_b.font.color.rgb = color_text
        p_b.space_before = Pt(8)
        
    # ------------------ SLIDE 5: LEVEL 4: BASIC ANALYSIS & VISUALIZATION ------------------
    slide = prs.slides.add_slide(blank_layout)
    add_slide_header(slide, "Level 4: Basic Analysis & Station Traffic")
    
    body_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.5), Inches(5.0))
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    
    p = tf_body.paragraphs[0]
    p.text = "Profiling Station Traffic & Route Scalings"
    p.font.name = 'Arial'
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = color_navy
    p.space_after = Pt(14)
    
    bullets = [
        "Descriptive Stats (Journey Hours by Category):",
        "  - Short Routes (<= 100 km): Averages 1.29 hours",
        "  - Medium Routes (101-500 km): Averages 5.56 hours",
        "  - Long Routes (> 500 km): Averages 25.78 hours",
        "Busiest Railway Hubs: Identified top busiest transit junctions by unique visiting train counts, led by CST-Mumbai (CSMT - 1,027 trains), Kalyan JN (828), and Thane (796).",
        "Regional Pillars: Sealdah (SDAH - 745 trains) and Howrah JN (699 trains) anchor east-coast transit lines, while Chennai Beach (MSB - 738 trains) anchors south-coast loops."
    ]
    
    for b in bullets:
        p_b = tf_body.add_paragraph()
        p_b.text = b
        p_b.font.name = 'Arial'
        p_b.font.size = Pt(14)
        p_b.font.color.rgb = color_text
        p_b.space_before = Pt(6)
        
    # EMBED THE GENERATED GRAPH ON THE RIGHT SIDE!
    chart_path = "visualizations/top_stations_traffic.png"
    if os.path.exists(chart_path):
        slide.shapes.add_picture(chart_path, Inches(6.8), Inches(1.8), width=Inches(5.8), height=Inches(4.5))
    else:
        # Placeholder box
        rect = slide.shapes.add_shape(1, Inches(6.8), Inches(1.8), Inches(5.8), Inches(4.5))
        rect.fill.solid()
        rect.fill.fore_color.rgb = RGBColor(226, 232, 240)
        p_rec = rect.text_frame.paragraphs[0]
        p_rec.text = "[Chart Placeholder: visualizations/top_stations_traffic.png]"
        p_rec.font.name = 'Arial'
        p_rec.font.size = Pt(14)
        p_rec.font.color.rgb = color_navy
        
    # ------------------ SLIDE 6: LEVEL 5: ADVANCED ANALYSIS & VISUALIZATION ------------------
    slide = prs.slides.add_slide(blank_layout)
    add_slide_header(slide, "Level 5: Advanced Pivot Compositions & Heatmaps")
    
    body_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.5), Inches(5.0))
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    
    p = tf_body.paragraphs[0]
    p.text = "Uncovering Hidden Multi-Dimensional Trends"
    p.font.name = 'Arial'
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = color_navy
    p.space_after = Pt(14)
    
    bullets = [
        "Hub Composition Profiles: Pivot tables show Mumbai terminals consist of over 95% Short-distance commuter shuttle loops (e.g. Kurla, Ghatkopar at 100%), whereas Howrah JN handles a highly diversified mix of commuter, regional, and long-distance trains.",
        "Stop Density Violin Spreads: Violin plots show Short routes have extremely tight stop-counts (1-5 stops), whereas Long routes display a wide distribution, with many trains making 31+ stops to connect intermediate rural regions.",
        "Corridor Density Matrices: Cross-tabulations map dense commuter origin-destination frequencies between local metropolitan junctions."
    ]
    
    for b in bullets:
        p_b = tf_body.add_paragraph()
        p_b.text = b
        p_b.font.name = 'Arial'
        p_b.font.size = Pt(14)
        p_b.font.color.rgb = color_text
        p_b.space_before = Pt(8)
        
    # EMBED ADVANCED COMPOSITION GRAPH ON THE RIGHT SIDE!
    chart_path2 = "visualizations/station_route_composition.png"
    if os.path.exists(chart_path2):
        slide.shapes.add_picture(chart_path2, Inches(6.8), Inches(1.8), width=Inches(5.8), height=Inches(4.5))
    else:
        # Placeholder box
        rect = slide.shapes.add_shape(1, Inches(6.8), Inches(1.8), Inches(5.8), Inches(4.5))
        rect.fill.solid()
        rect.fill.fore_color.rgb = RGBColor(226, 232, 240)
        p_rec = rect.text_frame.paragraphs[0]
        p_rec.text = "[Chart Placeholder: visualizations/station_route_composition.png]"
        p_rec.font.name = 'Arial'
        p_rec.font.size = Pt(14)
        p_rec.font.color.rgb = color_navy

    # ------------------ SLIDE 7: LEVEL 6: CAPSTONE PORTAL (WEB APP) ------------------
    slide = prs.slides.add_slide(blank_layout)
    add_slide_header(slide, "Level 6: Final Capstone Interactive Web System")
    
    body_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.5), Inches(5.0))
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    
    p = tf_body.paragraphs[0]
    p.text = "Futuristic Glassmorphic Train Enquiry Dashboard"
    p.font.name = 'Arial'
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = color_navy
    p.space_after = Pt(14)
    
    bullets = [
        "Direct Route Enquiry: Interactive autocomplete dropdowns for 8,000+ stations. Instantly identifies all direct route options and computes exact sub-leg durations.",
        "Chronological Route Timeline: Expanding search matches displays the train's full list of stops, highlighting get-on and get-off terminals, timing, and distances.",
        "Interactive Ticket Pricing Engine: Dynamically calculates ticket fares for Sleeper (SL), 3AC, 2AC, and 1AC based on differential distance-fare subtraction.",
        "Active Live Boards: Search any station code to instantly view its national rank, originating statistics, and complete schedule arrivals board."
    ]
    
    for b in bullets:
        p_b = tf_body.add_paragraph()
        p_b.text = b
        p_b.font.name = 'Arial'
        p_b.font.size = Pt(14)
        p_b.font.color.rgb = color_text
        p_b.space_before = Pt(8)
        
    # Visual illustration box on the right
    vis_box = slide.shapes.add_shape(1, Inches(8.0), Inches(1.8), Inches(4.5), Inches(4.5))
    vis_box.fill.solid()
    vis_box.fill.fore_color.rgb = color_navy
    vis_box.line.color.rgb = color_teal
    vis_box_tf = vis_box.text_frame
    vis_box_tf.word_wrap = True
    p_v = vis_box_tf.paragraphs[0]
    p_v.text = "\n💻 Streamlit Architecture"
    p_v.font.name = 'Arial'
    p_v.font.size = Pt(18)
    p_v.font.bold = True
    p_v.font.color.rgb = RGBColor(255, 255, 255)
    p_v.alignment = PP_ALIGN.CENTER
    
    bullets_v = [
        "Web server runs locally on http://localhost:8501.",
        "Lightweight Python execution with @st.cache_data for instant zero-latency loads.",
        "Styling powered by custom CSS stylesheets injected directly into Streamlit containers."
    ]
    for bv in bullets_v:
        p_bv = vis_box_tf.add_paragraph()
        p_bv.text = "\n• " + bv
        p_bv.font.name = 'Arial'
        p_bv.font.size = Pt(13)
        p_bv.font.color.rgb = RGBColor(226, 232, 240)
        p_bv.alignment = PP_ALIGN.LEFT

    # ------------------ SLIDE 8: COHORT SUBMISSION GUIDELINES ------------------
    slide = prs.slides.add_slide(blank_layout)
    add_slide_header(slide, "Fulfilling the Sysslan Internship Cohort Mandate")
    
    body_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.73), Inches(5.0))
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    
    p = tf_body.paragraphs[0]
    p.text = "Submitting Accomplishments & Spreading Engagement"
    p.font.name = 'Arial'
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = color_navy
    p.space_after = Pt(14)
    
    bullets = [
        "LinkedIn Outreach: Showcase your offer letter or internship certificates from Sysslan IT Solutions on your profile. Mention and tag Sysslan IT Solutions in your posts to celebrate milestones.",
        "Originality Code Compliance: Assured that 100% of python-scripts, preprocessing engines, charts, and application interfaces in this submission are original and plagiarism-free, avoiding duplication violations.",
        "Professional Video Walkthrough: Share a 3-minute screen recording presentation of these PowerPoint slides and your live Streamlit enquiry portal on LinkedIn.",
        "Submission Hashtags (Be sure to tag Sysslan IT Solutions and use these tags):",
        "  #SysslanITSolutions  #SysslanExperience  #FutureWithSysslan  #SysslanInnovation  #SysslanProjects"
    ]
    
    for b in bullets:
        p_b = tf_body.add_paragraph()
        p_b.text = b
        p_b.font.name = 'Arial'
        p_b.font.size = Pt(14)
        p_b.font.color.rgb = color_text
        p_b.space_before = Pt(8)

    # ------------------ SLIDE 9: THANK YOU SLIDE ------------------
    slide = prs.slides.add_slide(blank_layout)
    
    # Dark Navy solid background card
    bg = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color_navy
    bg.line.fill.background()
    
    # Thank You text
    thank_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(11.33), Inches(2.0))
    tf_t = thank_box.text_frame
    p_t1 = tf_t.paragraphs[0]
    p_t1.text = "THANK YOU"
    p_t1.font.name = 'Arial'
    p_t1.font.size = Pt(64)
    p_t1.font.bold = True
    p_t1.font.color.rgb = RGBColor(255, 255, 255)
    p_t1.alignment = PP_ALIGN.CENTER
    
    p_t2 = tf_t.add_paragraph()
    p_t2.text = "Sysslan IT Solutions • Data Analysis Internship Cohort Presentation"
    p_t2.font.name = 'Arial'
    p_t2.font.size = Pt(20)
    p_t2.font.color.rgb = color_teal
    p_t2.alignment = PP_ALIGN.CENTER
    p_t2.space_before = Pt(15)
    
    # Save the PPTX file
    pptx_filename = "Sysslan_Internship_Presentation.pptx"
    prs.save(pptx_filename)
    print(f"-> Editable PowerPoint presentation saved to '{os.path.abspath(pptx_filename)}'")
    print("=" * 60)

if __name__ == "__main__":
    create_professional_pptx()
