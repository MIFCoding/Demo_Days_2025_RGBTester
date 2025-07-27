import os
from pathlib import Path
from datetime import datetime

from color import *

def generate_html_report(results):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"test_report_{timestamp}.html"
    
    def truncate(text, max_len=300):
        if not isinstance(text, str):
            text = str(text)
        return text[:max_len] + ('...' if len(text) > max_len else '')
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Отчет тестирования аудио кодека</title>
        <style>
            :root {{
                --green: #4CAF50;
                --yellow: #FFC107;
                --magenta: #9C27B0;
                --red: #F44336;
                --gray: #f0f0f0;
                --dark: #2c3e50;
            }}
            
            * {{
                box-sizing: border-box;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            body {{
                margin: 0;
                padding: 20px;
                background-color: #fafafa;
                color: #333;
                line-height: 1.6;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            
            header {{
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 1px solid #ddd;
            }}
            
            h1, h2, h3, h4 {{
                color: var(--dark);
                margin-top: 0;
            }}
            
            .summary {{
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                margin-bottom: 30px;
                overflow: hidden;
            }}
            
            .summary-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
                padding: 20px;
            }}
            
            .summary-card {{
                background: white;
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                text-align: center;
                border-left: 4px solid;
            }}
            
            .group-accordion {{
                margin-bottom: 20px;
            }}
            
            .accordion-header {{
                background: var(--dark);
                color: white;
                padding: 15px 20px;
                cursor: pointer;
                border-radius: 4px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-weight: bold;
            }}
            
            .accordion-content {{
                background: white;
                border-radius: 0 0 4px 4px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                display: none;
                padding: 20px;
                overflow-x: auto;
            }}
            
            .string-card {{
                background: white;
                border-radius: 4px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                margin-bottom: 15px;
                overflow: hidden;
            }}
            
            .string-header {{
                padding: 12px 15px;
                background: var(--gray);
                cursor: pointer;
                display: flex;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 10px;
            }}
            
            .string-info {{
                flex: 1;
                min-width: 0;
            }}
            
            .original-text {{
                font-family: monospace;
                background: #f5f5f5;
                padding: 2px 5px;
                border-radius: 3px;
                display: inline-block;
                max-width: 100%;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            
            .test-results {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 15px;
                padding: 15px;
            }}
            
            .test-card {{
                padding: 12px;
                border-radius: 4px;
                border-left: 3px solid;
                background: #f9f9f9;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }}
            
            .text-comparison {{
                display: flex;
                flex-direction: column;
                gap: 5px;
                margin: 10px 0;
            }}
            
            .decoded-text {{
                font-family: monospace;
                background: #f0f8ff;
                padding: 2px 5px;
                border-radius: 3px;
                display: inline-block;
                max-width: 100%;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            
            .percent {{
                font-weight: bold;
                font-size: 1.1em;
            }}
            
            .success {{ color: var(--green); }}
            .warning {{ color: var(--yellow); }}
            .danger {{ color: var(--red); }}
            .critical {{ color: var(--magenta); }}
            
            .error {{
                color: var(--red);
                font-weight: bold;
                background: #ffebee;
                padding: 2px 5px;
                border-radius: 3px;
            }}
            
            .diff-easy {{ border-color: var(--green); }}
            .diff-medium {{ border-color: var(--yellow); }}
            .diff-hard {{ border-color: var(--magenta); }}
            .diff-extreme {{ border-color: var(--red); }}
            
            @media (max-width: 768px) {{
                .test-results {{
                    grid-template-columns: 1fr;
                }}
                
                .summary-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Отчет тестирования аудио кодека</h1>
                <p>Тестирование завершено: {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</p>
            </header>
            
            <section class="summary">
                <h2 style="padding: 15px 20px 0 20px; margin-bottom: 0;">Сводка результатов</h2>
                <div class="summary-grid">
    """

    for group, data in results.items():
        success_rate = data["success_rate"]
        color_class = "success" if success_rate >= 0.9 else (
            "warning" if success_rate >= 0.8 else (
                "critical" if success_rate >= 0.7 else "danger"
            )
        )
        
        html_content += f"""
        <div class="summary-card">
            <h3>Группа {group} символов</h3>
            <div class="percent {color_class}">{success_rate:.1%}</div>
            <div>{data['successful_tests']} / {data['total_tests']} успешных тестов</div>
        </div>
        """
    
    html_content += """
                </div>
            </section>
            
            <section class="detailed-results">
                <h2>Детализированные результаты</h2>
    """

    for group, data in results.items():
        success_rate = data["success_rate"]
        header_color = (
            "var(--green)" if success_rate >= 0.9 else
            "var(--yellow)" if success_rate >= 0.8 else
            "var(--magenta)" if success_rate >= 0.7 else "var(--red)"
        )
        
        html_content += f"""
        <div class="group-accordion">
            <div class="accordion-header" style="background: {header_color};" onclick="toggleGroup('group-{group}')">
                <span>Группа {group} символов</span>
                <span>{success_rate:.1%} ({data['successful_tests']}/{data['total_tests']})</span>
            </div>
            <div class="accordion-content" id="group-{group}">
        """

        for i, string_data in enumerate(data["details"]):
            total_tests = 1 + len(string_data["noises"])
            success_count = 0
            
            if string_data["clean"] and "success" in string_data["clean"]:
                success_count += 1 if string_data["clean"]["success"] else 0
            
            for noise in string_data["noises"]:
                if "success" in noise and noise["success"]:
                    success_count += 1
            
            success_rate_str = success_count / total_tests
            str_color_class = "success" if success_rate_str >= 0.9 else (
                "warning" if success_rate_str >= 0.8 else (
                    "critical" if success_rate_str >= 0.7 else "danger"
                )
            )
            
            html_content += f"""
            <div class="string-card">
                <div class="string-header" onclick="toggleString('string-{group}-{i}')">
                    <div class="string-info">
                        <strong>Строка #{i+1}:</strong> <span class="original-text" title="{string_data['original']}">{truncate(string_data['original'])}</span>
                    </div>
                    <div class="percent {str_color_class}">{success_rate_str:.0%}</div>
                </div>
                <div class="string-details" id="string-{group}-{i}" style="display: none;">
                    <div class="test-results">
            """

            if string_data["clean"]:
                if "error" in string_data["clean"]:
                    html_content += f"""
                    <div class="test-card">
                        <h4>Чистый сигнал</h4>
                        <div class="error">Ошибка: {truncate(string_data['clean']['error'])}</div>
                    </div>
                    """
                else:
                    sim = string_data["clean"]["similarity"]
                    color_class = "success" if sim >= 0.9 else (
                        "warning" if sim >= 0.8 else (
                            "critical" if sim >= 0.7 else "danger"
                        )
                    )
                    
                    html_content += f"""
                    <div class="test-card">
                        <h4>Чистый сигнал</h4>
                        <div class="text-comparison">
                            <div><strong>Оригинал:</strong> <span class="original-text" title="{string_data['original']}">{truncate(string_data['original'])}</span></div>
                            <div><strong>Декодировано:</strong> <span class="decoded-text" title="{string_data['clean']['decoded']}">{truncate(string_data['clean']['decoded'])}</span></div>
                        </div>
                        <div><strong>Сходство:</strong> <span class="percent {color_class}">{sim:.1%}</span></div>
                        <div><strong>Статус:</strong> {'✅ Успех' if string_data['clean']['success'] else '❌ Ошибка'}</div>
                    </div>
                    """

            for noise in string_data["noises"]:
                diff_class = (
                    "diff-easy" if noise["difficulty"] == "easy" else
                    "diff-medium" if noise["difficulty"] == "medium" else
                    "diff-hard" if noise["difficulty"] == "hard" else "diff-extreme"
                )
                
                if "error" in noise:
                    html_content += f"""
                    <div class="test-card {diff_class}">
                        <h4>{noise['name']} ({noise['params']})</h4>
                        <div class="error">Ошибка: {truncate(noise['error'])}</div>
                    </div>
                    """
                else:
                    sim = noise["similarity"]
                    color_class = "success" if sim >= 0.9 else (
                        "warning" if sim >= 0.8 else (
                            "critical" if sim >= 0.7 else "danger"
                        )
                    )
                    
                    html_content += f"""
                    <div class="test-card {diff_class}">
                        <h4>{noise['name']} ({noise['params']})</h4>
                        <div class="text-comparison">
                            <div><strong>Оригинал:</strong> <span class="original-text" title="{string_data['original']}">{truncate(string_data['original'])}</span></div>
                            <div><strong>Декодировано:</strong> <span class="decoded-text" title="{noise['decoded']}">{truncate(noise['decoded'])}</span></div>
                        </div>
                        <div><strong>Сходство:</strong> <span class="percent {color_class}">{sim:.1%}</span></div>
                        <div><strong>Статус:</strong> {'✅ Успех' if noise['success'] else '❌ Ошибка'}</div>
                    </div>
                    """
            
            html_content += """
                    </div>
                </div>
            </div>
            """
        
        html_content += """
            </div>
        </div>
        """

    html_content += """
            </section>
        </div>
        
        <script>
            function toggleGroup(groupId) {
                const content = document.getElementById(groupId);
                content.style.display = content.style.display === 'block' ? 'none' : 'block';
            }
            
            function toggleString(stringId) {
                const content = document.getElementById(stringId);
                content.style.display = content.style.display === 'block' ? 'none' : 'block';
            }
            
            // Закрыть все группы при загрузке
            document.addEventListener('DOMContentLoaded', function() {
                document.querySelectorAll('.accordion-content').forEach(el => {
                    el.style.display = 'none';
                });
                document.querySelectorAll('.string-details').forEach(el => {
                    el.style.display = 'none';
                });
            });
        </script>
    </body>
    </html>
    """
    
    # Сохранение отчета
    with open(f"reports/{filename}", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"\n{COLOR_GREEN}Отчёт сохранён как: {os.path.abspath(filename)}{COLOR_RESET}")
    return filename