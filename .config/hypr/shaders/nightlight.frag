precision mediump float;
varying vec2 v_texcoord;
uniform sampler2D tex;

void main() {
    vec4 pixColor = texture2D(tex, v_texcoord);
    // Gentle warm temperature (3800K equivalent, reduces eye strain)
    pixColor.b *= 0.75;
    pixColor.g *= 0.96;
    gl_FragColor = pixColor;
}
