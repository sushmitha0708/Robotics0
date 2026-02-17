import tkinter as tk
from tkinter import ttk, messagebox
import math

# ============================================
# Constants
# ============================================

JOINT_DOF = {
    "R": 1,
    "P": 1,
    "H": 1,
    "S": 3,
    "U": 2,
    "C": 2
}

JOINT_CONSTRAINTS = {
    "R": 5,
    "P": 5,
    "H": 5,
    "S": 3,
    "U": 4,
    "C": 4
}

RIGID_BODY_DOF = {
    "Planar": 3,
    "Spatial": 6
}

LINK_LENGTH = 80


# ============================================
# Main GUI
# ============================================

class MobilityAnalyzer:

    def __init__(self, root):

        self.root = root

        # Fixed window size
        self.root.title("Robot Mobility Analyzer")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        self.joint_dropdowns = []

        self.create_layout()


    # ============================================
    # Layout
    # ============================================

    def create_layout(self):

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)


        # LEFT PANEL
        left = tk.Frame(main_frame, width=350)
        left.pack(side="left", fill="y", padx=10)

        title = tk.Label(left,
                         text="Mobility Input",
                         font=("Arial", 16, "bold"))
        title.pack(pady=10)


        tk.Label(left, text="Links (N)").pack()
        self.links_entry = tk.Entry(left)
        self.links_entry.pack()

        tk.Label(left, text="Joints (J)").pack()
        self.joints_entry = tk.Entry(left)
        self.joints_entry.pack()

        tk.Label(left, text="Loops (L)").pack()
        self.loops_entry = tk.Entry(left)
        self.loops_entry.insert(0, "0")
        self.loops_entry.pack()


        tk.Label(left, text="System Type").pack()

        self.type_combo = ttk.Combobox(
            left,
            values=["Planar", "Spatial"],
            state="readonly"
        )
        self.type_combo.current(0)
        self.type_combo.pack()


        tk.Button(left,
                  text="Create Robot",
                  command=self.create_joints,
                  bg="blue",
                  fg="white").pack(pady=10)


        tk.Button(left,
                  text="Analyze Mobility",
                  command=self.analyze,
                  bg="green",
                  fg="white").pack(pady=10)


        # Joint list frame
        self.joint_frame = tk.Frame(left)
        self.joint_frame.pack()


        # RIGHT PANEL
        right = tk.Frame(main_frame)
        right.pack(side="right", fill="both", expand=True)


        # Canvas
        self.canvas = tk.Canvas(
            right,
            width=600,
            height=400,
            bg="white"
        )
        self.canvas.pack(pady=10)


        # Explanation panel
        self.explain = tk.Text(
            right,
            height=15,
            width=70,
            font=("Consolas", 10)
        )
        self.explain.pack()


    # ============================================
    # Create joints
    # ============================================

    def create_joints(self):

        for widget in self.joint_frame.winfo_children():
            widget.destroy()

        self.joint_dropdowns.clear()

        try:
            J = int(self.joints_entry.get())
        except:
            return

        for i in range(J):

            frame = tk.Frame(self.joint_frame)
            frame.pack()

            tk.Label(frame, text=f"Joint {i+1}").pack(side="left")

            combo = ttk.Combobox(
                frame,
                values=list(JOINT_DOF.keys()),
                state="readonly",
                width=5
            )

            combo.current(0)
            combo.pack(side="left")

            combo.bind("<<ComboboxSelected>>",
                       lambda e: self.draw())

            self.joint_dropdowns.append(combo)

        self.draw()


    # ============================================
    # Draw robot with coordinate frames
    # ============================================

    def draw(self):

        self.canvas.delete("all")

        system = self.type_combo.get()

        if system == "Planar":
            link_color = "blue"
            frame_color = "green"
        else:
            link_color = "purple"
            frame_color = "red"

        x = 100
        y = 200

        # Base
        self.canvas.create_rectangle(
            x-20, y-20, x, y+20,
            fill="black")

        for joint in self.joint_dropdowns:

            joint_type = joint.get()

            x_new = x + LINK_LENGTH

            # Link
            self.canvas.create_line(
                x, y, x_new, y,
                width=4,
                fill=link_color
            )

            # Joint symbol
            self.draw_joint(x, y, joint_type)

            # Coordinate frame
            self.draw_frame(x, y, frame_color)

            x = x_new

        # End effector
        self.canvas.create_oval(
            x-6, y-6, x+6, y+6,
            fill="red")

        self.draw_workspace(x, y)


    # ============================================
    # Draw coordinate frame
    # ============================================

    def draw_frame(self, x, y, color):

        size = 20

        self.canvas.create_line(
            x, y,
            x+size, y,
            arrow=tk.LAST,
            fill=color)

        self.canvas.create_line(
            x, y,
            x, y-size,
            arrow=tk.LAST,
            fill=color)

        self.canvas.create_text(
            x+size+10, y,
            text="x",
            fill=color)

        self.canvas.create_text(
            x, y-size-10,
            text="y",
            fill=color)


    # ============================================
    # Draw workspace boundary
    # ============================================

    def draw_workspace(self, x, y):

        radius = LINK_LENGTH * len(self.joint_dropdowns)

        self.canvas.create_oval(
            100-radius,
            200-radius,
            100+radius,
            200+radius,
            dash=(4,2),
            outline="gray"
        )

        self.canvas.create_text(
            100,
            200-radius-10,
            text="Workspace Boundary"
        )


    # ============================================
    # Draw joint symbols
    # ============================================

    def draw_joint(self, x, y, joint):

        if joint == "R":
            self.canvas.create_oval(x-8,y-8,x+8,y+8)

        elif joint == "P":
            self.canvas.create_rectangle(x-8,y-8,x+8,y+8)

        elif joint == "S":
            self.canvas.create_oval(x-8,y-8,x+8,y+8, fill="black")

        elif joint == "U":
            self.canvas.create_line(x-10,y,x+10,y)
            self.canvas.create_line(x,y-10,x,y+10)

        elif joint == "C":
            self.canvas.create_rectangle(x-8,y-8,x+8,y+8)
            self.canvas.create_oval(x-5,y-5,x+5,y+5)

        elif joint == "H":
            self.canvas.create_oval(x-8,y-8,x+8,y+8)


    # ============================================
    # Analyze mobility
    # ============================================

    def analyze(self):

        try:

            N = int(self.links_entry.get())
            J = int(self.joints_entry.get())
            L = int(self.loops_entry.get())

            system = self.type_combo.get()

            m = RIGID_BODY_DOF[system]

            f_sum = sum(
                JOINT_DOF[j.get()]
                for j in self.joint_dropdowns
            )

            constraint_sum = sum(
                JOINT_CONSTRAINTS[j.get()]
                for j in self.joint_dropdowns
            )

            M = m*(N-1-J) + f_sum - m*L

            # Explanation
            text = ""

            text += "GRÜBLER–KUTZBACH MOBILITY ANALYSIS\n"
            text += "----------------------------------\n\n"

            text += f"System type: {system}\n"
            text += f"Rigid body DOF (m): {m}\n\n"

            text += f"Links (N): {N}\n"
            text += f"Joints (J): {J}\n"
            text += f"Loops (L): {L}\n\n"

            text += f"Sum of joint DOF: {f_sum}\n"
            text += f"Total constraints: {constraint_sum}\n\n"

            text += "Mobility equation:\n"
            text += f"M = m(N-1-J) + Σf - mL\n\n"

            text += f"M = {m}({N}-1-{J}) + {f_sum} - {m}({L})\n\n"

            text += f"M = {M}\n"

            self.explain.delete("1.0", tk.END)
            self.explain.insert(tk.END, text)

        except Exception as e:

            messagebox.showerror("Error", str(e))


# ============================================
# Run
# ============================================

root = tk.Tk()

app = MobilityAnalyzer(root)

root.mainloop()
