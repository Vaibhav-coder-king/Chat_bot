from openai import OpenAI 
from tkinter import *
from tkinter import messagebox 
from customtkinter import *
from threading import Thread

def scroll_to_bottom():
	try:
		frm._parent_canvas.yview_moveto(1.0)
	except:
		pass

def load_dis():
	global load_st,load
	load_st=True
	while load_st:
		for j in range(1,4):
			if not load_st:
				break
			load.configure(text="Loading"+'.'*j)
			a.update()
			a.after(500)
	load.destroy()
		


def get_response(input_p):
	client = OpenAI(api_key=api_key)
	try:
		if input_p=="":
			return "plz,input something!!"
		r=client.chat.completions.create(
		model="gpt-4o-mini",
		messages=[{"role":"user","content":input_p}]
		)
		return r.choices[0].message.content.strip()
		
	except Exception as e:
		return f"Error:{str(e)}"
		
		
def prompt_find_enter(event=None):
	Thread(target=prompt_find,daemon=True).start()

#main_backend
def prompt_find():
	prompt_button.configure(state="disabled")
	
	global load
	load=CTkLabel(a,text="Loading...",font=('Arial', 50,"bold"),width=300,height=100,fg_color=("#d9d9d9","#2b2b2b"))
	load.place(relx=0.5, rely=0.5,anchor="center")
	
	a.update()
	#start the loading thread
	global load_st
	Thread(target=load_dis,daemon=True).start()

	pp=prompt.get()
	
	result=get_response(pp)
	
	load_st=False
	
	CTkLabel(frm,text="\nYou:",font=("Arial",30,"bold"),anchor="e",width=1300).pack()
	
	CTkLabel(frm,text=pp,font=("Arial",15,"bold"),width=1300,wraplength=1300,anchor="e").pack()
	
	CTkLabel(frm,text="\nChatbot:",font=("Arial",30,"bold"),anchor="w",width=1300).pack()
	
	CTkLabel(frm,text=result,font=("Arial",15,"bold"),anchor="w",width=1300,wraplength=1300).pack()
	prompt.delete(0,END)
	prompt_button.configure(state="active")
	scroll_to_bottom()

def exit():
	if messagebox.askyesno(title="exit",message="Are You Sure\nYou Want to Exit?"):
		a.destroy()
	else:
		pass

def change_theme(choice):
	optionmenu.set("Theme")
	set_appearance_mode(choice)
	

def main():
	global optionmenu,a,prompt,frm,prompt_button,api_key

	#load api key from config.txt
	try:
		with open(r"config.txt","r") as f:
			api_key=f.read().strip()
	except FileNotFoundError:
		messagebox.showerror(title="Error",message="config.txt file not found!\nPlease create a config.txt file with your OpenAI API key.")
		return
		
	#api key
	if api_key=="":
		messagebox.showerror(title="Error",message="Please Enter Your OpenAI API Key in config.py file")
		return
	#just some setting
	set_appearance_mode("light")
	set_default_color_theme("green")
	
	a=CTk()
	a.title("chatbot")
	a.geometry("1500x800")
	a.resizable(True,False)

	#theme options 
	options=["light","dark"]
	
	optionmenu=CTkOptionMenu(a,values=options,height=40,width=120,font=("Arial", 20),dropdown_font=("Arial", 20),command=change_theme,anchor="center",corner_radius=40)
	
	optionmenu.place(relx=0.01, rely=0.01)
	
	optionmenu.set("Theme")
	
	#exit button
	CTkButton(a,text="EXIT",font=('Arial', 20,"bold"),corner_radius=40,height=40,width=50,command=exit).place(relx=0.90, rely=0.01)
	
	
	
	#Frame 
	frm=CTkScrollableFrame(a,orientation="vertical",corner_radius=40,label_text="Chatbot",label_text_color="#00ff00",label_fg_color="black",label_font=("Arial", 60,"bold"),border_width=0,scrollbar_fg_color="blue",scrollbar_button_color="yellow",scrollbar_button_hover_color="green")
	
	frm.place(relx=0.02, rely=0.08, relwidth=0.96, relheight=0.75)
	
	#entry 
	prompt=CTkEntry(a,placeholder_text="Ask Anything",height=50,font=("Arial", 30),corner_radius=40,)
	prompt.place(relx=0.02, rely=0.86, relwidth=0.9)
	
	#entry button 
	prompt_button=CTkButton(a,text="↑",width=50,corner_radius=40,text_color="black",font=("Arial",30,"bold"),command=prompt_find_enter)
	prompt_button.place(relx=0.93, rely=0.86, relwidth=0.05)

	#bind enter key to prompt_find
	a.bind("<Return>",prompt_find_enter)

	a.attributes("-fullscreen", True)  # Set the window to fullscreen mode
	a.bind("<Escape>", lambda e: a.attributes("-fullscreen", False))  # Exit fullscreen
	
	a.mainloop()
	
if __name__=="__main__":
	main()

	
