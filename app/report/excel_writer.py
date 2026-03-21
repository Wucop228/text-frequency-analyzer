from openpyxl import Workbook

def create_report_xlsx(word_stats: dict[str, dict], output_path: str):
    wb = Workbook()
    sheet = wb.active
    sheet.title = "Word Stats"

    sheet.append(["словоформа", "кол-во данной словоформы во всём документе", "кол-во словоформ в каждой строке"])

    for word, stat in word_stats.items():
        per_line_str = ",".join(str(n) for n in stat["per_line"])
        sheet.append([word, stat["total"], per_line_str])

    wb.save(output_path)