import sys
import os
import shutil
import json
import re
import csv
import ctypes 
import time
from datetime import datetime
import qtawesome as qta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QPushButton, QListWidget, 
                             QLabel, QDialog, QMessageBox, QSizePolicy, QListWidgetItem, QGroupBox, QFileDialog, QPlainTextEdit, QFrame, QLineEdit, QComboBox)
from PyQt5.QtCore import Qt, QUrl, QTimer, QMimeData, QPoint, QSize
from PyQt5.QtGui import QDesktopServices, QPixmap, QIcon, QDrag, QColor, QImageReader

# ==========================================
# GLOBAL LANGUAGE SYSTEM & DICTIONARY
# ==========================================
CURRENT_LANG = "English"

UI_TEXT = {
    "English": {
        "main_title": "StockAI Pro - Asset Manager",
        "detail_title": "StockAI Pro - Details",
        "paste_label": "<b>Paste Prompt Here (Auto-Add):</b>",
        "info": " Info",
        "prompts_btn": " My Prompts",
        "bmc": " Buy Me a Coffee",
        "placeholder": "Paste the format here and it will be automatically added to the list...",
        "pending_group": " Pending Assets (Double Click to Open)",
        "uploaded_group": " Uploaded Assets",
        "up_all": " Upload All to Adobe Stock",
        "del_pen": " Delete All Pending",
        "del_upl": " Delete All Uploaded",
        "export_csv": " Export CSV & Images for Adobe Stock",
        "prompt_lbl": "Prompt",
        "title_lbl": "Title",
        "keywords_lbl": "Keywords",
        "category_lbl": "Category",
        "copy_link": " Copy Folder Link",
        "open_folder": " Open Linked Folder",
        "browse_manual": " Browse Manually",
        "replace_img": " Replace Image",
        "copy": " Copy",
        "copied": " Copied!",
        "drag_drop": "Drag & Drop Here\nOr Click to Auto-Pick Latest Download",
        "auto_picked": " Auto-Picked Latest Image!\nClosing...",
        "my_prompts_title": "My Custom Prompts",
        "export_all_prompts": " Export All Prompts",
        "add_new_prompt": " Add New Prompt",
        "advanced_editor": "Advanced Prompt Editor",
        "save_prompt": " Save Prompt",
        "cancel": " Cancel",
        "edit_prompt": " Edit Prompt",
        "untitled": "Untitled Prompt",
        "auto_search_title": "Auto Image Search",
        "searching": " Prompt Copied!\nDownloading image... Please wait.",
        "force_pick": " Force Auto Pick",
        "img_found": " Image Found! Applying...",
        "err_save": " Error saving file!"
    },
    "Hindi": {
        "main_title": "StockAI Pro - Asset Manager",
        "detail_title": "StockAI Pro - Details",
        "paste_label": "<b>Yahan Paste Karein (Auto-Add):</b>",
        "info": " Jankari",
        "prompts_btn": " Mere Prompts",
        "bmc": " Buy Me a Coffee",
        "placeholder": "Format paste karte hi ye automatically list me add ho jayega...",
        "pending_group": " Pending Assets (Double Click to Open)",
        "uploaded_group": " Uploaded Assets",
        "up_all": " Sabhi Adobe Stock Par Upload Karein",
        "del_pen": " Sabhi Pending Delete Karein",
        "del_upl": " Sabhi Uploaded Delete Karein",
        "export_csv": " Adobe Stock ke liye CSV & Images Export Karein",
        "prompt_lbl": "Prompt",
        "title_lbl": "Title",
        "keywords_lbl": "Keywords",
        "category_lbl": "Category",
        "copy_link": " Folder Link Copy Karein",
        "open_folder": " Linked Folder Kholein",
        "browse_manual": " Manually Browse Karein",
        "replace_img": " Image Replace Karein",
        "copy": " Copy",
        "copied": " Copied!",
        "drag_drop": "Drag & Drop Karein\nYa Click Karke Latest Download Auto-Pick Karein",
        "auto_picked": " Latest Image Auto-Pick Ho Gayi!\nClosing...",
        "my_prompts_title": "Mere Custom Prompts",
        "export_all_prompts": " Sabhi Prompts Export Karein",
        "add_new_prompt": " Naya Prompt Jodein",
        "advanced_editor": "Advanced Prompt Editor",
        "save_prompt": " Prompt Save Karein",
        "cancel": " Cancel",
        "edit_prompt": " Prompt Edit Karein",
        "untitled": "Bina Naam ka Prompt",
        "auto_search_title": "Auto Image Search",
        "searching": " Prompt Copied!\nImage download ho rahi hai... Kripya pratiksha karein.",
        "force_pick": " Force Auto Pick",
        "img_found": " Image Mil Gayi! Apply kar rahe hain...",
        "err_save": " File save karne me error!"
    },
    "Español": {
        "main_title": "StockAI Pro - Gestor de Activos",
        "detail_title": "StockAI Pro - Detalles",
        "paste_label": "<b>Pegar Prompt Aquí (Auto-Añadir):</b>",
        "info": " Info",
        "prompts_btn": " Mis Prompts",
        "bmc": " Cómprame un Café",
        "placeholder": "Pegue el formato aquí y se añadirá a la lista automáticamente...",
        "pending_group": " Activos Pendientes (Doble clic)",
        "uploaded_group": " Activos Subidos",
        "up_all": " Subir Todo a Adobe Stock",
        "del_pen": " Eliminar Todos Pendientes",
        "del_upl": " Eliminar Todos Subidos",
        "export_csv": " Exportar CSV e Imágenes para Adobe",
        "prompt_lbl": "Prompt",
        "title_lbl": "Título",
        "keywords_lbl": "Palabras clave",
        "category_lbl": "Categoría",
        "copy_link": " Copiar Enlace de Carpeta",
        "open_folder": " Abrir Carpeta Vinculada",
        "browse_manual": " Buscar Manualmente",
        "replace_img": " Reemplazar Imagen",
        "copy": " Copiar",
        "copied": " ¡Copiado!",
        "drag_drop": "Arrastra y Suelta Aquí\nO Haz Clic para Auto-Seleccionar Descarga",
        "auto_picked": " ¡Última Imagen Seleccionada!\nCerrando...",
        "my_prompts_title": "Mis Prompts Personalizados",
        "export_all_prompts": " Exportar Todos los Prompts",
        "add_new_prompt": " Añadir Nuevo Prompt",
        "advanced_editor": "Editor Avanzado de Prompts",
        "save_prompt": " Guardar Prompt",
        "cancel": " Cancelar",
        "edit_prompt": " Editar Prompt",
        "untitled": "Prompt sin Título",
        "auto_search_title": "Búsqueda Automática",
        "searching": " ¡Prompt Copiado!\nDescargando imagen... Por favor espera.",
        "force_pick": " Forzar Selección",
        "img_found": " ¡Imagen Encontrada! Aplicando...",
        "err_save": " ¡Error al guardar archivo!"
    },
    "Português": {
        "main_title": "StockAI Pro - Gerenciador",
        "detail_title": "StockAI Pro - Detalhes",
        "paste_label": "<b>Colar Prompt Aqui (Auto-Add):</b>",
        "info": " Info",
        "prompts_btn": " Meus Prompts",
        "bmc": " Compre-me um Café",
        "placeholder": "Cole o formato aqui e ele será adicionado à lista automaticamente...",
        "pending_group": " Ativos Pendientes (Duplo clique)",
        "uploaded_group": " Ativos Enviados",
        "up_all": " Enviar Tudo para Adobe Stock",
        "del_pen": " Excluir Todos Pendentes",
        "del_upl": " Excluir Todos Enviados",
        "export_csv": " Exportar CSV e Imagens para Adobe",
        "prompt_lbl": "Prompt",
        "title_lbl": "Título",
        "keywords_lbl": "Palavras-chave",
        "category_lbl": "Categoria",
        "copy_link": " Copiar Link da Pasta",
        "open_folder": " Abrir Pasta Vinculada",
        "browse_manual": " Procurar Manualmente",
        "replace_img": " Substituir Imagem",
        "copy": " Copiar",
        "copied": " Copiado!",
        "drag_drop": "Arraste e Solte Aqui\nOu Clique para Pegar Último Download",
        "auto_picked": " Última Imagem Pega!\nFechando...",
        "my_prompts_title": "Meus Prompts Personalizados",
        "export_all_prompts": " Exportar Todos os Prompts",
        "add_new_prompt": " Adicionar Novo Prompt",
        "advanced_editor": "Editor Avançado",
        "save_prompt": " Salvar Prompt",
        "cancel": " Cancelar",
        "edit_prompt": " Editar Prompt",
        "untitled": "Prompt Sem Título",
        "auto_search_title": "Busca Automática",
        "searching": " Prompt Copiado!\nBaixando imagem... Aguarde.",
        "force_pick": " Forçar Escolha",
        "img_found": " Imagem Encontrada! Aplicando...",
        "err_save": " Erro ao salvar arquivo!"
    },
    "Русский": {
        "main_title": "StockAI Pro - Менеджер активов",
        "detail_title": "StockAI Pro - Детали",
        "paste_label": "<b>Вставить Промпт (Авто-Добавление):</b>",
        "info": " Инфо",
        "prompts_btn": " Мои Промпты",
        "bmc": " Купить мне кофе",
        "placeholder": "Вставьте формат сюда, и он будет автоматически добавлен...",
        "pending_group": " Ожидающие (Двойной клик)",
        "uploaded_group": " Загруженные",
        "up_all": " Загрузить все на Adobe Stock",
        "del_pen": " Удалить все ожидающие",
        "del_upl": " Удалить все загруженные",
        "export_csv": " Экспорт CSV и Изображений для Adobe",
        "prompt_lbl": "Промпт",
        "title_lbl": "Название",
        "keywords_lbl": "Ключевые слова",
        "category_lbl": "Категория",
        "copy_link": " Скопировать ссылку",
        "open_folder": " Открыть папку",
        "browse_manual": " Выбрать вручную",
        "replace_img": " Заменить изображение",
        "copy": " Копировать",
        "copied": " Скопировано!",
        "drag_drop": "Перетащите сюда\nИли нажмите для автовыбора",
        "auto_picked": " Изображение выбрано!\nЗакрытие...",
        "my_prompts_title": "Мои кастомные промпты",
        "export_all_prompts": " Экспорт всех промптов",
        "add_new_prompt": " Добавить новый промпт",
        "advanced_editor": "Продвинутый редактор",
        "save_prompt": " Сохранить",
        "cancel": " Отмена",
        "edit_prompt": " Изменить",
        "untitled": "Промпт без названия",
        "auto_search_title": "Автопоиск",
        "searching": " Промпт скопирован!\nОжидание загрузки...",
        "force_pick": " Принудительный выбор",
        "img_found": " Изображение найдено! Применяем...",
        "err_save": " Ошибка сохранения!"
    },
    "日本語": {
        "main_title": "StockAI Pro - アセットマネージャー",
        "detail_title": "StockAI Pro - 詳細",
        "paste_label": "<b>プロンプトを貼り付け (自動追加):</b>",
        "info": " 情報",
        "prompts_btn": " プロンプト",
        "bmc": " コーヒーをおごる",
        "placeholder": "ここにフォーマットを貼り付けると自動的にリストに追加されます...",
        "pending_group": " 保留中のアセット (ダブルクリック)",
        "uploaded_group": " アップロード済み",
        "up_all": " すべてAdobe Stockにアップロード",
        "del_pen": " すべての保留中を削除",
        "del_upl": " すべてのアップロード済みを削除",
        "export_csv": " CSVと画像をエクスポート",
        "prompt_lbl": "プロンプト",
        "title_lbl": "タイトル",
        "keywords_lbl": "キーワード",
        "category_lbl": "カテゴリー",
        "copy_link": " フォルダリンクをコピー",
        "open_folder": " フォルダを開く",
        "browse_manual": " 手動で参照",
        "replace_img": " 画像を置換",
        "copy": " コピー",
        "copied": " コピー完了!",
        "drag_drop": "ここにドラッグ＆ドロップ\nまたはクリックして最新を自動取得",
        "auto_picked": " 最新画像を取得しました！\n閉じています...",
        "my_prompts_title": "マイプロンプト",
        "export_all_prompts": " すべてエクスポート",
        "add_new_prompt": " 新規プロンプト追加",
        "advanced_editor": "プロンプトエディタ",
        "save_prompt": " 保存する",
        "cancel": " キャンセル",
        "edit_prompt": " 編集する",
        "untitled": "無題のプロンプト",
        "auto_search_title": "自動画像検索",
        "searching": " コピーしました！\n画像のダウンロードを待機中...",
        "force_pick": " 強制取得",
        "img_found": " 画像を発見！適用中...",
        "err_save": " 保存エラー！"
    },
    "Deutsch": {
        "main_title": "StockAI Pro - Asset-Manager",
        "detail_title": "StockAI Pro - Details",
        "paste_label": "<b>Prompt Hier Einfügen (Auto-Add):</b>",
        "info": " Info",
        "prompts_btn": " Meine Prompts",
        "bmc": " Kaffee Spendieren",
        "placeholder": "Fügen Sie das Format hier ein und es wird automatisch hinzugefügt...",
        "pending_group": " Ausstehende Assets (Doppelklick)",
        "uploaded_group": " Hochgeladene Assets",
        "up_all": " Alle zu Adobe Stock Hochladen",
        "del_pen": " Alle Ausstehenden Löschen",
        "del_upl": " Alle Hochgeladenen Löschen",
        "export_csv": " CSV & Bilder Exportieren",
        "prompt_lbl": "Prompt",
        "title_lbl": "Titel",
        "keywords_lbl": "Schlüsselwörter",
        "category_lbl": "Kategorie",
        "copy_link": " Ordnerlink Kopieren",
        "open_folder": " Verknüpften Ordner Öffnen",
        "browse_manual": " Manuell Durchsuchen",
        "replace_img": " Bild Ersetzen",
        "copy": " Kopieren",
        "copied": " Kopiert!",
        "drag_drop": "Hierhin ziehen\nOder klicken für Auto-Pick",
        "auto_picked": " Letztes Bild ausgewählt!\nSchließen...",
        "my_prompts_title": "Meine Benutzerdefinierten Prompts",
        "export_all_prompts": " Alle Prompts Exportieren",
        "add_new_prompt": " Neuen Prompt Hinzufügen",
        "advanced_editor": "Erweiterter Editor",
        "save_prompt": " Prompt Speichern",
        "cancel": " Abbrechen",
        "edit_prompt": " Prompt Bearbeiten",
        "untitled": "Unbenannter Prompt",
        "auto_search_title": "Automatische Bildsuche",
        "searching": " Prompt Kopiert!\nWarten auf Download...",
        "force_pick": " Auswahl Erzwingen",
        "img_found": " Bild Gefunden! Wende an...",
        "err_save": " Fehler beim Speichern!"
    },
    "Français": {
        "main_title": "StockAI Pro - Gestionnaire",
        "detail_title": "StockAI Pro - Détails",
        "paste_label": "<b>Coller le Prompt (Auto-Ajout):</b>",
        "info": " Info",
        "prompts_btn": " Mes Prompts",
        "bmc": " Offrez-moi un Café",
        "placeholder": "Collez le format ici et il sera automatiquement ajouté à la liste...",
        "pending_group": " Actifs en Attente (Double Clic)",
        "uploaded_group": " Actifs Téléchargés",
        "up_all": " Tout Télécharger sur Adobe",
        "del_pen": " Supprimer Tous les en Attente",
        "del_upl": " Supprimer Tous les Téléchargés",
        "export_csv": " Exporter CSV et Images",
        "prompt_lbl": "Prompt",
        "title_lbl": "Titre",
        "keywords_lbl": "Mots-clés",
        "category_lbl": "Catégorie",
        "copy_link": " Copier le Lien du Dossier",
        "open_folder": " Ouvrir le Dossier",
        "browse_manual": " Parcourir Manuellement",
        "replace_img": " Remplacer l'Image",
        "copy": " Copier",
        "copied": " Copié !",
        "drag_drop": "Glissez-Déposez Ici\nOu Cliquez pour Auto-Sélectionner",
        "auto_picked": " Dernière image sélectionnée !\nFermeture...",
        "my_prompts_title": "Mes Prompts Personnalisés",
        "export_all_prompts": " Exporter Tous les Prompts",
        "add_new_prompt": " Ajouter un Nouveau Prompt",
        "advanced_editor": "Éditeur Avancé",
        "save_prompt": " Enregistrer",
        "cancel": " Annuler",
        "edit_prompt": " Modifier",
        "untitled": "Prompt Sans Titre",
        "auto_search_title": "Recherche Automatique",
        "searching": " Prompt Copié !\nAttente du téléchargement...",
        "force_pick": " Forcer la Sélection",
        "img_found": " Image Trouvée ! Application...",
        "err_save": " Erreur d'enregistrement !"
    }
}

def t(key):
    # Helpher function to fetch current language text
    lang_dict = UI_TEXT.get(CURRENT_LANG, UI_TEXT["English"])
    return lang_dict.get(key, UI_TEXT["English"].get(key, key))

def get_real_documents_path():
    CSIDL_PERSONAL = 5       
    SHGFP_TYPE_CURRENT = 0   
    buf = ctypes.create_unicode_buffer(260) 
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    return buf.value

def get_latest_image_from_downloads():
    downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    if not os.path.exists(downloads_dir): return None
    
    valid_exts = ('.png', '.jpg', '.jpeg', '.webp')
    latest_file = None
    max_time = 0
    
    try:
        with os.scandir(downloads_dir) as it:
            for entry in it:
                if entry.is_file() and entry.name.lower().endswith(valid_exts):
                    mtime = entry.stat().st_mtime
                    if mtime > max_time:
                        max_time = mtime
                        latest_file = entry.path
    except Exception:
        pass
        
    return latest_file

WORKSPACE_DIR = os.path.join(get_real_documents_path(), 'StockAI_Pro_Workspace')
os.makedirs(WORKSPACE_DIR, exist_ok=True)

DATA_FILE = os.path.join(WORKSPACE_DIR, "saved_prompts.json")
PICKED_DATA_FILE = os.path.join(WORKSPACE_DIR, "picked_images.json")
MY_PROMPTS_FILE = os.path.join(WORKSPACE_DIR, "my_custom_prompts.json")
SETTINGS_FILE = os.path.join(WORKSPACE_DIR, "settings.json")
OUTPUT_FOLDER = "Adobe_Stock_Assets"
DELETED_FOLDER = "Deleted_Assets"
THUMBNAILS_FOLDER = "Thumbnails"

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
ICON_FILE = os.path.join(application_path, "app_icon.ico")

# ==========================================
# MY PROMPTS & NOTEPAD CLASSES
# ==========================================

class NotepadDialog(QDialog):
    def __init__(self, parent=None, existing_title="", existing_text=""):
        super().__init__(parent)
        self.setWindowTitle(t("advanced_editor"))
        
        screen_geo = QApplication.primaryScreen().geometry()
        self.resize(int(screen_geo.width() * 0.8), int(screen_geo.height() * 0.8))
        
        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)
        
        layout = QVBoxLayout(self)
        
        self.title_input = QLineEdit(self)
        self.title_input.setText(existing_title)
        self.title_input.setPlaceholderText(t("untitled"))
        self.title_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 12px;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                background-color: #FFFFFF;
                color: #1F2937;
                margin-bottom: 5px;
            }
            QLineEdit:focus { border: 1px solid #3B82F6; }
        """)
        layout.addWidget(self.title_input)
        
        self.editor = QPlainTextEdit(self)
        self.editor.setPlainText(existing_text)
        self.editor.setStyleSheet("""
            QPlainTextEdit {
                font-family: Consolas, 'Courier New', monospace;
                font-size: 15px;
                background-color: #FFFFFF;
                color: #1F2937;
                padding: 15px;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
            }
            QPlainTextEdit:focus { border: 1px solid #3B82F6; }
        """)
        layout.addWidget(self.editor)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton(t("cancel"))
        cancel_btn.setIcon(qta.icon('fa5s.times', color='white'))
        cancel_btn.setStyleSheet("background-color: #EF4444; color: white; padding: 10px 25px; font-weight: bold; border-radius: 6px; font-size: 14px;")
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton(t("save_prompt"))
        save_btn.setIcon(qta.icon('fa5s.save', color='white'))
        save_btn.setStyleSheet("background-color: #10B981; color: white; padding: 10px 25px; font-weight: bold; border-radius: 6px; font-size: 14px;")
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
    def get_data(self):
        return self.title_input.text().strip(), self.editor.toPlainText()

class PromptCardWidget(QFrame):
    def __init__(self, prompt_data, parent_dialog):
        super().__init__()
        self.prompt_data = prompt_data
        self.parent_dialog = parent_dialog
        
        self.setFixedSize(320, 260)
        self.setStyleSheet("""
            PromptCardWidget {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
            }
            PromptCardWidget:hover {
                border: 1px solid #3B82F6;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        
        header_layout = QHBoxLayout()
        title_text = self.prompt_data.get('title', t('untitled'))
        if not title_text: title_text = t('untitled')
        self.title_label = QLabel(title_text)
        self.title_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #111827; border: none;")
        
        self.pin_btn = QPushButton()
        self.pin_btn.setFixedSize(28, 25)
        self.pin_btn.setCursor(Qt.PointingHandCursor)
        self.update_pin_style()
        self.pin_btn.clicked.connect(self.toggle_pin)
        
        del_btn = QPushButton()
        del_btn.setIcon(qta.icon('fa5s.trash', color='#EF4444'))
        del_btn.setFixedSize(25, 25)
        del_btn.setStyleSheet("background-color: transparent; border: none;")
        del_btn.setCursor(Qt.PointingHandCursor)
        del_btn.clicked.connect(self.delete_prompt)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.pin_btn)
        header_layout.addWidget(del_btn)
        layout.addLayout(header_layout)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("border: 1px solid #E5E7EB;")
        layout.addWidget(line)
        
        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setPlainText(self.prompt_data.get('text', ''))
        self.preview.setStyleSheet("""
            QPlainTextEdit {
                background-color: transparent;
                border: none;
                font-size: 13px;
                color: #6B7280;
            }
        """)
        layout.addWidget(self.preview)
        
        footer_layout = QHBoxLayout()
        
        self.copy_btn = QPushButton(t("copy"))
        self.copy_btn.setIcon(qta.icon('fa5s.copy', color='white'))
        self.copy_btn.setStyleSheet("background-color: #3B82F6; color: white; font-weight: bold; border-radius: 4px; padding: 6px 12px; border: none;")
        self.copy_btn.setCursor(Qt.PointingHandCursor)
        self.copy_btn.clicked.connect(self.copy_text)
        
        edit_btn = QPushButton(t("edit_prompt"))
        edit_btn.setIcon(qta.icon('fa5s.edit', color='white'))
        edit_btn.setStyleSheet("background-color: #10B981; color: white; font-weight: bold; border-radius: 4px; padding: 6px 12px; border: none;")
        edit_btn.setCursor(Qt.PointingHandCursor)
        edit_btn.clicked.connect(self.edit_prompt)
        
        footer_layout.addWidget(self.copy_btn)
        footer_layout.addStretch()
        footer_layout.addWidget(edit_btn)
        layout.addLayout(footer_layout)

    def update_pin_style(self):
        if self.prompt_data.get('pinned', False):
            self.pin_btn.setIcon(qta.icon('fa5s.thumbtack', color='white'))
            self.pin_btn.setStyleSheet("background-color: #10B981; border-radius: 4px; border: none;")
        else:
            self.pin_btn.setIcon(qta.icon('fa5s.thumbtack', color='#6B7280'))
            self.pin_btn.setStyleSheet("background-color: #E5E7EB; border-radius: 4px; border: none;")

    def toggle_pin(self):
        is_pinned = self.prompt_data.get('pinned', False)
        self.prompt_data['pinned'] = not is_pinned
        self.parent_dialog.save_and_refresh()

    def edit_prompt(self):
        dialog = NotepadDialog(self.parent_dialog, self.prompt_data.get('title', ''), self.prompt_data.get('text', ''))
        if dialog.exec_() == QDialog.Accepted:
            new_title, new_text = dialog.get_data()
            self.prompt_data['title'] = new_title
            self.prompt_data['text'] = new_text
            self.title_label.setText(new_title if new_title else t('untitled'))
            self.preview.setPlainText(new_text)
            self.parent_dialog.save_and_refresh()

    def delete_prompt(self):
        reply = QMessageBox.question(self, 'Delete', "Delete this prompt?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.parent_dialog.prompts_list = [p for p in self.parent_dialog.prompts_list if p['id'] != self.prompt_data['id']]
            self.parent_dialog.save_and_refresh()

    def copy_text(self):
        QApplication.clipboard().setText(self.prompt_data.get('text', ''))
        self.copy_btn.setText(t("copied"))
        self.copy_btn.setIcon(qta.icon('fa5s.check', color='white'))
        self.copy_btn.setStyleSheet("background-color: #10B981; color: white; font-weight: bold; border-radius: 4px; padding: 6px 12px; border: none;")
        QTimer.singleShot(1500, lambda: self.copy_btn.setText(t("copy")))
        QTimer.singleShot(1500, lambda: self.copy_btn.setIcon(qta.icon('fa5s.copy', color='white')))
        QTimer.singleShot(1500, lambda: self.copy_btn.setStyleSheet("background-color: #3B82F6; color: white; font-weight: bold; border-radius: 4px; padding: 6px 12px; border: none;"))

class MyPromptsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("my_prompts_title"))
        if os.path.exists(ICON_FILE): self.setWindowIcon(QIcon(ICON_FILE))
        
        screen_geo = QApplication.primaryScreen().geometry()
        self.resize(int(screen_geo.width() * 0.8), int(screen_geo.height() * 0.8))
        
        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)
        
        self.prompts_list = self.load_prompts()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        self.grid_list = QListWidget()
        self.grid_list.setViewMode(QListWidget.IconMode)
        self.grid_list.setResizeMode(QListWidget.Adjust)
        self.grid_list.setSpacing(20)
        self.grid_list.setMovement(QListWidget.Static)
        self.grid_list.setGridSize(QSize(340, 280))
        self.grid_list.setStyleSheet("""
            QListWidget { background-color: #F3F4F6; border: none; }
            QListWidget::item:selected { background-color: transparent; }
        """)
        layout.addWidget(self.grid_list)
        
        bottom_layout = QHBoxLayout()
        
        export_btn = QPushButton(t("export_all_prompts"))
        export_btn.setIcon(qta.icon('fa5s.file-export', color='white'))
        export_btn.setFixedHeight(45)
        export_btn.setStyleSheet("background-color: #F59E0B; color: white; font-size: 15px; font-weight: bold; border-radius: 6px; padding: 0px 30px;")
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.clicked.connect(self.export_all_prompts)
        
        add_btn = QPushButton(t("add_new_prompt"))
        add_btn.setIcon(qta.icon('fa5s.plus', color='#8B5CF6'))
        add_btn.setFixedHeight(45)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: 2px dashed #8B5CF6;
                border-radius: 6px;
                font-size: 16px;
                color: #8B5CF6;
                font-weight: bold;
                padding: 0px 30px;
            }
            QPushButton:hover { background-color: #F3E8FF; }
        """)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.add_new_prompt)
        
        bottom_layout.addWidget(export_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(add_btn)
        bottom_layout.addStretch()
        
        layout.addLayout(bottom_layout)
        self.refresh_grid()

    def load_prompts(self):
        if os.path.exists(MY_PROMPTS_FILE):
            try:
                with open(MY_PROMPTS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: pass
        return []

    def save_and_refresh(self):
        with open(MY_PROMPTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.prompts_list, f, indent=4)
        self.refresh_grid()

    def refresh_grid(self):
        self.grid_list.clear()
        sorted_prompts = sorted(self.prompts_list, key=lambda p: (p.get('pinned', False), p.get('id', 0)), reverse=True)
        for p_data in sorted_prompts: 
            item = QListWidgetItem(self.grid_list)
            item.setSizeHint(QSize(320, 260))
            card = PromptCardWidget(p_data, self)
            self.grid_list.setItemWidget(item, card)

    def add_new_prompt(self):
        dialog = NotepadDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_title, new_text = dialog.get_data()
            if new_text.strip():
                new_id = max([p.get('id', 0) for p in self.prompts_list], default=0) + 1
                self.prompts_list.append({"id": new_id, "title": new_title, "text": new_text, "pinned": False})
                self.save_and_refresh()

    def export_all_prompts(self):
        if not self.prompts_list:
            QMessageBox.warning(self, "Empty", "No prompts available to export.")
            return
            
        export_root = os.path.join(WORKSPACE_DIR, "Exported_Prompts")
        os.makedirs(export_root, exist_ok=True)
        latest_dir = os.path.join(export_root, "Latest Prompt")
        
        if os.path.exists(latest_dir):
            old_num = 1
            while os.path.exists(os.path.join(export_root, f"Old {old_num}")):
                old_num += 1
            os.rename(latest_dir, os.path.join(export_root, f"Old {old_num}"))
            
        os.makedirs(latest_dir)
        
        for idx, p in enumerate(self.prompts_list):
            raw_text = p.get('text', '')
            custom_title = p.get('title', '')
            
            if custom_title:
                clean_name = re.sub(r'[\\/*?:"<>|]', "", custom_title.strip())
                filename = f"{clean_name}.txt"
            else:
                seo_match = re.search(r'SEO Optimized File Name:\s*(.*)', raw_text, re.IGNORECASE)
                if seo_match:
                    clean_name = re.sub(r'[\\/*?:"<>|]', "", seo_match.group(1).strip())
                    filename = f"{clean_name}.txt" if clean_name else f"Prompt_{idx+1}.txt"
                else:
                    filename = f"Prompt_{idx+1}.txt"
            
            with open(os.path.join(latest_dir, filename), 'w', encoding='utf-8') as f:
                f.write(raw_text)
                
        QMessageBox.information(self, "Success", "Export successful!")
        QDesktopServices.openUrl(QUrl.fromLocalFile(latest_dir))

# ==========================================
# MAIN APP CLASSES
# ==========================================

class CopyButton(QPushButton):
    def __init__(self, text_to_copy):
        super().__init__(t("copy"))
        self.setIcon(qta.icon('fa5s.copy', color='white'))
        self.text_to_copy = text_to_copy
        self.setFixedSize(100, 45)
        self.setStyleSheet("background-color: #3B82F6; color: white; font-weight: bold; border-radius: 6px;")
        self.setCursor(Qt.PointingHandCursor)
        self.clicked.connect(self.copy_action)

    def copy_action(self):
        QApplication.clipboard().setText(self.text_to_copy)
        self.setText(t("copied"))
        self.setIcon(qta.icon('fa5s.check', color='white'))
        self.setStyleSheet("background-color: #10B981; color: white; font-weight: bold; border-radius: 6px;")
        QTimer.singleShot(1000, self.reset_button)

    def reset_button(self):
        self.setText(t("copy"))
        self.setIcon(qta.icon('fa5s.copy', color='white'))
        self.setStyleSheet("background-color: #3B82F6; color: white; font-weight: bold; border-radius: 6px;")

class DropZone(QLabel):
    def __init__(self, entry_data, entry_id, parent_popup):
        super().__init__()
        self.entry_data = entry_data
        self.entry_id = entry_id
        self.parent_popup = parent_popup
        self.img_path = None
        self.drag_start_pos = None
        
        self.setText(t("drag_drop"))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 3px dashed #3B82F6; border-radius: 10px; font-size: 15px; background-color: #F8FAFC; color: #475569; font-weight: bold;")
        self.setAcceptDrops(True)
        self.setMinimumHeight(150) 
        
        self.check_existing_image()

    def check_existing_image(self):
        subfolder_name = f"{self.entry_id:03d}"
        target_dir = os.path.abspath(os.path.join(WORKSPACE_DIR, OUTPUT_FOLDER, subfolder_name))
        if os.path.exists(target_dir):
            try:
                with os.scandir(target_dir) as it:
                    for entry in it:
                        if entry.is_file() and entry.name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                            self.img_path = entry.path
                            break
            except: pass

    def resizeEvent(self, event):
        if self.img_path:
            self.show_preview()
        super().resizeEvent(event)

    def show_preview(self):
        try:
            pixmap = QPixmap(self.img_path)
            scaled_pixmap = pixmap.scaled(self.width() - 10, self.height() - 10, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(scaled_pixmap)
            self.setStyleSheet("border: 3px dashed #10B981; border-radius: 10px; background-color: #F0FDF4;")
        except Exception:
            pass

    def get_latest_downloaded_image(self):
        latest_file_abs = get_latest_image_from_downloads()
        if not latest_file_abs: return None, False
        
        main_win = self.parent_popup.main_window if hasattr(self.parent_popup, 'main_window') else None
        picked_set = main_win.picked_download_files if main_win else set()
        
        if latest_file_abs in picked_set:
            return latest_file_abs, True
            
        return latest_file_abs, False

    def auto_pick_latest(self):
        latest_image, is_duplicate = self.get_latest_downloaded_image()
        
        if is_duplicate:
            reply = QMessageBox.warning(self.parent_popup, "Image Already Used!", "The latest downloaded image has already been used!\n\nPlease download a new one and click 'Retry', or click 'Cancel' to Browse Manually.", QMessageBox.Retry | QMessageBox.Cancel)
            if reply == QMessageBox.Retry:
                self.auto_pick_latest()
            return
            
        if latest_image:
            self.process_dropped_file(latest_image)
            self.setText(t("auto_picked"))
            self.setStyleSheet("border: 3px dashed #10B981; border-radius: 10px; font-size: 16px; background-color: #D1FAE5; color: #065F46; font-weight: bold;")
            if hasattr(self, 'parent_popup') and self.parent_popup:
                QTimer.singleShot(400, self.parent_popup.close)
        else:
            self.browse_file()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.img_path:
                self.drag_start_pos = event.pos()
            else:
                self.auto_pick_latest()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton) or not self.img_path or not self.drag_start_pos:
            return
        
        if (event.pos() - self.drag_start_pos).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        url = QUrl.fromLocalFile(self.img_path)
        mime_data.setUrls([url])
        drag.setMimeData(mime_data)
        
        thumbnail = QPixmap(self.img_path).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        drag.setPixmap(thumbnail)
        drag.setHotSpot(QPoint(thumbnail.width() // 2, thumbnail.height() // 2))
        drag.exec_(Qt.CopyAction)

    def browse_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.webp);;All Files (*)", options=options)
        if file_path:
            self.process_dropped_file(file_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls(): event.accept()
        else: event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls: return
        self.process_dropped_file(urls[0].toLocalFile())
            
    def process_dropped_file(self, file_path):
        os.makedirs(WORKSPACE_DIR, exist_ok=True)
        subfolder_name = f"{self.entry_id:03d}"
        target_dir = os.path.abspath(os.path.join(WORKSPACE_DIR, OUTPUT_FOLDER, subfolder_name))
        os.makedirs(target_dir, exist_ok=True)
        
        for f_name in os.listdir(target_dir):
            if f_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                try: os.remove(os.path.join(target_dir, f_name))
                except: pass
        
        ext = os.path.splitext(file_path)[1]
        seo_name = self.entry_data.get('seo_filename', f'image_{self.entry_id}')
        seo_name = re.sub(r'\.(jpe?g|png|webp)$', '', seo_name, flags=re.IGNORECASE)
        
        new_file_name = f"{seo_name}{ext}"
        new_file_path = os.path.join(target_dir, new_file_name)
        txt_file_path = os.path.join(target_dir, f"{seo_name}.txt")
        
        try:
            shutil.copy(file_path, new_file_path)
            
            thumb_dir = os.path.join(WORKSPACE_DIR, THUMBNAILS_FOLDER)
            os.makedirs(thumb_dir, exist_ok=True)
            thumb_path = os.path.join(thumb_dir, f"{self.entry_id:03d}.jpg")
            reader = QImageReader(new_file_path)
            reader.setScaledSize(QSize(150, 150))
            img = reader.read()
            if not img.isNull():
                img.save(thumb_path, "JPG", 85)
            
            if hasattr(self.parent_popup, 'main_window'):
                self.parent_popup.main_window.picked_download_files.add(os.path.abspath(file_path))
                self.parent_popup.main_window.save_picked_files()
                
            with open(txt_file_path, 'w', encoding='utf-8') as f:
                f.write(f"Title: {self.entry_data.get('title', '')}\n\n")
                f.write(f"Prompt: {self.entry_data.get('prompt', '')}\n\n")
                f.write(f"Keywords: {self.entry_data.get('keywords', '')}\n\n")
                f.write(f"Category: {self.entry_data.get('category', '')}\n")
                f.write(f"Aspect Ratio: {self.entry_data.get('aspect_ratio', '')}\n")
                f.write(f"SEO File Name: {seo_name}\n")

            self.img_path = new_file_path
            self.show_preview()
            if hasattr(self.parent_popup, 'main_window'):
                self.parent_popup.main_window.refresh_lists()
        except Exception as e:
            self.setText(" Error saving file!")

class AutoSearchDialog(QDialog):
    def __init__(self, item_data, main_window):
        super().__init__(main_window)
        self.item_data = item_data
        self.main_window = main_window
        self.setWindowTitle(t("auto_search_title"))
        self.setFixedSize(350, 160)
        
        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)

        QApplication.clipboard().setText(item_data.get('prompt', ''))
        
        self.start_time = time.time()
        
        layout = QVBoxLayout()
        self.status_label = QLabel(t("searching"))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #1F2937;")
        layout.addWidget(self.status_label)
        
        btn_layout = QHBoxLayout()
        self.manual_btn = QPushButton(t("browse_manual"))
        self.manual_btn.setIcon(qta.icon('fa5s.folder-open', color='white'))
        self.manual_btn.setStyleSheet("background-color: #3B82F6; color: white; padding: 6px; font-weight: bold; border-radius: 4px;")
        
        self.auto_btn = QPushButton(t("force_pick"))
        self.auto_btn.setIcon(qta.icon('fa5s.bolt', color='white'))
        self.auto_btn.setStyleSheet("background-color: #F59E0B; color: white; padding: 6px; font-weight: bold; border-radius: 4px;")
        
        btn_layout.addWidget(self.manual_btn)
        btn_layout.addWidget(self.auto_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        self.manual_btn.clicked.connect(self.manual_browse)
        self.auto_btn.clicked.connect(self.force_auto_pick)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_for_new_image)
        self.timer.start(1000) 

    def check_for_new_image(self):
        latest_file = get_latest_image_from_downloads()
        if not latest_file: return
        
        file_mtime = os.path.getmtime(latest_file)
        if file_mtime >= (self.start_time - 2.0):
            if os.path.getsize(latest_file) > 0:
                try:
                    with open(latest_file, 'rb') as f: pass
                    self.timer.stop()
                    self.process_file(latest_file)
                except IOError: pass 

    def force_auto_pick(self):
        self.timer.stop()
        latest_file = get_latest_image_from_downloads()
        if latest_file:
            if latest_file in self.main_window.picked_download_files:
                reply = QMessageBox.warning(self, "Used", "Image already used! Download a new one or Browse Manually.", QMessageBox.Retry | QMessageBox.Cancel)
                if reply == QMessageBox.Retry:
                    self.timer.start(1000)
                return
            self.process_file(latest_file)
            return
        QMessageBox.warning(self, "Not found", "No images found in downloads.")
        self.timer.start(1000)

    def manual_browse(self):
        self.timer.stop()
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.webp);;All Files (*)", options=options)
        if file_path:
            self.process_file(file_path)
        else:
            self.timer.start(1000)

    def process_file(self, file_path):
        self.status_label.setText(t("img_found"))
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #10B981;")
        QApplication.processEvents()
        
        subfolder_name = f"{self.item_data['id']:03d}"
        target_dir = os.path.abspath(os.path.join(WORKSPACE_DIR, OUTPUT_FOLDER, subfolder_name))
        os.makedirs(target_dir, exist_ok=True)
        
        for f_name in os.listdir(target_dir):
            if f_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                try: os.remove(os.path.join(target_dir, f_name))
                except: pass
        
        ext = os.path.splitext(file_path)[1]
        seo_name = self.item_data.get('seo_filename', f'image_{self.item_data["id"]}')
        seo_name = re.sub(r'\.(jpe?g|png|webp)$', '', seo_name, flags=re.IGNORECASE)
        
        new_file_name = f"{seo_name}{ext}"
        new_file_path = os.path.join(target_dir, new_file_name)
        txt_file_path = os.path.join(target_dir, f"{seo_name}.txt")
        
        try:
            shutil.copy(file_path, new_file_path)
            
            thumb_dir = os.path.join(WORKSPACE_DIR, THUMBNAILS_FOLDER)
            os.makedirs(thumb_dir, exist_ok=True)
            thumb_path = os.path.join(thumb_dir, f"{self.item_data['id']:03d}.jpg")
            reader = QImageReader(new_file_path)
            reader.setScaledSize(QSize(150, 150))
            img = reader.read()
            if not img.isNull():
                img.save(thumb_path, "JPG", 85)
            
            self.main_window.picked_download_files.add(os.path.abspath(file_path))
            self.main_window.save_picked_files()
            
            with open(txt_file_path, 'w', encoding='utf-8') as f:
                f.write(f"Title: {self.item_data.get('title', '')}\n\n")
                f.write(f"Prompt: {self.item_data.get('prompt', '')}\n\n")
                f.write(f"Keywords: {self.item_data.get('keywords', '')}\n\n")
                f.write(f"Category: {self.item_data.get('category', '')}\n")
                f.write(f"Aspect Ratio: {self.item_data.get('aspect_ratio', '')}\n")
                f.write(f"SEO File Name: {seo_name}\n")
                
            self.main_window.refresh_lists()
            QTimer.singleShot(400, self.close) 
        except Exception as e:
            self.status_label.setText(t("err_save"))
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #EF4444;")
            self.timer.start(1000)

class DetailPopup(QDialog):
    def __init__(self, entry_data, entry_id, main_window=None):
        super().__init__()
        self.entry_id = entry_id
        self.main_window = main_window
        self.setWindowTitle(f"{t('detail_title')} ({entry_data.get('seo_filename', 'Item')})")
        if os.path.exists(ICON_FILE):
            self.setWindowIcon(QIcon(ICON_FILE))
            
        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)
            
        self.resize(800, 650)
        
        layout = QVBoxLayout()
        layout.setSpacing(8) 

        layout.addLayout(self.create_copyable_field(t("prompt_lbl"), entry_data.get('prompt', ''), is_red=True))
        layout.addLayout(self.create_copyable_field(t("title_lbl"), entry_data.get('title', '')))
        layout.addLayout(self.create_copyable_field(t("keywords_lbl"), entry_data.get('keywords', '')))

        buttons_layout = QHBoxLayout()
        self.copy_link_btn = QPushButton(t("copy_link"))
        self.copy_link_btn.setIcon(qta.icon('fa5s.link', color='white'))
        self.copy_link_btn.setFixedHeight(40)
        self.copy_link_btn.setStyleSheet("background-color: #3B82F6; color: white; font-size: 14px; font-weight: bold; border-radius: 6px;")
        self.copy_link_btn.clicked.connect(self.copy_folder_link)
        
        open_btn = QPushButton(t("open_folder"))
        open_btn.setIcon(qta.icon('fa5s.folder-open', color='white'))
        open_btn.setFixedHeight(40)
        open_btn.setStyleSheet("background-color: #3B82F6; color: white; font-size: 14px; font-weight: bold; border-radius: 6px;")
        open_btn.clicked.connect(self.open_folder)
        
        buttons_layout.addWidget(self.copy_link_btn)
        buttons_layout.addWidget(open_btn)
        layout.addLayout(buttons_layout)

        category_text = entry_data.get('category', 'Not Available')
        cat_label = QLabel(f"<b>{t('category_lbl')}:</b>  {category_text}")
        cat_label.setStyleSheet("font-size: 14px; padding: 6px; color: #1F2937; background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 4px;")
        layout.addWidget(cat_label)
        
        dropzone_header_layout = QHBoxLayout()
        dropzone_header_layout.addStretch()
        
        self.browse_btn = QPushButton(t("browse_manual"))
        self.browse_btn.setIcon(qta.icon('fa5s.search', color='white'))
        self.browse_btn.setStyleSheet("background-color: #3B82F6; color: white; padding: 6px 12px; font-weight: bold; border-radius: 6px;")
        self.browse_btn.setCursor(Qt.PointingHandCursor)
        dropzone_header_layout.addWidget(self.browse_btn)

        self.replace_btn = QPushButton(t("replace_img"))
        self.replace_btn.setIcon(qta.icon('fa5s.sync-alt', color='white'))
        self.replace_btn.setStyleSheet("background-color: #6B7280; color: white; padding: 6px 12px; font-weight: bold; border-radius: 6px;")
        self.replace_btn.setCursor(Qt.PointingHandCursor)
        dropzone_header_layout.addWidget(self.replace_btn)
        layout.addLayout(dropzone_header_layout)

        self.drop_zone = DropZone(entry_data, entry_id, self)
        self.browse_btn.clicked.connect(self.drop_zone.browse_file)
        self.replace_btn.clicked.connect(self.drop_zone.browse_file)
        self.drop_zone.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
        layout.addWidget(self.drop_zone)

        self.setLayout(layout)

    def create_copyable_field(self, label_text, text_value, is_red=False):
        row_layout = QHBoxLayout()
        if is_red:
            lbl = QLabel(f'<b style="color: #DC2626;">{label_text}:</b>')
        else:
            lbl = QLabel(f'<b style="color: #374151;">{label_text}:</b>')
            
        lbl.setFixedWidth(70)
        lbl.setStyleSheet("font-size: 13px;")
        
        txt_box = QTextEdit(text_value)
        txt_box.setReadOnly(True)
        txt_box.setFixedHeight(60) 
        txt_box.setStyleSheet("background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 4px; color: #1F2937; font-size: 13px;")
        
        copy_btn = CopyButton(text_value)
        
        row_layout.addWidget(lbl)
        row_layout.addWidget(txt_box)
        row_layout.addWidget(copy_btn)
        return row_layout

    def copy_folder_link(self):
        subfolder_name = f"{self.entry_id:03d}"
        target_dir = os.path.abspath(os.path.join(WORKSPACE_DIR, OUTPUT_FOLDER, subfolder_name))
        os.makedirs(target_dir, exist_ok=True) 
        QApplication.clipboard().setText(target_dir)
        self.copy_link_btn.setText(t("copied"))
        self.copy_link_btn.setIcon(qta.icon('fa5s.check', color='white'))
        self.copy_link_btn.setStyleSheet("background-color: #10B981; color: white; font-size: 14px; font-weight: bold; border-radius: 6px;")
        QTimer.singleShot(1500, self.reset_copy_link_btn)

    def reset_copy_link_btn(self):
        self.copy_link_btn.setText(t("copy_link"))
        self.copy_link_btn.setIcon(qta.icon('fa5s.link', color='white'))
        self.copy_link_btn.setStyleSheet("background-color: #3B82F6; color: white; font-size: 14px; font-weight: bold; border-radius: 6px;")

    def open_folder(self):
        subfolder_name = f"{self.entry_id:03d}"
        target_dir = os.path.abspath(os.path.join(WORKSPACE_DIR, OUTPUT_FOLDER, subfolder_name))
        os.makedirs(target_dir, exist_ok=True) 
        QDesktopServices.openUrl(QUrl.fromLocalFile(target_dir))

class ListItemWidget(QWidget):
    def __init__(self, item_data, main_window, img_path=None):
        super().__init__()
        self.item_data = item_data
        self.main_window = main_window
        
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)
        
        self.thumb_label = QLabel()
        self.thumb_label.setFixedSize(36, 30)
        self.thumb_label.setStyleSheet("border-radius: 4px; border: 1px solid #D1D5DB; background-color: #F3F4F6;")
        self.thumb_label.setAlignment(Qt.AlignCenter)
        
        if img_path:
            pixmap = QPixmap(img_path).scaled(36, 30, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            self.thumb_label.setPixmap(pixmap)
        else:
            self.thumb_label.setPixmap(qta.icon('fa5s.image', color='#9CA3AF').pixmap(20, 20))
            
        layout.addWidget(self.thumb_label)
        
        display_text = f"{item_data['id']}. {item_data.get('seo_filename', 'Unknown')}"
        if item_data.get('status') == 'uploaded' and 'upload_date' in item_data:
            display_text += f"   <span style='color:#6B7280; font-size:12px; font-style:normal;'> | {item_data['upload_date']}</span>"
            
        lbl = QLabel(display_text)
        lbl.setTextFormat(Qt.RichText)
        
        if item_data.get('status') == 'uploaded':
            lbl.setStyleSheet("font-size: 14px; font-weight: 500; color: #6B7280; font-style: italic; background: transparent;")
        else:
            lbl.setStyleSheet("font-size: 14px; font-weight: 500; color: #1F2937; background: transparent;")
            
        lbl.setMinimumWidth(150)
        lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lbl.setWordWrap(False)
        layout.addWidget(lbl) 
        
        self.search_btn = QPushButton()
        self.search_btn.setIcon(qta.icon('fa5s.robot', color='white'))
        self.search_btn.setToolTip("Copy Prompt & Auto-Pick Image")
        self.search_btn.setStyleSheet("background-color: #3B82F6; border-radius: 4px;")
        self.search_btn.setFixedSize(36, 30)
        self.search_btn.setCursor(Qt.PointingHandCursor)
        self.search_btn.clicked.connect(self.open_auto_search)
        layout.addWidget(self.search_btn)
        
        open_btn = QPushButton()
        open_btn.setIcon(qta.icon('fa5s.folder-open', color='white'))
        open_btn.setToolTip("Open Folder")
        open_btn.setStyleSheet("background-color: #8B5CF6; border-radius: 4px;")
        open_btn.setFixedSize(36, 30)
        open_btn.setCursor(Qt.PointingHandCursor)
        open_btn.clicked.connect(self.open_folder)
        layout.addWidget(open_btn)
        
        if item_data.get('status', 'pending') == 'pending':
            up_btn = QPushButton()
            up_btn.setIcon(qta.icon('fa5s.cloud-upload-alt', color='white'))
            up_btn.setToolTip("Upload")
            up_btn.setStyleSheet("background-color: #10B981; border-radius: 4px;")
            up_btn.clicked.connect(lambda: self.main_window.change_status(self.item_data, 'uploaded'))
        else:
            up_btn = QPushButton()
            up_btn.setIcon(qta.icon('fa5s.undo', color='white'))
            up_btn.setToolTip("Undo Upload")
            up_btn.setStyleSheet("background-color: #F59E0B; border-radius: 4px;")
            up_btn.clicked.connect(lambda: self.main_window.change_status(self.item_data, 'pending'))
        up_btn.setFixedSize(36, 30)
        up_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(up_btn)
        
        del_btn = QPushButton()
        del_btn.setIcon(qta.icon('fa5s.trash-alt', color='white'))
        del_btn.setToolTip("Delete Asset")
        del_btn.setStyleSheet("background-color: #EF4444; border-radius: 4px;")
        del_btn.setFixedSize(36, 30)
        del_btn.setCursor(Qt.PointingHandCursor)
        del_btn.clicked.connect(lambda: self.main_window.delete_item(self.item_data))
        layout.addWidget(del_btn)
        
        self.setLayout(layout)

    def open_auto_search(self):
        dialog = AutoSearchDialog(self.item_data, self.main_window)
        dialog.exec_()

    def open_folder(self):
        subfolder_name = f"{self.item_data['id']:03d}"
        target_dir = os.path.abspath(os.path.join(WORKSPACE_DIR, OUTPUT_FOLDER, subfolder_name))
        os.makedirs(target_dir, exist_ok=True) 
        QDesktopServices.openUrl(QUrl.fromLocalFile(target_dir))

    def mouseDoubleClickEvent(self, event):
        self.main_window.open_popup(self.item_data)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.load_app_settings()
        self.setWindowTitle(t("main_title"))
        
        if os.path.exists(ICON_FILE):
            self.setWindowIcon(QIcon(ICON_FILE))
        
        screen_geo = QApplication.primaryScreen().geometry()
        width = int(screen_geo.width() * 0.9)
        height = int(screen_geo.height() * 0.9)
        self.resize(width, height)
        
        frame_gm = self.frameGeometry()
        center_point = QApplication.primaryScreen().availableGeometry().center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())
        
        self.data_list = self.load_data()
        self.picked_download_files = self.load_picked_files()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Height Increased by 10%
        self.header_container = QWidget()
        self.header_container.setFixedHeight(50) 
        header_layout = QHBoxLayout(self.header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.input_label = QLabel(t("paste_label"))
        self.input_label.setStyleSheet("color: #1F2937; font-size: 14px;")
        
        self.info_btn = QPushButton(t("info"))
        self.info_btn.setIcon(qta.icon('fa5s.info-circle', color='white'))
        self.info_btn.setStyleSheet("background-color: #10B981; color: white; padding: 6px 12px; border-radius: 4px; font-weight: bold;")
        self.info_btn.setCursor(Qt.PointingHandCursor)
        self.info_btn.clicked.connect(self.show_format_info)
        
        self.my_prompts_btn = QPushButton(t("prompts_btn"))
        self.my_prompts_btn.setIcon(qta.icon('fa5s.list-alt', color='white'))
        self.my_prompts_btn.setStyleSheet("background-color: #8B5CF6; color: white; padding: 6px 12px; border-radius: 4px; font-weight: bold;")
        self.my_prompts_btn.setCursor(Qt.PointingHandCursor)
        self.my_prompts_btn.clicked.connect(self.open_my_prompts)
        
        self.bmc_btn = QPushButton(t("bmc"))
        self.bmc_btn.setIcon(qta.icon('fa5s.coffee', color='#000000'))
        self.bmc_btn.setStyleSheet("background-color: #FFDD00; color: #000000; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-family: Arial;")
        self.bmc_btn.setCursor(Qt.PointingHandCursor)
        self.bmc_btn.clicked.connect(self.open_bmc)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(list(UI_TEXT.keys()))
        self.lang_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 6px 20px 6px 12px;
                background-color: #FFFFFF;
                color: #1F2937;
                font-weight: bold;
                font-size: 13px;
                min-width: 100px;
            }
            QComboBox:hover { border: 1px solid #3B82F6; }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: none;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                background-color: #FFFFFF;
                selection-background-color: #DBEAFE;
                selection-color: #1E40AF;
                outline: none;
            }
        """)
        idx = self.lang_combo.findText(CURRENT_LANG)
        if idx >= 0: self.lang_combo.setCurrentIndex(idx)
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        
        header_layout.addWidget(self.input_label)
        header_layout.addWidget(self.info_btn)
        header_layout.addStretch()
        header_layout.addWidget(self.my_prompts_btn)
        header_layout.addWidget(self.bmc_btn)
        header_layout.addWidget(self.lang_combo)
        
        main_layout.addWidget(self.header_container)
        
        self.text_input = QTextEdit()
        self.text_input.setFixedHeight(80) 
        self.text_input.setPlaceholderText(t("placeholder"))
        self.text_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #3B82F6; 
                background-color: #FFFFFF; 
                font-size: 14px; 
                padding: 8px;
                border-radius: 6px;
                color: #1F2937;
            }
        """)
        self.text_input.textChanged.connect(self.auto_parse_input)
        main_layout.addWidget(self.text_input)

        lists_layout = QHBoxLayout()
        
        self.pending_group = QGroupBox(t("pending_group"))
        pending_layout = QVBoxLayout()
        self.pending_list = QListWidget()
        self.pending_list.setObjectName("mainList")
        self.pending_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.pending_list.setResizeMode(QListWidget.Adjust)
        pending_layout.addWidget(self.pending_list)
        
        pending_buttons_layout = QHBoxLayout()
        self.upload_all_btn = QPushButton(t("up_all"))
        self.upload_all_btn.setIcon(qta.icon('fa5s.cloud-upload-alt', color='white'))
        self.upload_all_btn.setStyleSheet("background-color: #10B981; color: white; padding: 10px; border-radius: 6px; font-weight: bold;")
        self.upload_all_btn.setCursor(Qt.PointingHandCursor)
        self.upload_all_btn.clicked.connect(self.upload_all_pending)
        
        self.delete_all_pending_btn = QPushButton(t("del_pen"))
        self.delete_all_pending_btn.setIcon(qta.icon('fa5s.trash-alt', color='white'))
        self.delete_all_pending_btn.setStyleSheet("background-color: #EF4444; color: white; padding: 10px; border-radius: 6px; font-weight: bold;")
        self.delete_all_pending_btn.setCursor(Qt.PointingHandCursor)
        self.delete_all_pending_btn.clicked.connect(self.delete_all_pending)
        
        pending_buttons_layout.addWidget(self.upload_all_btn)
        pending_buttons_layout.addWidget(self.delete_all_pending_btn)
        pending_layout.addLayout(pending_buttons_layout)
        self.pending_group.setLayout(pending_layout)
        
        self.uploaded_group = QGroupBox(t("uploaded_group"))
        self.uploaded_group.setStyleSheet("QGroupBox { color: #059669; font-weight: bold; }")
        uploaded_layout = QVBoxLayout()
        self.uploaded_list = QListWidget()
        self.uploaded_list.setObjectName("mainList")
        self.uploaded_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.uploaded_list.setResizeMode(QListWidget.Adjust)
        uploaded_layout.addWidget(self.uploaded_list)
        
        uploaded_buttons_layout = QHBoxLayout()
        uploaded_buttons_layout.addStretch()
        self.delete_all_uploaded_btn = QPushButton(t("del_upl"))
        self.delete_all_uploaded_btn.setIcon(qta.icon('fa5s.trash-alt', color='white'))
        self.delete_all_uploaded_btn.setStyleSheet("background-color: #EF4444; color: white; padding: 10px; border-radius: 6px; font-weight: bold;")
        self.delete_all_uploaded_btn.setCursor(Qt.PointingHandCursor)
        self.delete_all_uploaded_btn.clicked.connect(self.delete_all_uploaded)
        
        uploaded_buttons_layout.addWidget(self.delete_all_uploaded_btn)
        uploaded_layout.addLayout(uploaded_buttons_layout)
        self.uploaded_group.setLayout(uploaded_layout)
        
        lists_layout.addWidget(self.pending_group)
        lists_layout.addWidget(self.uploaded_group)
        main_layout.addLayout(lists_layout)
        
        self.export_btn = QPushButton(t("export_csv"))
        self.export_btn.setIcon(qta.icon('fa5s.file-export', color='white'))
        self.export_btn.setStyleSheet("background-color: #F59E0B; color: white; padding: 12px; font-weight: bold; border-radius: 6px; font-size: 15px; margin-top: 5px;")
        self.export_btn.setCursor(Qt.PointingHandCursor)
        self.export_btn.clicked.connect(self.export_csv)
        main_layout.addWidget(self.export_btn)

        self.refresh_lists()

    def load_app_settings(self):
        global CURRENT_LANG
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    settings = json.load(f)
                    CURRENT_LANG = settings.get("language", "English")
            except: pass

    def change_language(self):
        global CURRENT_LANG
        CURRENT_LANG = self.lang_combo.currentText()
        
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump({"language": CURRENT_LANG}, f)
        except: pass

        self.setWindowTitle(t("main_title"))
        self.input_label.setText(t("paste_label"))
        self.info_btn.setText(t("info"))
        self.my_prompts_btn.setText(t("prompts_btn"))
        self.bmc_btn.setText(t("bmc"))
        self.text_input.setPlaceholderText(t("placeholder"))
        self.pending_group.setTitle(t("pending_group"))
        self.uploaded_group.setTitle(t("uploaded_group"))
        self.upload_all_btn.setText(t("up_all"))
        self.delete_all_pending_btn.setText(t("del_pen"))
        self.delete_all_uploaded_btn.setText(t("del_upl"))
        self.export_btn.setText(t("export_csv"))

    def open_bmc(self):
        QDesktopServices.openUrl(QUrl("https://buymeacoffee.com/rishichaurasiya"))

    def open_my_prompts(self):
        dialog = MyPromptsDialog(self)
        dialog.exec_()

    def show_format_info(self):
        info_msg = """Ensure your text EXACTLY contains these labels:

Category: Backgrounds / Holidays
Aspect Ratio: 9:16
AI Image Generation Prompt: [Your Prompt]
Adobe Stock Title: [Your Title]
Adobe Stock Keywords: [Your Keywords]
SEO Optimized File Name: [Your-File-Name]"""
        QMessageBox.information(self, "Format Required", info_msg)

    def auto_parse_input(self):
        text = self.text_input.toPlainText()
        
        if "Category:" in text and "SEO Optimized File Name:" in text:
            raw_blocks = text.split("Category:")
            entries_added = 0
            
            for block in raw_blocks:
                if not block.strip():
                    continue
                    
                full_block = "Category:" + block 
                
                if "SEO Optimized File Name:" in full_block:
                    try:
                        data = {}
                        data['category'] = re.search(r'Category:\s*(.*?)(?=Aspect Ratio:)', full_block, re.DOTALL).group(1).strip()
                        data['aspect_ratio'] = re.search(r'Aspect Ratio:\s*(.*?)(?=AI Image Generation Prompt:)', full_block, re.DOTALL).group(1).strip()
                        data['prompt'] = re.search(r'AI Image Generation Prompt:\s*(.*?)(?=Adobe Stock Title:)', full_block, re.DOTALL).group(1).strip()
                        data['title'] = re.search(r'Adobe Stock Title:\s*(.*?)(?=Adobe Stock Keywords:)', full_block, re.DOTALL).group(1).strip()
                        data['keywords'] = re.search(r'Adobe Stock Keywords:\s*(.*?)(?=SEO Optimized File Name:)', full_block, re.DOTALL).group(1).strip()
                        
                        raw_seo_name = re.search(r'SEO Optimized File Name:\s*(.*)', full_block, re.DOTALL).group(1).strip()
                        data['seo_filename'] = re.sub(r'\.(jpe?g|png|webp|gif)$', '', raw_seo_name, flags=re.IGNORECASE)
                        
                        max_id = max([item.get('id', 0) for item in self.data_list], default=0)
                        data['id'] = max_id + 1
                        data['status'] = 'pending'
                        
                        self.data_list.append(data)
                        entries_added += 1
                    except AttributeError:
                        pass 

            if entries_added > 0:
                self.save_data()
                self.refresh_lists()
                
                self.text_input.blockSignals(True) 
                self.text_input.clear()
                self.text_input.blockSignals(False)
                
                self.pending_list.scrollToBottom()

    def refresh_lists(self):
        pending_scroll = self.pending_list.verticalScrollBar().value()
        uploaded_scroll = self.uploaded_list.verticalScrollBar().value()

        self.pending_list.clear()
        self.uploaded_list.clear()
        
        for item in self.data_list:
            list_w = self.pending_list if item.get('status') == 'pending' else self.uploaded_list
            
            target_dir = os.path.join(WORKSPACE_DIR, OUTPUT_FOLDER, f"{item['id']:03d}")
            thumb_path = os.path.join(WORKSPACE_DIR, THUMBNAILS_FOLDER, f"{item['id']:03d}.jpg")
            
            has_img = False
            img_path_to_display = None
            
            if os.path.exists(thumb_path):
                has_img = True
                img_path_to_display = thumb_path
            elif os.path.exists(target_dir):
                try:
                    with os.scandir(target_dir) as it:
                        for entry in it:
                            if entry.is_file() and entry.name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                                has_img = True
                                thumb_dir = os.path.join(WORKSPACE_DIR, THUMBNAILS_FOLDER)
                                os.makedirs(thumb_dir, exist_ok=True)
                                reader = QImageReader(entry.path)
                                reader.setScaledSize(QSize(150, 150))
                                img = reader.read()
                                if not img.isNull():
                                    img.save(thumb_path, "JPG", 85)
                                img_path_to_display = thumb_path
                                break
                except: pass

            qitem = QListWidgetItem(list_w)
            custom_widget = ListItemWidget(item, self, img_path_to_display)
            qitem.setSizeHint(custom_widget.sizeHint())
            
            if item.get('status', 'pending') == 'pending' and has_img:
                qitem.setBackground(QColor("#D1FAE5"))
            
            list_w.setItemWidget(qitem, custom_widget)

        self.pending_list.verticalScrollBar().setValue(pending_scroll)
        self.uploaded_list.verticalScrollBar().setValue(uploaded_scroll)

    def change_status(self, item_data, new_status):
        item_data['status'] = new_status
        if new_status == 'uploaded':
            item_data['upload_date'] = datetime.now().strftime("%d/%m/%Y")
        self.save_data()
        self.refresh_lists()

    def upload_all_pending(self):
        reply = QMessageBox.question(self, 'Confirm Upload', "Continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for item in self.data_list:
                if item.get('status', 'pending') == 'pending':
                    item['status'] = 'uploaded'
                    item['upload_date'] = datetime.now().strftime("%d/%m/%Y")
            self.save_data()
            self.refresh_lists()

    def delete_all_pending(self):
        reply = QMessageBox.question(self, 'Confirm Delete', "Continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.bulk_delete_by_status('pending')

    def delete_all_uploaded(self):
        reply = QMessageBox.question(self, 'Confirm Delete', "Continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.bulk_delete_by_status('uploaded')

    def bulk_delete_by_status(self, status):
        items_to_delete = [item for item in self.data_list if item.get('status', 'pending') == status]
        for item in items_to_delete:
            subfolder_name = f"{item['id']:03d}"
            src_dir = os.path.abspath(os.path.join(WORKSPACE_DIR, OUTPUT_FOLDER, subfolder_name))
            if os.path.exists(src_dir):
                os.makedirs(os.path.join(WORKSPACE_DIR, DELETED_FOLDER), exist_ok=True)
                dest_dir = os.path.abspath(os.path.join(WORKSPACE_DIR, DELETED_FOLDER, f"{subfolder_name}_{item.get('seo_filename')}"))
                shutil.move(src_dir, dest_dir)
            
            thumb_path = os.path.join(WORKSPACE_DIR, THUMBNAILS_FOLDER, f"{item['id']:03d}.jpg")
            if os.path.exists(thumb_path): os.remove(thumb_path)
                
        self.data_list = [item for item in self.data_list if item.get('status', 'pending') != status]
        self.save_data()
        self.refresh_lists()

    def delete_item(self, item_data):
        subfolder_name = f"{item_data['id']:03d}"
        src_dir = os.path.abspath(os.path.join(WORKSPACE_DIR, OUTPUT_FOLDER, subfolder_name))
        
        if os.path.exists(src_dir):
            os.makedirs(os.path.join(WORKSPACE_DIR, DELETED_FOLDER), exist_ok=True)
            dest_dir = os.path.abspath(os.path.join(WORKSPACE_DIR, DELETED_FOLDER, f"{subfolder_name}_{item_data.get('seo_filename')}"))
            shutil.move(src_dir, dest_dir)
        
        thumb_path = os.path.join(WORKSPACE_DIR, THUMBNAILS_FOLDER, f"{item_data['id']:03d}.jpg")
        if os.path.exists(thumb_path): os.remove(thumb_path)
            
        self.data_list = [i for i in self.data_list if i.get('id') != item_data.get('id')]
        self.save_data()
        self.refresh_lists()

    def open_popup(self, item_data):
        popup = DetailPopup(item_data, item_data['id'], main_window=self)
        popup.exec_()

    def get_category_id(self, cat_text):
        if not cat_text: 
            return ''
        cat_text = cat_text.lower()
        mapping = {
            'animal': 1, 'building': 2, 'architecture': 2, 'business': 3, 
            'drink': 4, 'environment': 5, 'mind': 6, 'food': 7, 
            'graphic': 8, 'hobbies': 9, 'leisure': 9, 'industry': 10, 
            'landscape': 11, 'background': 11, 'lifestyle': 12, 'people': 13, 
            'plant': 14, 'flower': 14, 'culture': 15, 'religion': 15, 'holiday': 15,
            'science': 16, 'social': 17, 'sport': 18, 'technology': 19, 
            'transport': 20, 'travel': 21
        }
        for key, val in mapping.items():
            if key in cat_text:
                return val
        return ''

    def export_csv(self):
        export_folder = os.path.join(WORKSPACE_DIR, "Adobe_Stock_Export")
        images_export_folder = os.path.join(export_folder, "Images_To_Upload")
        
        if os.path.exists(export_folder):
            shutil.rmtree(export_folder)
        os.makedirs(images_export_folder, exist_ok=True)
        
        csv_file_path = os.path.join(export_folder, "AdobeStock_Metadata.csv")
        export_count = 0
        
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Filename", "Title", "Keywords", "Category", "Releases"])
            
            for item in self.data_list:
                if item.get('status') == 'pending':
                    subfolder_name = f"{item['id']:03d}"
                    target_dir = os.path.abspath(os.path.join(WORKSPACE_DIR, OUTPUT_FOLDER, subfolder_name))
                    
                    actual_filename = ""
                    actual_filepath = ""
                    if os.path.exists(target_dir):
                        for f in os.listdir(target_dir):
                            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                                actual_filename = f
                                actual_filepath = os.path.join(target_dir, f)
                                break
                                
                    if actual_filename and actual_filepath:
                        shutil.copy(actual_filepath, os.path.join(images_export_folder, actual_filename))
                        cat_id = self.get_category_id(item.get('category', ''))
                        writer.writerow([actual_filename, item.get('title', ''), item.get('keywords', ''), cat_id, ''])
                        export_count += 1
        
        if export_count > 0:
            QMessageBox.information(self, "Export Successful", f"✅ CSV & Images Ready!\n{export_count} assets packed securely.\nFolder: Adobe_Stock_Export")
            QDesktopServices.openUrl(QUrl.fromLocalFile(export_folder))

    def load_picked_files(self):
        if os.path.exists(PICKED_DATA_FILE):
            try:
                with open(PICKED_DATA_FILE, 'r') as f:
                    return set(json.load(f))
            except: pass
        return set()

    def save_picked_files(self):
        with open(PICKED_DATA_FILE, 'w') as f:
            json.dump(list(self.picked_download_files), f)

    def load_data(self):
        data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                
        for index, item in enumerate(data):
            if 'id' not in item:
                item['id'] = index + 1
            if 'status' not in item:
                item['status'] = 'pending'
        return data

    def save_data(self, f_path=DATA_FILE):
        with open(f_path, 'w') as f:
            json.dump(self.data_list, f, indent=4)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app.setStyle("Fusion")
    
    app.setStyleSheet("""
        QWidget {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: #F3F4F6;
            color: #1F2937;
        }
        QGroupBox {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            margin-top: 15px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
        QListWidget {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 6px;
        }
        QListWidget#mainList::item:selected {
           background-color: #DBEAFE; 
           color: #1E40AF; 
        }
        QScrollBar:vertical {
            border: none;
            background: transparent;
            width: 10px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #9CA3AF;
            min-height: 30px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical:hover {
            background: #6B7280;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
    """)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())