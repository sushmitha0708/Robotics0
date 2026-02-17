from pyscript import document
import math

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


# canvas
canvas = document.getElementById("robotCanvas")
ctx = canvas.getContext("2d")


joint_types = []


def create_joints():

    container = document.getElementById("joint-container")

    container.innerHTML = ""

    J = int(document.getElementById("joints").value)

    global joint_types

    joint_types = ["R"] * J

    for i in range(J):

        select = document.createElement("select")

        for jt in JOINT_DOF:

            option = document.createElement("option")
            option.text = jt
            select.add(option)

        select.onchange = lambda e, i=i: update_joint(i, e)

        container.appendChild(select)

    draw_robot()


def update_joint(i, event):

    joint_types[i] = event.target.value

    draw_robot()


def draw_robot():

    ctx.clearRect(0,0,700,400)

    system = document.getElementById("system").value

    if system == "Planar":

        link_color = "blue"
        frame_color = "green"

    else:

        link_color = "purple"
        frame_color = "red"

    x = 100
    y = 200

    # base
    ctx.fillRect(x-20,y-20,20,40)

    for jt in joint_types:

        x_new = x + LINK_LENGTH

        # link
        ctx.strokeStyle = link_color
        ctx.lineWidth = 4

        ctx.beginPath()
        ctx.moveTo(x,y)
        ctx.lineTo(x_new,y)
        ctx.stroke()

        # joint
        draw_joint(x,y,jt)

        # frame
        draw_frame(x,y,frame_color)

        x = x_new

    # workspace
    radius = LINK_LENGTH * len(joint_types)

    ctx.strokeStyle = "gray"
    ctx.setLineDash([5,5])

    ctx.beginPath()
    ctx.arc(100,200,radius,0,math.pi*2)
    ctx.stroke()

    ctx.setLineDash([])


def draw_joint(x,y,jt):

    ctx.strokeStyle = "black"

    if jt == "R":

        ctx.beginPath()
        ctx.arc(x,y,8,0,math.pi*2)
        ctx.stroke()

    elif jt == "P":

        ctx.strokeRect(x-8,y-8,16,16)

    elif jt == "S":

        ctx.beginPath()
        ctx.arc(x,y,8,0,math.pi*2)
        ctx.fill()

    elif jt == "U":

        ctx.beginPath()
        ctx.moveTo(x-10,y)
        ctx.lineTo(x+10,y)
        ctx.moveTo(x,y-10)
        ctx.lineTo(x,y+10)
        ctx.stroke()

    elif jt == "C":

        ctx.strokeRect(x-8,y-8,16,16)
        ctx.beginPath()
        ctx.arc(x,y,5,0,math.pi*2)
        ctx.stroke()


def draw_frame(x,y,color):

    ctx.strokeStyle = color

    ctx.beginPath()

    ctx.moveTo(x,y)
    ctx.lineTo(x+20,y)

    ctx.moveTo(x,y)
    ctx.lineTo(x,y-20)

    ctx.stroke()


def analyze():

    N = int(document.getElementById("links").value)
    J = int(document.getElementById("joints").value)
    L = int(document.getElementById("loops").value)

    system = document.getElementById("system").value

    m = RIGID_BODY_DOF[system]

    f_sum = sum(JOINT_DOF[j] for j in joint_types)

    constraint_sum = sum(JOINT_CONSTRAINTS[j] for j in joint_types)

    M = m*(N-1-J) + f_sum - m*L

    output = document.getElementById("output")

    output.innerText = f"""

GRÜBLER–KUTZBACH ANALYSIS

System: {system}

Links: {N}
Joints: {J}
Loops: {L}

Joint DOF Sum: {f_sum}

Constraints: {constraint_sum}

Mobility Equation:

M = m(N−1−J) + Σf − mL

M = {m}({N}-1-{J}) + {f_sum} − {m}({L})

Mobility = {M}

"""
