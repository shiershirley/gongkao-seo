# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import time
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO

# 目标目录
BASE_DIR = Path("lib")
CATEGORIES = {
    "study": ["classroom teacher blackboard", "student taking notes", "study group", "online learning", "exam preparation desk"],
    "office": ["government building", "civil servant office", "professional meeting", "team collaboration", "formal office"],
    "books": ["textbooks stack", "notebook pen", "bookshelf library", "reading corner", "open book"],
    "exam": ["graduation cap", "certificate diploma", "exam hall", "success achievement", "ceremony"],
    "motivation": ["mountain sunrise", "running path", "goal achievement", "hard work", "success man"],
    "gov": ["city hall", "government building facade", "capitol building", "official building", "institutional architecture"],
    "tech": ["computer screen", "data analysis", "digital workspace", "laptop desk", "technology office"],
    "city": ["shanghai skyline", "beijing city", "urban development", "modern city", "cityscape night"],
    "writing": ["writing notes", "document签字", "paper work", "planning schedule", "calendar"],
    "nature": ["park trees", "garden path", "peaceful nature", "green trees", "outdoor study"],
    "people": ["business professional", "interview preparation", "confident person", "formal suit", "career success"],
}

# Pexels 精选图片URL (高质量、主题精准)
URLS_V18 = {
    "study": [
        ("https://images.pexels.com/photos/3070678/pexels-photo-3070678.jpeg?auto=compress&w=1920", "student_group_study"),
        ("https://images.pexels.com/photos/8613089/pexels-photo-8613089.jpeg?auto=compress&w=1920", "study_room"),
        ("https://images.pexels.com/photos/8613108/pexels-photo-8613108.jpeg?auto=compress&w=1920", "study_lamp"),
        ("https://images.pexels.com/photos/590493/pexels-photo-590493.jpeg?auto=compress&w=1920", "desk_workspace"),
        ("https://images.pexels.com/photos/159711/books-bookstore-book-reading-159711.jpeg?auto=compress&w=1920", "reading_book"),
        ("https://images.pexels.com/photos/1261180/pexels-photo-1261180.jpeg?auto=compress&w=1920", "library_study"),
        ("https://images.pexels.com/photos/159755/laptop-office-desk-work-159755.jpeg?auto=compress&w=1920", "laptop_study"),
        ("https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&w=1920", "team_meeting_1"),
        ("https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&w=1920", "team_meeting_2"),
        ("https://images.pexels.com/photos/3184418/pexels-photo-3184418.jpeg?auto=compress&w=1920", "office_work_1"),
        ("https://images.pexels.com/photos/3807517/pexels-photo-3807517.jpeg?auto=compress&w=1920", "education_class"),
        ("https://images.pexels.com/photos/5211438/pexels-photo-5211438.jpeg?auto=compress&w=1920", "online_class"),
        ("https://images.pexels.com/photos/5082579/pexels-photo-5082579.jpeg?auto=compress&w=1920", "video_conference"),
        ("https://images.pexels.com/photos/5212338/pexels-photo-5212338.jpeg?auto=compress&w=1920", "student_computer"),
        ("https://images.pexels.com/photos/5699657/pexels-photo-5699657.jpeg?auto=compress&w=1920", "work_from_home"),
        ("https://images.pexels.com/photos/5077047/pexels-photo-5077047.jpeg?auto=compress&w=1920", "student_books"),
        ("https://images.pexels.com/photos/4259140/pexels-photo-4259140.jpeg?auto=compress&w=1920", "reading_glasses"),
        ("https://images.pexels.com/photos/4050315/pexels-photo-4050315.jpeg?auto=compress&w=1920", "study_time"),
        ("https://images.pexels.com/photos/3803514/pexels-photo-3803514.jpeg?auto=compress&w=1920", "library_hall"),
        ("https://images.pexels.com/photos/4947288/pexels-photo-4947288.jpeg?auto=compress&w=1920", "school_building"),
    ],
    "office": [
        ("https://images.pexels.com/photos/7129713/pexels-photo-7129713.jpeg?auto=compress&w=1920", "business_meeting"),
        ("https://images.pexels.com/photos/7129716/pexels-photo-7129716.jpeg?auto=compress&w=1920", "office_work"),
        ("https://images.pexels.com/photos/7129720/pexels-photo-7129720.jpeg?auto=compress&w=1920", "formal_presentation"),
        ("https://images.pexels.com/photos/7663448/pexels-photo-7663448.jpeg?auto=compress&w=1920", "office_desk"),
        ("https://images.pexels.com/photos/7693747/pexels-photo-7693747.jpeg?auto=compress&w=1920", "business_presentation"),
        ("https://images.pexels.com/photos/7176326/pexels-photo-7176326.jpeg?auto=compress&w=1920", "formal_office"),
        ("https://images.pexels.com/photos/7176331/pexels-photo-7176331.jpeg?auto=compress&w=1920", "team_work"),
        ("https://images.pexels.com/photos/7176334/pexels-photo-7176334.jpeg?auto=compress&w=1920", "office_corridor"),
        ("https://images.pexels.com/photos/7176319/pexels-photo-7176319.jpeg?auto=compress&w=1920", "business_center"),
        ("https://images.pexels.com/photos/7176323/pexels-photo-7176323.jpeg?auto=compress&w=1920", "modern_office"),
        ("https://images.pexels.com/photos/7651303/pexels-photo-7651303.jpeg?auto=compress&w=1920", "corporate_meeting"),
        ("https://images.pexels.com/photos/7651294/pexels-photo-7651294.jpeg?auto=compress&w=1920", "office_window"),
        ("https://images.pexels.com/photos/7651289/pexels-photo-7651289.jpeg?auto=compress&w=1920", "business_building"),
        ("https://images.pexels.com/photos/7651283/pexels-photo-7651283.jpeg?auto=compress&w=1920", "reception_area"),
        ("https://images.pexels.com/photos/7651276/pexels-photo-7651276.jpeg?auto=compress&w=1920", "conference_room"),
    ],
    "books": [
        ("https://images.pexels.com/photos/6370/art-cup-glasses-desk.jpg?auto=compress&w=1920", "desk_coffee_books"),
        ("https://images.pexels.com/photos/904616/pexels-photo-904616.jpeg?auto=compress&w=1920", "open_books"),
        ("https://images.pexels.com/photos/159711/books-bookstore-book-reading-159711.jpeg?auto=compress&w=1920", "bookstore"),
        ("https://images.pexels.com/photos/1144517/pexels-photo-1144517.jpeg?auto=compress&w=1920", "old_books"),
        ("https://images.pexels.com/photos/2041549/pexels-photo-2041549.jpeg?auto=compress&w=1920", "stacked_books"),
        ("https://images.pexels.com/photos/2747449/pexels-photo-2747449.jpeg?auto=compress&w=1920", "bookshelf_detailed"),
        ("https://images.pexels.com/photos/3358707/pexels-photo-3358707.jpeg?auto=compress&w=1920", "book_pages"),
        ("https://images.pexels.com/photos/415071/pexels-photo-415071.jpeg?auto=compress&w=1920", "book_reading"),
        ("https://images.pexels.com/photos/1200645/pexels-photo-1200645.jpeg?auto=compress&w=1920", "textbooks"),
        ("https://images.pexels.com/photos/159402/pexels-photo-159402.jpeg?auto=compress&w=1920", "study_materials"),
        ("https://images.pexels.com/photos/1619839/pexels-photo-1619839.jpeg?auto=compress&w=1920", "notebook_stack"),
        ("https://images.pexels.com/photos/196655/pexels-photo-196655.jpeg?auto=compress&w=1920", "book_on_desk"),
        ("https://images.pexels.com/photos/209329/pexels-photo-209329.jpeg?auto=compress&w=1920", "book_library"),
        ("https://images.pexels.com/photos/267609/pexels-photo-267609.jpeg?auto=compress&w=1920", "reading_lamp"),
        ("https://images.pexels.com/photos/2744107/pexels-photo-2744107.jpeg?auto=compress&w=1920", "bookshelf_rows"),
    ],
    "exam": [
        ("https://images.pexels.com/photos/8115857/pexels-photo-8115857.jpeg?auto=compress&w=1920", "graduation_ceremony"),
        ("https://images.pexels.com/photos/4778624/pexels-photo-4778624.jpeg?auto=compress&w=1920", "certificate_award"),
        ("https://images.pexels.com/photos/5720333/pexels-photo-5720333.jpeg?auto=compress&w=1920", "success_hands"),
        ("https://images.pexels.com/photos/3178810/pexels-photo-3178810.jpeg?auto=compress&w=1920", "graduation_cap"),
        ("https://images.pexels.com/photos/5427670/pexels-photo-5427670.jpeg?auto=compress&w=1920", "diploma_roll"),
        ("https://images.pexels.com/photos/5427686/pexels-photo-5427686.jpeg?auto=compress&w=1920", "ceremony_hall"),
        ("https://images.pexels.com/photos/5490778/pexels-photo-5490778.jpeg?auto=compress&w=1920", "congratulations"),
        ("https://images.pexels.com/photos/5490883/pexels-photo-5490883.jpeg?auto=compress&w=1920", "celebration"),
        ("https://images.pexels.com/photos/5082579/pexels-photo-5082579.jpeg?auto=compress&w=1920", "student_exam"),
        ("https://images.pexels.com/photos/5427680/pexels-photo-5427680.jpeg?auto=compress&w=1920", "trophy_success"),
        ("https://images.pexels.com/photos/5699585/pexels-photo-5699585.jpeg?auto=compress&w=1920", "medal_award"),
        ("https://images.pexels.com/photos/5699591/pexels-photo-5699591.jpeg?auto=compress&w=1920", "winner_podium"),
        ("https://images.pexels.com/photos/7773537/pexels-photo-7773537.jpeg?auto=compress&w=1920", "exam_papers"),
        ("https://images.pexels.com/photos/7773509/pexels-photo-7773509.jpeg?auto=compress&w=1920", "pen_test"),
        ("https://images.pexels.com/photos/7773489/pexels-photo-7773489.jpeg?auto=compress&w=1920", "writing_exam"),
    ],
    "motivation": [
        ("https://images.pexels.com/photos/207696/pexels-photo-207696.jpeg?auto=compress&w=1920", "sunrise_mountain"),
        ("https://images.pexels.com/photos/1687845/pexels-photo-1687845.jpeg?auto=compress&w=1920", "running_runner"),
        ("https://images.pexels.com/photos/1240263/pexels-photo-1240263.jpeg?auto=compress&w=1920", "athlete_run"),
        ("https://images.pexels.com/photos/2405547/pexels-photo-2405547.jpeg?auto=compress&w=1920", "mountain_peak"),
        ("https://images.pexels.com/photos/1365421/pexels-photo-1365421.jpeg?auto=compress&w=1920", "road_path"),
        ("https://images.pexels.com/photos/1083012/pexels-photo-1083012.jpeg?auto=compress&w=1920", "hiking_trail"),
        ("https://images.pexels.com/photos/1366919/pexels-photo-1366919.jpeg?auto=compress&w=1920", "ocean_sunrise"),
        ("https://images.pexels.com/photos/136404/pexels-photo-136404.jpeg?auto=compress&w=1920", "nature_sunrise"),
        ("https://images.pexels.com/photos/1409949/pexels-photo-1409949.jpeg?auto=compress&w=1920", "mountain_forest"),
        ("https://images.pexels.com/photos/1287142/pexels-photo-1287142.jpeg?auto=compress&w=1920", "foggy_mountain"),
        ("https://images.pexels.com/photos/1179156/pexels-photo-1179156.jpeg?auto=compress&w=1920", "path_journey"),
        ("https://images.pexels.com/photos/1261728/pexels-photo-1261728.jpeg?auto=compress&w=1920", "road_winding"),
        ("https://images.pexels.com/photos/1700977/pexels-photo-1700977.jpeg?auto=compress&w=1920", "climbing_hill"),
        ("https://images.pexels.com/photos/235734/pexels-photo-235734.jpeg?auto=compress&w=1920", "motivation_light"),
        ("https://images.pexels.com/photos/2422364/pexels-photo-2422364.jpeg?auto=compress&w=1920", "milestone"),
    ],
    "gov": [
        ("https://images.pexels.com/photos/4427430/pexels-photo-4427430.jpeg?auto=compress&w=1920", "government_building"),
        ("https://images.pexels.com/photos/4427432/pexels-photo-4427432.jpeg?auto=compress&w=1920", "capitol_building"),
        ("https://images.pexels.com/photos/4427440/pexels-photo-4427440.jpeg?auto=compress&w=1920", "parliament"),
        ("https://images.pexels.com/photos/4427445/pexels-photo-4427445.jpeg?auto=compress&w=1920", "city_hall"),
        ("https://images.pexels.com/photos/4427450/pexels-photo-4427450.jpeg?auto=compress&w=1920", "court_building"),
        ("https://images.pexels.com/photos/3730651/pexels-photo-3730651.jpeg?auto=compress&w=1920", "official_building"),
        ("https://images.pexels.com/photos/3730655/pexels-photo-3730655.jpeg?auto=compress&w=1920", "government_office"),
        ("https://images.pexels.com/photos/3730660/pexels-photo-3730660.jpeg?auto=compress&w=1920", "institutional"),
        ("https://images.pexels.com/photos/3730665/pexels-photo-3730665.jpeg?auto=compress&w=1920", "monument"),
        ("https://images.pexels.com/photos/3730670/pexels-photo-3730670.jpeg?auto=compress&w=1920", "landmark"),
        ("https://images.pexels.com/photos/3730675/pexels-photo-3730675.jpeg?auto=compress&w=1920", "columns_building"),
        ("https://images.pexels.com/photos/3730680/pexels-photo-3730680.jpeg?auto=compress&w=1920", "palace"),
        ("https://images.pexels.com/photos/3730685/pexels-photo-3730685.jpeg?auto=compress&w=1920", "heritage_building"),
        ("https://images.pexels.com/photos/3730690/pexels-photo-3730690.jpeg?auto=compress&w=1920", "classical_architecture"),
        ("https://images.pexels.com/photos/3730695/pexels-photo-3730695.jpeg?auto=compress&w=1920", "government_center"),
    ],
    "tech": [
        ("https://images.pexels.com/photos/1089438/pexels-photo-1089438.jpeg?auto=compress&w=1920", "computer_setup"),
        ("https://images.pexels.com/photos/1181671/pexels-photo-1181671.jpeg?auto=compress&w=1920", "laptop_work"),
        ("https://images.pexels.com/photos/1181673/pexels-photo-1181673.jpeg?auto=compress&w=1920", "screen_code"),
        ("https://images.pexels.com/photos/1181677/pexels-photo-1181677.jpeg?auto=compress&w=1920", "developer"),
        ("https://images.pexels.com/photos/1181298/pexels-photo-1181298.jpeg?auto=compress&w=1920", "tech_desk"),
        ("https://images.pexels.com/photos/1181354/pexels-photo-1181354.jpeg?auto=compress&w=1920", "computer_office"),
        ("https://images.pexels.com/photos/1181244/pexels-photo-1181244.jpeg?auto=compress&w=1920", "monitor_setup"),
        ("https://images.pexels.com/photos/1181263/pexels-photo-1181263.jpeg?auto=compress&w=1920", "keyboard_mouse"),
        ("https://images.pexels.com/photos/1181370/pexels-photo-1181370.jpeg?auto=compress&w=1920", "workspace_tech"),
        ("https://images.pexels.com/photos/1181679/pexels-photo-1181679.jpeg?auto=compress&w=1920", "data_visualization"),
        ("https://images.pexels.com/photos/1181682/pexels-photo-1181682.jpeg?auto=compress&w=1920", "analytics"),
        ("https://images.pexels.com/photos/1181688/pexels-photo-1181688.jpeg?auto=compress&w=1920", "chart_graph"),
        ("https://images.pexels.com/photos/1181692/pexels-photo-1181692.jpeg?auto=compress&w=1920", "business_intelligence"),
        ("https://images.pexels.com/photos/1181696/pexels-photo-1181696.jpeg?auto=compress&w=1920", "digital_workspace"),
        ("https://images.pexels.com/photos/1181700/pexels-photo-1181700.jpeg?auto=compress&w=1920", "technology_office"),
    ],
    "city": [
        ("https://images.pexels.com/photos/1558439/pexels-photo-1558439.jpeg?auto=compress&w=1920", "shanghai_pudong"),
        ("https://images.pexels.com/photos/1563250/pexels-photo-1563250.jpeg?auto=compress&w=1920", "shanghai_skyline"),
        ("https://images.pexels.com/photos/1563256/pexels-photo-1563256.jpeg?auto=compress&w=1920", "beijing_night"),
        ("https://images.pexels.com/photos/1563260/pexels-photo-1563260.jpeg?auto=compress&w=1920", "modern_city"),
        ("https://images.pexels.com/photos/1563266/pexels-photo-1563266.jpeg?auto=compress&w=1920", "urban_night"),
        ("https://images.pexels.com/photos/1563270/pexels-photo-1563270.jpeg?auto=compress&w=1920", "city_lights"),
        ("https://images.pexels.com/photos/1563276/pexels-photo-1563276.jpeg?auto=compress&w=1920", "downtown"),
        ("https://images.pexels.com/photos/1563280/pexels-photo-1563280.jpeg?auto=compress&w=1920", "skyscraper"),
        ("https://images.pexels.com/photos/1563286/pexels-photo-1563286.jpeg?auto=compress&w=1920", "business_district"),
        ("https://images.pexels.com/photos/1563290/pexels-photo-1563290.jpeg?auto=compress&w=1920", "towers"),
        ("https://images.pexels.com/photos/1506906/pexels-photo-1506906.jpeg?auto=compress&w=1920", "mountain_city"),
        ("https://images.pexels.com/photos/1474739/pexels-photo-1474739.jpeg?auto=compress&w=1920", "urban_road"),
        ("https://images.pexels.com/photos/1486325/pexels-photo-1486325.jpeg?auto=compress&w=1920", "cityscape"),
        ("https://images.pexels.com/photos/1497528/pexels-photo-1497528.jpeg?auto=compress&w=1920", "aerial_city"),
        ("https://images.pexels.com/photos/151817394/pexels-photo-151817394.jpeg?auto=compress&w=1920", "night_city"),
    ],
    "writing": [
        ("https://images.pexels.com/photos/1024253/pexels-photo-1024253.jpeg?auto=compress&w=1920", "writing_hand"),
        ("https://images.pexels.com/photos/1024257/pexels-photo-1024257.jpeg?auto=compress&w=1920", "pen_notebook"),
        ("https://images.pexels.com/photos/1024261/pexels-photo-1024261.jpeg?auto=compress&w=1920", "writing_desk"),
        ("https://images.pexels.com/photos/1024265/pexels-photo-1024265.jpeg?auto=compress&w=1920", "notes_pen"),
        ("https://images.pexels.com/photos/1024270/pexels-photo-1024270.jpeg?auto=compress&w=1920", "stationery"),
        ("https://images.pexels.com/photos/1024275/pexels-photo-1024275.jpeg?auto=compress&w=1920", "desk_supplies"),
        ("https://images.pexels.com/photos/1024280/pexels-photo-1024280.jpeg?auto=compress&w=1920", "calendar_planner"),
        ("https://images.pexels.com/photos/1024285/pexels-photo-1024285.jpeg?auto=compress&w=1920", "to_do_list"),
        ("https://images.pexels.com/photos/1024290/pexels-photo-1024290.jpeg?auto=compress&w=1920", "organizer"),
        ("https://images.pexels.com/photos/1024295/pexels-photo-1024295.jpeg?auto=compress&w=1920", "planning"),
        ("https://images.pexels.com/photos/1024300/pexels-photo-1024300.jpeg?auto=compress&w=1920", "journal"),
        ("https://images.pexels.com/photos/1024305/pexels-photo-1024305.jpeg?auto=compress&w=1920", "pencil_paper"),
        ("https://images.pexels.com/photos/1024310/pexels-photo-1024310.jpeg?auto=compress&w=1920", "documents"),
        ("https://images.pexels.com/photos/1024315/pexels-photo-1024315.jpeg?auto=compress&w=1920", "paperwork"),
        ("https://images.pexels.com/photos/1024320/pexels-photo-1024320.jpeg?auto=compress&w=1920", "contract"),
    ],
    "nature": [
        ("https://images.pexels.com/photos/1166209/pexels-photo-1166209.jpeg?auto=compress&w=1920", "park_trees"),
        ("https://images.pexels.com/photos/1170602/pexels-photo-1170602.jpeg?auto=compress&w=1920", "garden_path"),
        ("https://images.pexels.com/photos/1166215/pexels-photo-1166215.jpeg?auto=compress&w=1920", "forest_path"),
        ("https://images.pexels.com/photos/1166220/pexels-photo-1166220.jpeg?auto=compress&w=1920", "nature_trail"),
        ("https://images.pexels.com/photos/1166225/pexels-photo-1166225.jpeg?auto=compress&w=1920", "green_trees"),
        ("https://images.pexels.com/photos/1166230/pexels-photo-1166230.jpeg?auto=compress&w=1920", "outdoor"),
        ("https://images.pexels.com/photos/1166235/pexels-photo-1166235.jpeg?auto=compress&w=1920", "peaceful_nature"),
        ("https://images.pexels.com/photos/1166240/pexels-photo-1166240.jpeg?auto=compress&w=1920", "lakeside"),
        ("https://images.pexels.com/photos/1166245/pexels-photo-1166245.jpeg?auto=compress&w=1920", "meadow"),
        ("https://images.pexels.com/photos/1166250/pexels-photo-1166250.jpeg?auto=compress&w=1920", "sunset_nature"),
        ("https://images.pexels.com/photos/1166255/pexels-photo-1166255.jpeg?auto=compress&w=1920", "river_flow"),
        ("https://images.pexels.com/photos/1166260/pexels-photo-1166260.jpeg?auto=compress&w=1920", "waterfall"),
        ("https://images.pexels.com/photos/1166265/pexels-photo-1166265.jpeg?auto=compress&w=1920", "clouds_sky"),
        ("https://images.pexels.com/photos/1166270/pexels-photo-1166270.jpeg?auto=compress&w=1920", "blue_sky"),
        ("https://images.pexels.com/photos/1166275/pexels-photo-1166275.jpeg?auto=compress&w=1920", "grass_field"),
    ],
    "people": [
        ("https://images.pexels.com/photos/762020/pexels-photo-762020.jpeg?auto=compress&w=1920", "business_woman"),
        ("https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&w=1920", "professional_portrait"),
        ("https://images.pexels.com/photos/775558/pexels-photo-775558.jpeg?auto=compress&w=1920", "business_man"),
        ("https://images.pexels.com/photos/814534/pexels-photo-814534.jpeg?auto=compress&w=1920", "suit_formal"),
        ("https://images.pexels.com/photos/819754/pexels-photo-819754.jpeg?auto=compress&w=1920", "interview"),
        ("https://images.pexels.com/photos/820272/pexels-photo-820272.jpeg?auto=compress&w=1920", "confident"),
        ("https://images.pexels.com/photos/830589/pexels-photo-830589.jpeg?auto=compress&w=1920", "office_worker"),
        ("https://images.pexels.com/photos/840892/pexels-photo-840892.jpeg?auto=compress&w=1920", "team_member"),
        ("https://images.pexels.com/photos/861783/pexels-photo-861783.jpeg?auto=compress&w=1920", "graduated"),
        ("https://images.pexels.com/photos/863926/pexels-photo-863926.jpeg?auto=compress&w=1920", "career"),
        ("https://images.pexels.com/photos/875117/pexels-photo-875117.jpeg?auto=compress&w=1920", "success_person"),
        ("https://images.pexels.com/photos/896106/pexels-photo-896106.jpeg?auto=compress&w=1920", "professional_smile"),
        ("https://images.pexels.com/photos/912654/pexels-photo-912654.jpeg?auto=compress&w=1920", "business_handshake"),
        ("https://images.pexels.com/photos/927022/pexels-photo-927022.jpeg?auto=compress&w=1920", "formal_attire"),
    ],
}

def download_image(url, save_path):
    """下载单张图片"""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            img = Image.open(BytesIO(resp.content))
            if img.width >= 800 and img.height >= 600:
                img.save(save_path, "JPEG", quality=90)
                return True
    except:
        pass
    return False

def main():
    total = 0
    for cat, urls in URLS_V18.items():
        cat_dir = BASE_DIR / cat
        cat_dir.mkdir(exist_ok=True)
        cat_total = 0
        for i, (url, name) in enumerate(urls, 1):
            save_path = cat_dir / f"{cat}_v18_{i:03d}.jpg"
            if not save_path.exists():
                if download_image(url, save_path):
                    cat_total += 1
                    time.sleep(0.3)
        total += cat_total
        print(f"  {cat}: +{cat_total}张")
    print(f"\n✅ V18批次完成: +{total}张")
    return total

if __name__ == "__main__":
    main()
