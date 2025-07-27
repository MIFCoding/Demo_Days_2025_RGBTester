import base64
import io
import asyncio

import aiohttp
from Levenshtein import distance as levenshtein_distance
import scipy.io.wavfile as wavfile
import numpy as np

from config import *
from color import *
from html import generate_html_report


BASE_URL = "http://localhost:8000"

MAX_PING_ATTEMPTS = 5
PING_INTERVAL = 1

TIMEOUT = aiohttp.ClientTimeout(total=60)


def generate_test_configs(tests):
    configs = []
    for test in tests:
        for test_case in test["tests"]:
            params = dict(zip(test["args"], test_case["values"]))

            params_str = ", ".join(f"{k}={v}" for k, v in params.items())

            difficulty = test_case["difficulty"]
            color = DIFFICULTY_COLORS.get(difficulty, COLOR_WHITE)

            configs.append({
                "name": test["name"],
                "func": test["func"],
                "params": params,
                "params_str": params_str,
                "difficulty": difficulty,
                "color": color
            })
    return configs


NOISE_CONFIGS = generate_test_configs(NOISE_TESTS)
TOTAL_TESTS_PER_STRING = 1 + len(NOISE_CONFIGS)


async def ping_service(session):
    print(f"{COLOR_CYAN}Проверка доступности сервера {BASE_URL}...{COLOR_RESET}")
    for attempt in range(1, MAX_PING_ATTEMPTS + 1):
        try:
            async with session.get(f"{BASE_URL}/ping") as response:
                if response.status == 200:
                    print(f"{COLOR_GREEN}Сервер доступен!{COLOR_RESET}")
                    return True
                else:
                    print(
                        f"{COLOR_YELLOW}Попытка {attempt}/{MAX_PING_ATTEMPTS}: Сервер вернул статус {response.status}{COLOR_RESET}")
        except aiohttp.ClientError as e:
            print(
                f"{COLOR_YELLOW}Попытка {attempt}/{MAX_PING_ATTEMPTS}: Ошибка подключения - {str(e)}{COLOR_RESET}")

        if attempt < MAX_PING_ATTEMPTS:
            print(
                f"{COLOR_YELLOW}Повторная попытка через {PING_INTERVAL} сек...{COLOR_RESET}")
            await asyncio.sleep(PING_INTERVAL)

    print(f"{COLOR_RED}⚠️  Сервер не ответил после {MAX_PING_ATTEMPTS} попыток. Тесты отменены.{COLOR_RESET}")
    return False


def generate_random_digits_batch(length, count):
    digits = rng.integers(0, 10, size=(count, length), dtype=np.uint8)
    return [''.join(digits[i].astype(str)) for i in range(count)]


def audio_to_base64(audio):
    buffer = io.BytesIO()
    wavfile.write(buffer, 44_100, audio)
    wav_bytes = buffer.getvalue()
    return base64.b64encode(wav_bytes).decode('utf-8')


def base64_to_audio(b64_string):
    wav_bytes = base64.b64decode(b64_string)
    with io.BytesIO(wav_bytes) as wav_buffer:
        _, audio = wavfile.read(wav_buffer)
    return audio


async def encode_string(session, text):
    async with session.post(
        f"{BASE_URL}/encode",
        json={"text": text}
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return data["data"]


async def decode_audio(session, audio_base64):
    async with session.post(
        f"{BASE_URL}/decode",
        json={"data": audio_base64}
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return data["text"]


def calculate_similarity(original, decoded):
    if not original:
        return 0.0
    max_len = max(len(original), len(decoded))
    lev_dist = levenshtein_distance(original, decoded)
    return 1.0 - (lev_dist / max_len)


def normalize_audio(audio):
    if audio.dtype != np.float32:
        return audio.astype(np.float32) / np.iinfo(audio.dtype).max
    return audio


def denormalize_audio(audio_float):
    return (np.clip(audio_float, -1.0, 1.0) * 32767.0).astype(np.int16)


def get_color_for_percent(percent):
    if percent >= 0.9:
        return COLOR_GREEN
    elif percent >= 0.8:
        return COLOR_YELLOW
    elif percent >= 0.7:
        return COLOR_MAGENTA
    else:
        return COLOR_RED


async def run_tests(session):
    results = {}
    detailed_results = {}

    grouped_configs = {}
    for config in NOISE_CONFIGS:
        base_name = config["name"]
        if base_name not in grouped_configs:
            grouped_configs[base_name] = []
        grouped_configs[base_name].append(config)

    for group in GROUPS:
        print(f"\n{COLOR_BOLD}{COLOR_CYAN}=== Тестирование группы {group} символов ==={COLOR_RESET}")
        group_success = 0
        group_total = 0
        group_details = []

        test_strings = generate_random_digits_batch(group, NUM_STRINGS_PER_GROUP)

        for i, original_text in enumerate(test_strings):
            string_results = {
                "original": original_text,
                "clean": None,
                "noises": []
            }

            if SILENT_MODE:
                string_success = 0
                string_completed = 0
                print(f"{COLOR_BOLD}  Строка #{i+1} [0/{TOTAL_TESTS_PER_STRING}]{COLOR_RESET} ", end='', flush=True)
            else:
                print(f"{COLOR_BOLD}  Строка #{i+1}:{COLOR_RESET} ", flush=True)

            try:
                audio_b64 = await encode_string(session, original_text)
                audio_clean = base64_to_audio(audio_b64)
                
                decoded_text = await decode_audio(session, audio_b64)
                similarity = calculate_similarity(original_text, decoded_text)
                
                if similarity >= 0.9:
                    group_success += 1
                    if SILENT_MODE:
                        string_success += 1
                
                group_total += 1
                
                string_results["clean"] = {
                    "decoded": decoded_text,
                    "similarity": similarity,
                    "success": similarity >= 0.9
                }

                if not SILENT_MODE:
                    color = get_color_for_percent(similarity)
                    print(f"  [{COLOR_BOLD}Чистый{COLOR_RESET}: {color}{similarity:.2%}{COLOR_RESET}]\n", flush=True)
                else:
                    string_completed += 1
                    percent = string_success / string_completed if string_completed > 0 else 0.0
                    color = get_color_for_percent(percent)
                    print(f"\r{COLOR_BOLD}  Строка #{i+1} {color}[{string_success}/{string_completed}/{TOTAL_TESTS_PER_STRING}]{COLOR_RESET}    ", end='', flush=True)

            except Exception as e:
                string_results["clean"] = {
                    "error": str(e)
                }
                
                if not SILENT_MODE:
                    print(f"  [{COLOR_BOLD}Чистый{COLOR_RESET}: {COLOR_RED}🚫{COLOR_RESET}]\n", flush=True)
                else:
                    string_completed += 1
                    percent = string_success / string_completed if string_completed > 0 else 0.0
                    color = get_color_for_percent(percent)
                    print(f"\r{COLOR_BOLD}  Строка #{i+1} {color}[{string_success}/{string_completed}/{TOTAL_TESTS_PER_STRING}]{COLOR_RESET}    ", end='', flush=True)

            for base_name, configs in grouped_configs.items():
                if not SILENT_MODE:
                    print(f"  {COLOR_BOLD}{base_name}{COLOR_RESET}:")

                for config in configs:
                    test_result = {
                        "name": config["name"],
                        "params": config["params_str"],
                        "difficulty": config["difficulty"],
                        "color": config["color"]
                    }
                    
                    audio_normalized = normalize_audio(audio_clean.copy())

                    try:
                        audio_noised_float = config["func"](audio_normalized, **config["params"])
                        audio_noised = denormalize_audio(audio_noised_float)
                        noised_b64 = audio_to_base64(audio_noised)
                        
                        decoded_text = await decode_audio(session, noised_b64)
                        similarity = calculate_similarity(original_text, decoded_text)
                        
                        if similarity >= 0.9:
                            group_success += 1
                            if SILENT_MODE:
                                string_success += 1
                        
                        test_result.update({
                            "decoded": decoded_text,
                            "similarity": similarity,
                            "success": similarity >= 0.9
                        })

                        if not SILENT_MODE:
                            color_percent = get_color_for_percent(similarity)
                            print(f"    [{config['color']}{config['params_str']}{COLOR_RESET}: {color_percent}{similarity:.2%}{COLOR_RESET}]")
                    
                    except Exception as e:
                        test_result["error"] = str(e)
                        
                        if not SILENT_MODE:
                            print(f"    [{config['color']}{config['params_str']}{COLOR_RESET}: {COLOR_RED}🚫 (ошибка: {str(e)}){COLOR_RESET}]")

                    group_total += 1
                    string_results["noises"].append(test_result)
                    
                    if SILENT_MODE:
                        string_completed += 1
                        percent = string_success / string_completed if string_completed > 0 else 0.0
                        color = get_color_for_percent(percent)
                        print(f"\r{COLOR_BOLD}  Строка #{i+1} {color}[{string_success}/{string_completed}/{TOTAL_TESTS_PER_STRING}]{COLOR_RESET}    ", end='', flush=True)

                if not SILENT_MODE:
                    print(flush=False)

            if SILENT_MODE:
                percent = string_success / TOTAL_TESTS_PER_STRING
                color = get_color_for_percent(percent)
                print(f"\r{COLOR_BOLD}  Строка #{i+1} {color}[{string_success}/{TOTAL_TESTS_PER_STRING}]{COLOR_RESET}    ", flush=True)
            elif not SILENT_MODE:
                print(end="", flush=True)

            group_details.append(string_results)

        success_rate = group_success / group_total if group_total else 0
        results[group] = {
            "total_tests": group_total,
            "successful_tests": group_success,
            "success_rate": success_rate
        }
        
        detailed_results[group] = {
            "total_tests": group_total,
            "successful_tests": group_success,
            "success_rate": success_rate,
            "details": group_details
        }

        color = get_color_for_percent(success_rate)
        print(f"  {COLOR_BOLD}Результат:{COLOR_RESET} {group_success}/{group_total} ({color}{success_rate:.1%}{COLOR_RESET})")

    print(f"\n{COLOR_BOLD}{COLOR_CYAN}=== Итоговый отчет ==={COLOR_RESET}")
    for group, res in results.items():
        color = get_color_for_percent(res['success_rate'])
        print(f"{COLOR_BOLD}Группа {group}:{COLOR_RESET} {res['successful_tests']}/{res['total_tests']} ({color}{res['success_rate']:.1%}{COLOR_RESET})")

    generate_html_report(detailed_results)
    
    return detailed_results


async def main():
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        if await ping_service(session):
            await run_tests(session)

if __name__ == "__main__":
    try:
        display_heart()
        input()

        asyncio.run(main())
    except KeyboardInterrupt:
        print(
            f"\n{COLOR_RED}{COLOR_BOLD}Программа прервана пользователем.{COLOR_RESET}")
    except Exception as e:
        print(f"\n{COLOR_RED}{COLOR_BOLD}Неожиданная ошибка: {e}{COLOR_RESET}")