import tkinter as tk
from tkinter import filedialog, messagebox

def decodificar_instruccion(instruccion):
    opcode = "0110011" 
    partes = instruccion.replace(",", "").split()
    if len(partes) != 4:
        raise ValueError(f"Formato inválido: {instruccion}")
    
    operacion, rd, rs1, rs2 = partes
    rd = f"{int(rd[1:]):05b}"
    rs1 = f"{int(rs1[1:]):05b}"
    rs2 = f"{int(rs2[1:]):05b}"
    
    if operacion == "add":
        funct3 = "000"
        funct7 = "0000000"
    elif operacion == "sub":
        funct3 = "000"
        funct7 = "0100000"
    elif operacion == "and":
        funct3 = "111"
        funct7 = "0000000"
    elif operacion == "or":
        funct3 = "110"
        funct7 = "0000000"
    elif operacion == "slt":
        funct3 = "010"
        funct7 = "0000000"
    else:
        raise ValueError(f"Instrucción no soportada: {operacion}")
    
    return f"{funct7}{rs2}{rs1}{funct3}{rd}{opcode}"

def procesar_archivo():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos ASM", "*.asm")])
    if not ruta_archivo:
        return

    try:
        with open(ruta_archivo, "r") as archivo:
            lineas = archivo.readlines()

        instrucciones_binarias = []
        for linea in lineas:
            linea = linea.strip()
            if not linea or linea.startswith("#"):  
                continue
            instrucciones_binarias.append(decodificar_instruccion(linea))

        mostrar_resultados(instrucciones_binarias)

    except Exception as e:
        messagebox.showerror("Error", f"Error al procesar el archivo: {e}")

def mostrar_resultados(instrucciones_binarias):
    resultados_text.delete("1.0", tk.END)
    resultados_text.insert(tk.END, "\n".join(instrucciones_binarias))
    messagebox.showinfo("Éxito", "Archivo procesado correctamente. ¡Revisa los resultados!")

def guardar_resultados():
    contenido = resultados_text.get("1.0", tk.END).strip()
    if not contenido:
        messagebox.showerror("Error", "No hay resultados para guardar.")
        return

    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos TXT", "*.txt")])
    if not ruta_archivo:
        return

    try:
        with open(ruta_archivo, "w") as archivo:
            archivo.write(contenido)
        messagebox.showinfo("Éxito", f"Archivo guardado en: {ruta_archivo}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar el archivo: {e}")

ventana = tk.Tk()
ventana.title("Decodificador ASM a Binario")
ventana.geometry("600x400")

titulo_label = tk.Label(ventana, text="Decodificador ASM a Binario", font=("Arial", 16))
titulo_label.pack(pady=10)

boton_procesar = tk.Button(ventana, text="Cargar y Decodificar Archivo .ASM", command=procesar_archivo)
boton_procesar.pack(pady=5)

resultados_label = tk.Label(ventana, text="Resultados Binarios:")
resultados_label.pack(pady=5)

resultados_text = tk.Text(ventana, height=15, width=70)
resultados_text.pack(pady=5)

boton_guardar = tk.Button(ventana, text="Guardar Resultados", command=guardar_resultados)
boton_guardar.pack(pady=5)

ventana.mainloop()
