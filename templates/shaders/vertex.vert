#version 300 es
precision highp float;
layout(location=0) in vec3 vertex_position;
layout(location=1) in vec3 vertex_color;

uniform mat4 view;
uniform mat4 projection;

uniform vec3 lineColor;      // uniform variable for line color
uniform vec3 triangleColor;  // uniform variable for triangle color

out vec3 f_color;
void main(){
    gl_Position = projection * view * vec4(vertex_position, 1.0);
    f_color = vertex_color;
    gl_PointSize = 3.0;
}