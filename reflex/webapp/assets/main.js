import * as THREE from "https://cdnjs.cloudflare.com/ajax/libs/three.js/0.161.0/three.module.js";

/* <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/0.161.0/three.module.js" integrity="sha512-PyU89+FbuSQctRii6eiPRVTKL+A+Tv1Vn4D7khS53Rksv48PB7JBZxhG8gnZBG7QjXpD9xWfEiDYpZIlq8cgfA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script> */
const renderer = new THREE.WebGLRenderer();
renderer.setSize( 500, 500 );

const container = document.getElementById('canvas_id_123');
console.log(container, document);
// document.body.appendChild(container)
container.appendChild( renderer.domElement );

const camera = new THREE.PerspectiveCamera( 45, 1, 1, 500 );
camera.position.set( 0, 0, 100 );
camera.lookAt( 0, 0, 0 );

const scene = new THREE.Scene();

// Assuming you have two arrays of spatial positions: point1Positions and point2Positions

// Create two spheres to represent the points
const point1 = new THREE.Mesh(new THREE.SphereGeometry(0.7), new THREE.MeshBasicMaterial({ color: 'purple' }));
const point2 = new THREE.Mesh(new THREE.SphereGeometry(0.7), new THREE.MeshBasicMaterial({ color: 'purple' })); 
const point3 = new THREE.Mesh(new THREE.SphereGeometry(0.7), new THREE.MeshBasicMaterial({ color: 'purple' })); 

// Create a line to connect the points
const lineGeometry = new THREE.BufferGeometry();
const lineMaterial = new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 1 });
const line = new THREE.Line(lineGeometry, lineMaterial);

const lineGeometry2 = new THREE.BufferGeometry();
const lineMaterial2 = new THREE.LineBasicMaterial({ color: 0xffffff });
const line2 = new THREE.Line(lineGeometry2, lineMaterial2);

let count = 0, fx = 0;
let point1Positions = [], point2Positions = [], point3Positions = [];
const point3pt = {
    x: 0,
    y: 0,
    z: 0
}
while (count < 10) {
    const obj1 = {
        x: count,
        y: count,
        z: count
    }
    point1Positions.push(obj1);
    const obj2 = {
        x: count + 2,
        y: count+15,
        z: count
    }
    point2Positions.push(obj2);
    point3Positions.push(point3pt);
    count += 1;
}
// console.log(point1Positions, point2Positions);
// Add points and line to the scene
scene.add(point1);
scene.add(point2);
scene.add(point3);
scene.add(line);
scene.add(line2);

// Function to update the positions of points and the line
function updatePointsAndLine(index) {
    // Get the spatial positions from the arrays
    const point1Position = point1Positions[index];
    const point2Position = point2Positions[index];
    const point3Position = point3Positions[index];
    // console.log(point1Position, point2Position, point3Position);
    // Update the positions of the points
    point1.position.set(point1Position.x, point1Position.y, point1Position.z);
    point2.position.set(point2Position.x, point2Position.y, point2Position.z);

    // Update the line geometry
    const linePositions = new Float32Array([
        point1Position.x, point1Position.y, point1Position.z,
        point2Position.x, point2Position.y, point2Position.z,
    ]);

    const line2Positions = new Float32Array([
        point1Position.x, point1Position.y, point1Position.z,
        point3Position.x, point3Position.y, point3Position.z,
    ]);

    line2.geometry.setAttribute('position', new THREE.BufferAttribute(line2Positions, 3));
    line.geometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));

    // Additional logic for more complex scenarios
}

// Animation loop
function animate() {
    requestAnimationFrame(animate);

    // Calculate the index based on time or other factors
    const index = Math.floor(Date.now() / 1000) % point1Positions.length;

    // Call the update function
    updatePointsAndLine(index);

    // Render the scene
    renderer.render(scene, camera);
}

// Start the animation loop
animate();

// //create a blue LineBasicMaterial
// const material = new THREE.LineBasicMaterial( { color: 0x0000ff } );

// const points = [];
// points.push( new THREE.Vector3( - 10, 0, 0 ) );
// points.push( new THREE.Vector3( 0, 10, 0 ) );
// points.push( new THREE.Vector3( 10, 0, 0 ) );

// // const geometry = new THREE.BoxGeometry( 1, 1, 1 );
// // const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
// // const cube = new THREE.Mesh( geometry, material );
// // scene.add( cube );

// // camera.position.z = 5;




// // renderer.render( scene, camera );

// const ax = 1, ay = -1
// var geometry = new THREE.BufferGeometry().setFromPoints( points );
// var line = new THREE.Line( geometry, material );
// scene.add( line );

// function animate() {
//     requestAnimationFrame( animate );
//     points[0].x += ax;
//     points[1].y += ay;
//     geometry = new THREE.BufferGeometry().setFromPoints( points );
//     line = new THREE.Line( geometry, material );
//     console.log(points);
// 	renderer.render( scene, camera );
// }
// animate();