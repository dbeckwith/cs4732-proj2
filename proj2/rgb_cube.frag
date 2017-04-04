#version 330 core

// fragment shader for RGB cube material

in vec3 position;

out vec4 fragColor;

void main() {
    // set color to space position, mapped from [-1, 1] to [0, 1]
    fragColor = vec4((position + 1.0) / 2.0, 1.0);
}
