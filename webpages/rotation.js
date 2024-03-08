function rotateX(angle){
    const matrix =math.matrix([
        [1, 0,0],
        [0, math.cos(angle),-math.sin(angle)],
        [0, math.sin(angle),math.cos(angle)],
        ]);
    return matrix
};

function rotateY(angle){
    const matrix =math.matrix([
        [math.cos(angle), 0,math.sin(angle)],
        [0, 1,0],
        [-math.sin(angle), 0,math.cos(angle)],
        ]);
    return matrix
    
};
function rotateZ(angle){
    const matrix =math.matrix([
        [math.cos(angle),-math.sin(angle),0],
        [math.sin(angle),math.cos(angle),0 ],
        [0,0,1 ],
        ]);
    return matrix
    
};