"""
Модуль стилей для пользовательского интерфейса
"""

# Цветовая схема
COLORS = {
    "primary": "#0a0e17",           # Темно-синий (почти черный)
    "primary_light": "#1a2130",     # Темно-синий светлее
    "accent": "#00D1B2",            # Неоновый бирюзовый
    "background": "#F8F9FA",        # Светлый фон
    "card": "#FFFFFF",              # Белый
    "text": "#212121",              # Почти черный
    "text_secondary": "#757575",    # Серый
    "divider": "#E0E0E0",           # Светло-серый
    "success": "#00C851",           # Неоновый зеленый
    "error": "#ff4444",             # Неоновый красный
    "warning": "#ffbb33",           # Неоновый желтый
    "info": "#33b5e5",              # Неоновый голубой
    "border": "#EEEEEE"             # Очень светло-серый
}

# Основные стили для приложения
MAIN_WINDOW_STYLE = f"""
QMainWindow, QDialog {{
    background-color: {COLORS["background"]};
}}

QWidget {{
    font-family: 'Segoe UI', Arial, sans-serif;
    color: {COLORS["text"]};
}}

QLabel {{
    color: {COLORS["text"]};
}}

QTextEdit {{
    background-color: {COLORS["card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    padding: 10px;
    color: {COLORS["text"]};
    font-size: 13px;
    selection-background-color: {COLORS["accent"]};
}}

QScrollBar:vertical {{
    border: none;
    background-color: {COLORS["background"]};
    width: 10px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS["primary_light"]};
    border-radius: 5px;
    min-height: 20px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QSplitter::handle {{
    background-color: {COLORS["divider"]};
    width: 1px;
}}
"""

# Стиль для кнопок
BUTTON_STYLE = f"""
QPushButton {{
    background-color: {COLORS["primary"]};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: bold;
    font-size: 14px;
    min-height: 20px;
}}

QPushButton:hover {{
    background-color: {COLORS["primary_light"]};
    border: 1px solid {COLORS["accent"]};
}}

QPushButton:pressed {{
    background-color: {COLORS["primary"]};
    border: 2px solid {COLORS["accent"]};
}}

QPushButton:disabled {{
    background-color: #BDC3C7;
    color: #7F8C8D;
}}
"""

# Стиль для кнопки успеха
SUCCESS_BUTTON_STYLE = f"""
QPushButton {{
    background-color: {COLORS["success"]};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: bold;
    font-size: 14px;
    min-height: 20px;
}}

QPushButton:hover {{
    background-color: #00E676;
    border: 1px solid white;
}}

QPushButton:pressed {{
    background-color: {COLORS["success"]};
    border: 2px solid white;
}}

QPushButton:disabled {{
    background-color: #BDC3C7;
    color: #7F8C8D;
}}
"""

# Контейнеры
FRAME_STYLE = f"""
QFrame#contentFrame {{
    background-color: {COLORS["card"]};
    border-radius: 10px;
    border: 1px solid {COLORS["border"]};
}}
"""

# Стиль для области изображения
IMAGE_FRAME_STYLE = f"""
QLabel#imageLabel {{
    background-color: {COLORS["card"]};
    border: 2px dashed {COLORS["primary_light"]};
    border-radius: 10px;
    color: {COLORS["text_secondary"]};
}}

QLabel#imageLabel:hover {{
    border: 2px dashed {COLORS["accent"]};
}}
"""

# Стиль для заголовков
TITLE_STYLE = f"""
QLabel#titleLabel {{
    color: {COLORS["primary"]};
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 16px;
    qproperty-alignment: AlignCenter;
}}
"""

# Стиль для результатов
RESULT_TITLE_STYLE = f"""
QLabel#resultTitleLabel {{
    color: {COLORS["primary"]};
    font-size: 16px;
    font-weight: bold;
    padding-top: 8px;
    padding-bottom: 4px;
}}
"""

# Стиль для карточек
CARD_STYLE = f"""
QFrame#card {{
    background-color: {COLORS["card"]};
    border-radius: 10px;
    border: 1px solid {COLORS["border"]};
}}
"""

# Стиль для строки состояния
STATUS_BAR_STYLE = f"""
QStatusBar {{
    background-color: {COLORS["primary"]};
    color: white;
    padding: 5px;
    font-weight: bold;
}}
""" 