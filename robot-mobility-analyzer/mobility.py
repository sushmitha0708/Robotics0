from pyscript import document
import math

# Joint DOF table
JOINT_DOF = {
    "R": 1,
    "P": 1,
    "H": 1,
    "C": 2,
    "U": 2,
    "S": 3
}

SYSTEM_DOF = {
    "Planar": 3,
    "Spatial": 6
}

joint_types = []

def create_joints():

    container = document.getElementById("joint-container")
    container.innerHTML = ""

    J = int(document.getElementById("joints").value)

    global joint_types
    joint_types = []

    for i in range(J):

        select_html = f"""
        <label>Joint {i+1}</label>
        <select id="joint{i}">
            <option value="R">Revolute</option>
            <option value="P">Prismatic</option>
            <option value="H">Helical</option>
            <option value="C">Cylindrical</option>
            <option value="U">Universal</option>
            <option value="S">Spherical</option>
        </select>
        """

        container.innerHTML += select_html


def analyze():

    N = int(document.getElementById("links").value)
    J = int(document.getElementById("joints").value)
    L = int(document.getElementById("loops").value)

    system = document.getElementById("system").value
    m = SYSTEM_DOF[system]

    f_sum = 0

    for i in range(J):

        joint = document.getElementById(f"joint{i}").value
        f_sum += JOINT_DOF[joint]

    # Kutzbach criterion with loop correction
    mobility = m*(N - 1 - J) + f_sum - m*L

    constraints = m*J - f_sum

    output = f"""
SYSTEM: {system}

Mobility (DOF): {mobility}

Constraints: {constraints}

Formula:
M = m(N − 1 − J) + Σf − mL

Substitution:
M = {m}({N}-1-{J}) + {f_sum} − {m}×{L}

Result:
M = {mobility}
"""

    document.getElementById("output").innerText = output

    draw_robot(N)


def draw_robot(N):

    canvas = document.getElementById("robotCanvas")
    ctx = canvas.getContext("2d")

    ctx.clearRect(0,0,700,400)

    x = 50
    y = 200

    spacing = 100

    ctx.beginPath()

    for i in range(N):

        ctx.arc(x+i*spacing, y, 10, 0, 2*math.pi)
        ctx.fill()

        if i > 0:
            ctx.moveTo(x+(i-1)*spacing, y)
            ctx.lineTo(x+i*spacing, y)

    ctx.stroke()
