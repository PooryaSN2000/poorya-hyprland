#version 300 es
precision mediump float;
in vec2 v_texcoord;
uniform sampler2D tex;
out vec4 fragColor;

void main() {
    vec4 pixColor = texture(tex, v_texcoord);
    // Gentle warm temperature (reduces blue light and eye strain)
    pixColor.b *= 0.75;
    pixColor.g *= 0.96;
    fragColor = pixColor;
}
