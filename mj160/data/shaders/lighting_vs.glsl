#version 330

uniform vec2 view_pos;
uniform vec4 view_dir;

in vec2 in_vert;
in vec2 in_uv;

out vec2 vs_pos;
out vec2 vs_uv;

void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
    vs_pos = view_pos + vs_uv.x * view_dir.xy + vs_uv.y * view_dir.zy;
    vs_uv = in_uv;
}
