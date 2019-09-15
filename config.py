# -*- coding: utf-8 -*-

from enum import Enum

token = "834392596:AAHAsAKIAozSY0pv4uODDLOZRYwnhNg_qwI"
db_file = "database.vdb"
DiscussionId = -389743199

class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_MENU = "1"   # Меню выбора квестов
    S_QUEST_1 = "2"  # Квест (Начало - от Часовни до Перекрестка)
    S_REVIEW = "3" # Ожидание отзыва
    S_QUEST_2 = "4"  # Квест (Граффити)
    S_QUEST_3 = "5"  # Квест (завершение - Камчатка)
