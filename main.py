from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# ----------------------------- CONSTANTS ---------------------------- #
TITLE = """🄿🄷🄾🅃🄾 🅂🅃🄸🄲🄺🄴🅁"""
BANNER = """ᴡᴇʟᴄᴏᴍᴇ sᴛɪᴄᴋ ᴘʜᴏᴛᴏs"""
YELLOW = "#FEFFA7"
MINT_NEON = "#00FF9C"
GREEN_LIGHT = "#B6FFA1"
SUMMER = "#FFE700"
BACKGROUND_COLOR = YELLOW
FONT_NAME = "Helvetica"
LABEL_COLOR = "#fcdc74"
BANNER_FONT = (FONT_NAME, 24,"normal")
BUTTON_FONT = (FONT_NAME, 14, "bold")
SECTION_FONT = (FONT_NAME, 14, "bold")
SELECTION_FONT = (FONT_NAME, 10, "normal")

# ----------------------------- GLOBAL ------------------------------- #
window = Tk(screenName=TITLE)

# ----------------------------- LOGIC -------------------------------- #
def list_img_files():
    """Lista os arquivos de imagem da pasta balões.

        Returns:
            list: Uma lista contendo os nomes dos arquivos de imagem encontrados.
        """
    # Extensões de arquivos de imagem suportadas
    extensoes_imagem = ('.png' , '.pgm' , '.ppm' , '.gif')

    # Lista todos os arquivos no diretório que possuem as extensões de imagem
    arquivos_imagem = [
        arquivo.split('.')[0] for arquivo in os.listdir('Speech Bubble Stickers/')
        if arquivo.lower().endswith(extensoes_imagem)
    ]
    return arquivos_imagem

def save_img(canvas, img_path):
    """Salva a imagem do canvas em um novo arquivo no mesmo diretório."""
    canvas.update()  # Garante que o Canvas está atualizado

    # Captura o nome e o caminho do diretório da imagem original
    diretorio , nome_arquivo = os.path.split(img_path)
    nome_base , extensao = os.path.splitext(nome_arquivo)

    # Define o novo nome do arquivo
    novo_nome_arquivo = f"{nome_base}_sticker.png"
    novo_caminho = os.path.join(diretorio , novo_nome_arquivo)

    # Extrai a imagem do canvas (o conteúdo do canvas é capturado como uma imagem)
    canvas_image = canvas.postscript(file=f"{nome_base}_sticker.eps")  # Salva em formato EPS
    modified_img = Image.open(canvas_image)
    original_img = Image.open(img_path)

    # Redimensiona a imagem modificada para ter o mesmo tamanho da original
    modified_img = modified_img.resize(original_img.size)

    # Converte a imagem EPS para um formato mais compatível (PNG, JPEG)
    img = modified_img.convert('png')

    canvas.destroy()

    # Salva a imagem final no arquivo original
    try:
        img.save(fp=novo_caminho)
    except ValueError:
        messagebox.showerror(message="Output format could not be determined")
    except OSError:
        messagebox.showerror(message="Image file could not be written")
    except Exception as e:
        messagebox.showerror(message=f"Erro inesperado: {e}")


def is_valid_color(color):
    """Função que verifica se a cor é válida"""
    try:
        window.winfo_rgb(color)  # Se a cor for válida, winfo_rgb não levanta exceção
        print(color)
        return True
    except TclError:
        return False

# ----------------------------- UI SETUP ----------------------------- #
def aplication(sticker_font, font_color, sticker ,sticker_text , img_path):
    """Usuário escolhe o lugar de colar o sticker na imagem carregada"""
    reset_window()
    window.config(bg=BACKGROUND_COLOR, padx=10 , pady=40)
    app = Frame(window , bg=BACKGROUND_COLOR , padx=20 , pady=20)
    app.pack()
    try:
        original_image = Image.open(img_path)
        if original_image:
            # Converter para formato compatível com Tkinter
            img_tk = ImageTk.PhotoImage(original_image)

            Label(window, text="Clique na imagem para posicionar o sticker:", bg=BACKGROUND_COLOR, font=SECTION_FONT, fg='black' )

            _x_, _y_ = original_image.size
            # Exibir a imagem no canvas
            canvas = Canvas(app , bg=BACKGROUND_COLOR , width=_x_ , height=_y_ , highlightthickness=0)
            canvas.create_image(0 , 0 , image=img_tk, anchor=NW)
            canvas.photo = img_tk  # Manter a referência da imagem
            canvas.pack()

            def draw_in_canvas(event):
                """Função que desenha o sticker na posição clicada pelo usuário"""
                # Limpar stickers anteriores
                canvas.delete("sticker")  # Remove todos os elementos com a tag 'sticker'
                canvas.delete("sticker_text")  # Remove todos os elementos com a tag 'sticker_text'

                x, y = event.x, event.y #pegar as coordenadas do clique

                # Adicionar o sticker

                current_path = os.path.dirname(os.path.abspath(__file__))  # Caminho da pasta onde o arquivo Python está
                sticker_path = os.path.join(current_path , 'Balões' , f'{sticker}.png')
                canvas.sticker = PhotoImage(file=sticker_path)
                canvas.sticker = canvas.sticker.subsample(2,2)
                canvas.create_image(x , y , image=canvas.sticker, tags="sticker")

                # Adicionar o texto do sticker
                canvas.create_text(
                    x , y ,
                    text=sticker_text ,
                    font=(sticker_font , 11 , 'bold') ,
                    fill=font_color ,
                    tags="sticker_text",
                    justify='center',
                    anchor="center",
                    width= canvas.sticker.width() - 50
                )

            # Conectar a função de desenho ao clique do mouse
            canvas.bind("<Button-1>" , draw_in_canvas)  # O clique esquerdo ativa a função

            # Botão para salvar as alterações feitas no Canvas
            button_save = Button(window , text="Save", command=lambda: save_img(canvas , img_path))
            button_save.config(
                fg='white' ,
                activeforeground="green" ,
                bg="green" ,
                activebackground=MINT_NEON ,
                font=BUTTON_FONT ,
                highlightthickness=0
            )
            button_save.pack(pady=10)

    except FileNotFoundError:
        messagebox.showwarning(message="Nenhuma imagem foi selecionada.")
    except OSError:
        messagebox.showerror(message="Erro ao abrir a imagem. Por favor, verifique se a imagem está "
                             "corrompida ou se o formato é suportado.")
    except Exception as e:
        messagebox.showerror(message=f"Erro inesperado: {e}")


def selection_box():
    """Abre uma caixa de diálogo para selecionar uma imagem e retorna o caminho do arquivo"""
    # Ocultar a janela principal do Tkinter
    box = Frame(window, padx=20, pady=20)

    # Abrir a caixa de seleção de arquivo
    try:
        img_path = filedialog.askopenfilename(
            title="Selecione uma imagem" ,
            filetypes=[("Imagens" , "*.png *.ppm *.pgm *.gif") , ("Todos os arquivos" , "*.*")]
        )
        if not img_path:
            messagebox.showwarning("No file selected")
        else:
            box.destroy()  # Fecha a janela principal após a seleção
            option_menu(img_path)
    except IOError as e:
        messagebox.showerror(message=f"Error opening image file: {e}")
    except ValueError as e:
        messagebox.showerror(message=f"Error format image file: {e}")
    except Exception as e:
        messagebox.showerror(message=f"Error occurred: {e}")

def option_menu(img_path):
    """Cria um menu interativo para escolher fonte, balão de fala e texto."""
    reset_window()  # Limpa a tela para o novo frame

    # Criar o frame principal para o menu
    menu = Frame(window, bg=BACKGROUND_COLOR, padx=20, pady=20)
    menu.grid()

    # ----------------- Seção de escolha da fonte de texto ----------------- #
    label_font = Label(menu, text="Escolha a Fonte de Texto:")
    label_font.config(bg=GREEN_LIGHT, font=SECTION_FONT, fg=MINT_NEON, width=20, anchor='e')
    label_font.grid(row=0, column=0, pady=5, sticky='e')

    fonts = ["Arial", "Comic Sans", "Courier New", "Times New Roman", "Verdana"]
    font_variable = StringVar()
    font_variable.set("Font Options ...")
    dropdown_font = OptionMenu(menu, font_variable, *fonts)
    dropdown_font.config(font=SELECTION_FONT, bg='white', width=23)
    dropdown_font.grid(row=0, column=1, padx=10)

    # ----------------- Seção de entrada da cor ----------------- #
    label_color = Label(menu , text="Text Color:")
    label_color.config(bg=GREEN_LIGHT , font=SECTION_FONT , fg=MINT_NEON, width=20, anchor='e')
    label_color.grid(row=1 , column=0 , pady=5 , sticky='e')

    # Configurar o campo de entrada da cor com validação
    color_text = Entry(menu)
    color_text.config(width=30, font=SELECTION_FONT)
    color_text.grid(row=1 , column=1 , padx=10)

    # ----------------- Seção de escolha do balão de fala ----------------- #
    label_sticker = Label(menu, text="Choose Sticker:")
    label_sticker.config(bg=GREEN_LIGHT, font=SECTION_FONT, fg=MINT_NEON, width=20, anchor='e')
    label_sticker.grid(row=2, column=0, pady=5, sticky='e')

    list_stickers = list_img_files()  # Obtém a lista de balões de fala
    sticker_variable = StringVar()
    sticker_variable.set("Sticker Options ...")
    dropdown_stickers = OptionMenu(menu, sticker_variable, *list_stickers)
    dropdown_stickers.config(font=SELECTION_FONT, bg='white', width=23)
    dropdown_stickers.grid(row=2, column=1, padx=10)

    # ----------------- Seção de entrada do texto do balão ----------------- #
    label_text = Label(menu, text="Sticker text:")
    label_text.config(bg=GREEN_LIGHT, font=SECTION_FONT, fg=MINT_NEON, width=20, anchor='e')
    label_text.grid(row=3, column=0, pady=10, sticky='e')

    entry_text = Entry(menu)
    entry_text.config(width=30, disabledbackground='', font=SELECTION_FONT)
    entry_text.insert(0, 'Entry your text here...')
    entry_text.grid(row=3, column=1, padx=10)


    # ----------------- Botão para enviar as informações ----------------- #
    def send_info():

        """Função que coleta as informações preenchidas pelo usuário."""
        color = color_text.get()
        if is_valid_color(color):
            selected_font = font_variable.get()
            selected_sticker = sticker_variable.get()
            text = entry_text.get()
            aplication(sticker_font=selected_font, font_color=color, sticker=selected_sticker, sticker_text=text, img_path=img_path)
            menu.destroy()
        else:
            messagebox.showwarning("Cor Inválida" , f"'{color}' não é uma cor válida.")

    button_next = Button(menu, text="Next  ->", command=send_info)
    button_next.config(
        fg='white' ,
        activeforeground="green" ,
        bg="green" ,
        activebackground=MINT_NEON ,
        font=BUTTON_FONT ,
        highlightthickness=0
    )
    button_next.grid(row=4, column=1)


def reset_window():
    for widget in window.winfo_children():
        widget.destroy()

def page_menu():
    """ Criar um menu interativo para o usuário fazer upload de imagens"""
    # Configurar o menu container
    reset_window()
    menu = Frame(window, bg=BACKGROUND_COLOR, padx=20, pady=20)
    menu.grid()

    # Load upload icon / Keep the image reference within the canvas scope
    canvas = Canvas(menu, bg=BACKGROUND_COLOR, width=350 , height=350, highlightthickness=0)
    upload_icon = PhotoImage(file="upload.png")
    canvas.resized_image = upload_icon.subsample(2 , 2)  # Divide a largura e a altura por 2
    canvas.create_image(175,175,image = canvas.resized_image)

    banner = Label(menu, text=BANNER, fg=MINT_NEON, font=BANNER_FONT,  bg=BACKGROUND_COLOR)

    select_button = Button(menu , text="Select Image", command=selection_box)
    select_button.config(
        fg='white',
        activeforeground="green",
        bg = "green",
        activebackground= MINT_NEON,
        font = BUTTON_FONT,
        highlightthickness=0
    )

    # Set widgets positions
    banner.grid(column=0 , row=0)
    canvas.grid(column=0 , row=1)
    select_button.grid(column=0 , row=2)

if __name__ == "__main__":
    page_menu()

window.mainloop()
