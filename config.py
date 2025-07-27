from noises import *

# Флаг для тихого режима (без вывода деталей тестов)
SILENT_MODE = True  # Установите в False для подробного вывода

# Флаг для цветного режима тестовых функций (цвет ависит от сложности функции)
RAINBOW_MODE = False  # Установите в True для цветного вывода подробной информации

GROUPS = [1, 10, 100, 1_000, 10_000, 20_000, 30_000]  # Группы тестов с n-ой длинной строки
NUM_STRINGS_PER_GROUP = 5  # Количество тестовых строк на группу

# Конфигурация тестовых функций 
NOISE_TESTS = [
    {
        "name": "Гауссов шум",
        "func": add_gaussian_noise,
        "args": ["mean", "sigma"],
        "tests": [
            {"values": [0.0, 0.05], "difficulty": "легкий"},
            {"values": [0.0, 0.2], "difficulty": "средний"},
            {"values": [0.0, 0.5], "difficulty": "тяжелый"},
            {"values": [0.0, 1], "difficulty": "экстремальный"}
        ]
    },
    {
        "name": "Белый шум",
        "func": add_white_noise,
        "args": ["snr_db"],
        "tests": [
            {"values": [30.0], "difficulty": "легкий"},
            {"values": [15.0], "difficulty": "средний"},
            {"values": [5.0], "difficulty": "тяжелый"},
            {"values": [0.0], "difficulty": "экстремальный"}
        ]
    },
    {
        "name": "Импульсный шум",
        "func": add_impulse_noise,
        "args": ["probability", "amplitude"],
        "tests": [
            {"values": [0.01, 0.5], "difficulty": "средний"},
            {"values": [0.02, 0.8], "difficulty": "тяжелый"},
            {"values": [0.05, 1.0], "difficulty": "экстремальный"}
        ]
    },
    {
        "name": "Реверберация",
        "func": add_reverb,
        "args": ["delay", "decay", "num_echos"],
        "tests": [
            {"values": [0.1, 0.7, 2], "difficulty": "средний"},
            {"values": [0.5, 0.3, 5], "difficulty": "экстремальный"}
        ]
    },
    {
        "name": "Синусоидальный шум",
        "func": add_tonal_noise,
        "args": ["freq", "amplitude"],
        "tests": [
            {"values": [1000.0, 0.05], "difficulty": "легкий"},
            {"values": [2000.0, 0.1], "difficulty": "средний"},
            {"values": [4000.0, 0.2], "difficulty": "тяжелый"},
            {"values": [8000.0, 0.3], "difficulty": "экстремальный"}
        ]
    },
    {
        "name": "Шум сети (AC Hum)",
        "func": add_ac_hum,
        "args": ["base_freq", "amplitude", "num_harmonics"],
        "tests": [
            {"values": [50.0, 0.05, 2], "difficulty": "легкий"},
            {"values": [50.0, 0.1, 3], "difficulty": "средний"},
            {"values": [60.0, 0.2, 4], "difficulty": "тяжелый"},
            {"values": [50.0, 0.3, 5], "difficulty": "экстремальный"}
        ]
    }
]
