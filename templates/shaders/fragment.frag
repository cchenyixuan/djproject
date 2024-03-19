#version 300 es
precision highp float;
in vec3 f_color;  // (x, y, z)
out vec4 FragColor;

uniform float time;
uniform int scene_type;

uniform vec3 lineColor;      // uniform variable for line color
uniform vec3 triangleColor;  // uniform variable for triangle color

void main(){
    if(scene_type==0){
        FragColor = vec4(abs(f_color)*22.5, 1.0);
    }
    else if(scene_type==1){
        // Render vertex points as orange
        FragColor = vec4(1.0, 0.5, 0.0, 1.0);
    }
    else{
        FragColor = vec4(triangleColor, 0.6);  // Use the triangle color uniform
    }

}