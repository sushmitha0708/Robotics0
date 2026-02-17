console.log("script loaded")

function createJoints(){

    const container =
        document.getElementById("joint-container")

    container.innerHTML = ""

    const J =
        parseInt(document.getElementById("joints").value)

    for(let i=0;i<J;i++){

        container.innerHTML +=
        `<label>Joint ${i+1}</label>
        <select id="joint${i}">
        <option value="R">R</option>
        <option value="P">P</option>
        </select>`
    }

}


function analyze(){

    const N =
        parseInt(document.getElementById("links").value)

    drawRobot(N)

}


function drawRobot(N){

    console.log("drawing robot with N =", N)

    const canvas =
        document.getElementById("robotCanvas")

    if(!canvas){

        console.log("canvas not found")
        return

    }

    const ctx =
        canvas.getContext("2d")

    ctx.clearRect(0,0,canvas.width,canvas.height)

    const spacing = canvas.width/(N+1)
    const y = canvas.height/2

    ctx.strokeStyle = "cyan"
    ctx.fillStyle = "yellow"
    ctx.lineWidth = 3

    // draw links
    ctx.beginPath()

    for(let i=0;i<N;i++){

        let x = spacing*(i+1)

        if(i==0)
            ctx.moveTo(x,y)
        else
            ctx.lineTo(x,y)

    }

    ctx.stroke()

    // draw joints
    for(let i=0;i<N;i++){

        let x = spacing*(i+1)

        ctx.beginPath()
        ctx.arc(x,y,10,0,Math.PI*2)
        ctx.fill()
        ctx.stroke()

    }

}


// run after page loads
window.addEventListener("load", function(){

    console.log("page loaded")

    createJoints()

    const N =
        parseInt(document.getElementById("links").value)

    drawRobot(N)

})
