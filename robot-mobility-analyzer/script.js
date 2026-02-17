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


function createJoints(){

    const container =
        document.getElementById("joint-container")

    container.innerHTML=""

    const J =
        parseInt(document.getElementById("joints").value)

    for(let i=0;i<J;i++){

        container.innerHTML +=

        `<label>Joint ${i+1}</label>
        <select id="joint${i}">
        <option value="R">Revolute</option>
        <option value="P">Prismatic</option>
        <option value="H">Helical</option>
        <option value="C">Cylindrical</option>
        <option value="U">Universal</option>
        <option value="S">Spherical</option>
        </select>`
    }

}


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
            document.getElementById(`joint${i}`).value

        f_sum += JOINT_DOF[joint]

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


function drawRobot(N){

    const canvas =
        document.getElementById("robotCanvas")

    const ctx =
        canvas.getContext("2d")

    ctx.clearRect(0,0,700,400)

    const spacing = 100
    const y = 200

    ctx.beginPath()

    for(let i=0;i<N;i++){

        const x = 50 + i*spacing

        ctx.arc(x,y,10,0,2*Math.PI)

        if(i>0){

            ctx.moveTo(x-spacing,y)
            ctx.lineTo(x,y)

        }

    }

    ctx.stroke()

}
