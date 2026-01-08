import tkinter as tk

from win import create_win
from utils import show_frames, get_cap, capture, request_portrait, set_name_email

def main():

    cap = get_cap()

    win_cam = create_win("카메라", "480x360+480+0")
    win_capture = create_win("찍힌 사진", "480x360+0+0")
    win_conver = create_win("변환 결과", "480x360+960+0")
    win = create_win("AI Art Portrait", "700x280+480+400")

    label_capture = tk.Label(win_capture)
    label_capture.grid(row=0, column=0)

    label_convert = tk.Label(win_conver)
    label_convert.grid(row=0, column=0)

    frame1 = tk.Frame(win)
    frame1.pack(side='left', fill='y')
    frame2 = tk.Frame(win)
    frame2.pack(side="right", fill='x')

    btn_cap = tk.Button(
        frame2, text="촬영", background="white"
    )
    btn_cap.config(width=30, height=5)
    btn_cap.config(command=lambda: capture(win_capture, cap, label_capture))
    btn_cap.pack(side="top")

    btn_con = tk.Button(
        frame2, text="변환", background="white"
    )
    btn_con.config(width=30, height=5)
    btn_con.config(command=lambda: request_portrait(win_conver, label_convert))
    btn_con.pack(side="bottom")

    label_name = tk.Label(frame1, text="이름")
    label_email = tk.Label(frame1, text="이메일")
    input_name = tk.Entry(
        frame1, width=30, takefocus=True
    )
    input_email = tk.Entry(
        frame1, width=30, takefocus=True
    )
    label_name.pack(side="top")
    input_name.pack(side="top")
    label_email.pack(side="top")
    input_email.pack(side="top")

    cur_name_label = tk.Label(frame1, text="", width=40)
    cur_email_label = tk.Label(frame1, text="", width=40)

    btn_input = tk.Button(
        frame1, text="등록", background="white", 
    )
    btn_input.config(width=30, height=5)
    btn_input.config(
        command=lambda: set_name_email(
            input_name.get(), input_email.get(), 
            cur_name_label, cur_email_label
    ))
    btn_input.pack()

    label = tk.Label(win_cam)
    label.grid(row=0, column=0)

    show_frames(cap, label)

    win.mainloop()

if __name__ == "__main__":
    main()