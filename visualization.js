var gl;
function initWebGL (canvas) {
	var element = document.createElement('h1');
	element.innerHTML = 'no canvas support!';
	try {
		gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
	} catch (e) {
		document.body.appendChild(element);
		return null;
	}
	if (!gl) {
		document.body.appendChild(element);
	}
	return gl;
}
function setupGraphics() {
	var canvas = document.querySelector('#graphCanvas');	
	gl = initWebGL(canvas);
	if (gl) {
		gl.clearColor(0.0, 0.0, 0.0, 1.0);
    	gl.enable(gl.DEPTH_TEST);                               
    	gl.depthFunc(gl.LEQUAL);                                
    	gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT); 
	}
}
window.onload = setupGraphics;