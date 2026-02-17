const JOINT_DOF = {
    R:1,
    P:1,
    H:1,
    C:2,
    U:2,
    S:3
}

const SYSTEM_DOF = {
    Planar:3,
    Spatial:6
}


// ==============================
// Create Joint Dropdowns
// ==============================
function createJoints(){

    const container =
        document.getElementById("joint-container")

    container.innerHTML = ""

    const J =
        parseInt(document.getElementById("joints").value)

    for(let i=0;i<J;i++){

        const label =
            document.createElement("label")

        label.innerText = `Joint ${i+1}`

        const select =
            document.createElement("select")

        select.id = `joint${i}`

        select.innerHTML = `
            <option value="R">Revolute</option>
            <option value="P">Prismatic</option>
            <option value="H">Helical</option>
            <option value="C">Cylindrical</option>
            <option value="U">Universal</option>
            <option value="S">Spherical</option>
        `

        container.appendChild(label)
        container.appendChild(select)

    }

}


// ==============================
// Analyze Mobility
// ==============================
function analyze(){

    const N =
        parseInt(document.getElementById("links").value)

    const J =
        parseInt(document.getElementById("joints").value)

    const L =
        parseInt(document.getElementById("loops").value)

    const system =
        document.getElementById("system").value

    const m = SYSTEM_DOF[system]

    let f_sum = 0

    for(let i=0;i<J;i++){

        const joint =
            document.getElementById(`joint${i}`)

        if(!joint){
            alert("Click 'Create Joints' first")
            return
        }

        f_sum += JOINT_DOF[joint.value]

    }

    const mobility =
        m*(N-1-J) + f_sum - m*L

    const constraints =
        m*J - f_sum

    document.getElementById("output").innerText =

`System: ${system}

Mobility (DOF): ${mobility}

Constraints: ${constraints}

Formula:
M = m(N − 1 − J) + Σf − mL

Substitution:
M = ${m}(${N}-1-${J}) + ${f_sum} − ${m}×${L}

Result:
M = ${mobility}`


    drawRobot(N)

}


// ==============================
// Draw Robot
// ==============================
function drawRobot(N){

    const canvas =
        document.getElementById("robotCanvas")

    const ctx =
        canvas.getContext("2d")

    ctx.clearRect(0,0,canvas.width,canvas.height)

    const spacing = canvas.width/(N+1)
    const y = canvas.height/2

    ctx.lineWidth = 3
    ctx.strokeStyle = "cyan"
    ctx.fillStyle = "yellow"

    // Draw links
    ctx.beginPath()

    for(let i=0;i<N;i++){

        const x = spacing*(i+1)

        if(i===0){
            ctx.moveTo(x,y)
        }else{
            ctx.lineTo(x,y)
        }

    }

    ctx.stroke()

    // Draw joints
    for(let i=0;i<N;i++){

        const x = spacing*(i+1)

        ctx.beginPath()
        ctx.arc(x,y,8,0,2*Math.PI)
        ctx.fill()
        ctx.stroke()

    }

}


// ==============================
// Auto Draw On Load
// ==============================
window.onload = function(){

    const N =
        parseInt(document.getElementById("links").value)

    drawRobot(N)

    createJoints()

}
