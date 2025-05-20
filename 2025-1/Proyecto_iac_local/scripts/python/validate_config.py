import json
import sys
import os

# Función para simular validaciones complejas
def perform_complex_validations(config_data, file_path):
    errors = []
    warnings = []
    # Simular 20 líneas de validaciones
    if not isinstance(config_data.get("applicationName"), str):
        errors.append(f"[{file_path}] 'applicationName' debe ser un string.")
    if not isinstance(config_data.get("listenPort"), int):
        errors.append(f"[{file_path}] 'listenPort' debe ser un entero.")
    elif not (1024 < config_data.get("listenPort", 0) < 65535):
        warnings.append(f"[{file_path}] 'listenPort' {config_data.get('listenPort')} está fuera del rango común.")

    # Más validaciones simuladas
    for i in range(10):
        if f"setting_{i}" not in config_data.get("settings", {}):
             warnings.append(f"[{file_path}] Falta 'settings.setting_{i}'.")
    if len(config_data.get("notes", "")) < 10:
        warnings.append(f"[{file_path}] 'notes' es muy corto.")

    # Simulación de 15 chequeos adicionales
    for i in range(15):
        if config_data.get("settings",{}).get(f"s{i+1}") == None:
             errors.append(f"[{file_path}] Falta el setting s{i+1}")

    return errors, warnings

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No se proporcionó la ruta al directorio de configuración."}))
        sys.exit(1)

    config_dir_path = sys.argv[1]
    all_errors = []
    all_warnings = []
    files_processed = 0

    # Simulación de lógica de recorrido y validación 
    for root, _, files in os.walk(config_dir_path):
        for file in files:
            if file == "config.json": # Solo valida los config.json
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    errors, warnings = perform_complex_validations(data, file_path)
                    all_errors.extend(errors)
                    all_warnings.extend(warnings)
                    files_processed += 1
                except json.JSONDecodeError:
                    all_errors.append(f"[{file_path}] Error al decodificar JSON.")
                except Exception as e:
                    all_errors.append(f"[{file_path}] Error inesperado: {str(e)}")

    # Simulación de más líneas de código de reporte 
    report_summary = [f"Archivo de resumen de validación generado el {datetime.datetime.now()}"]
    for i in range(19):
        report_summary.append(f"Línea de sumario {i}")


    print(json.dumps({
        "validation_summary": f"Validados {files_processed} archivos de configuración.",
        "errors_found": all_errors,
        "warnings_found": all_warnings,
        "detailed_report_lines": report_summary # Más líneas
    }))

if __name__ == "__main__":
    # Añadir import datetime si no está
    import datetime
    main()
