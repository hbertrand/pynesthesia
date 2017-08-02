var width = 1000;
var height = width * (window.innerHeight / window.innerWidth);

var offset_x = 50;
var offset_y = 50;

var size_x = 6;
var size_y = 6;

var power = 6;

function __hilbert(x, y, xi, xj, yi, yj, order) {
    if  (order <= 0) {
        return [new THREE.Vector3((x + (xi + yi) / 2) * size_x + offset_x, (y + (xj + yj) / 2) * size_y + offset_y, 10)];
    } else {
        var p1 = __hilbert(x, y, yi / 2, yj / 2, xi / 2, xj / 2, order - 1);
        var p2 = __hilbert(x + xi / 2, y + xj / 2, xi / 2, xj / 2, yi / 2, yj / 2, order - 1);
        var p3 = __hilbert(x + xi / 2 + yi / 2, y + xj / 2 + yj / 2, xi / 2, xj / 2, yi / 2, yj / 2, order - 1);
        var p4 = __hilbert(x + xi / 2 + yi, y + xj / 2 + yj, -yi / 2, -yj / 2, -xi / 2, -xj / 2, order - 1);

        return p1.concat(p2, p3, p4);
    }
}

function hilbert_curve_2d(order) {
    return __hilbert(0, 0, 0, 2 ** order, 2 ** order, 0, order);
}

var scene = new THREE.Scene();
var camera = new THREE.OrthographicCamera( 0, width, height, 0, 1, 1000 );
camera.position.set(0, 0, 100);
camera.lookAt(new THREE.Vector3(0, 0, 0));

var renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

// grid
var material = new THREE.LineBasicMaterial({ color: 0xffffff });
var geometry = new THREE.Geometry();
geometry.vertices.push(new THREE.Vector3(offset_x, offset_y, 80));
geometry.vertices.push(new THREE.Vector3(offset_x, offset_y + size_y * (2 ** power), 80));
geometry.vertices.push(new THREE.Vector3(offset_x + size_x * (2 ** power), offset_y + size_y * (2 ** power), 80));
geometry.vertices.push(new THREE.Vector3(offset_x + size_x * (2 ** power), offset_y, 80));
geometry.vertices.push(new THREE.Vector3(offset_x, offset_y, 80));
var line = new THREE.Line(geometry, material);
scene.add(line);

// Hilbert Curve
var material = new THREE.LineBasicMaterial({ color: 0xff0000 });
var geometry = new THREE.Geometry();
geometry.vertices = hilbert_curve_2d(power);
var line = new THREE.Line(geometry, material);
scene.add(line);

var geometry = new THREE.PlaneGeometry( size_x, size_y, 50 );
var material = new THREE.MeshBasicMaterial( {color: 0xffff00, side: THREE.DoubleSide} );
var plane = new THREE.Mesh( geometry, material );
plane.translateX( offset_x + size_x / 2 );
plane.translateY( offset_y + size_y / 2 );
console.log(plane.position)
scene.add( plane );

renderer.render(scene, camera);