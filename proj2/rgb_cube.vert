#version 330 core

// vertex shader for RGB cube material

in vec3 vertexPosition;
in vec3 vertexNormal;
in vec2 vertexTexCoord;
in vec4 vertexTangent;

out vec3 position;

uniform mat4 modelView;
uniform mat3 modelViewNormal;
uniform mat4 mvp;

void main() {
    // output position to be used in fragment shader to figure out color
    position = vertexPosition;

    gl_Position = mvp * vec4(vertexPosition, 1.0);
}
