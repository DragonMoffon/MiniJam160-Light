#version 330

uniform vec4 view_area;

in vec2 in_vert;
in vec2 in_uv;

out vec2 vs_pos;
out vec2 vs_uv;

void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
    vs_pos = vec2(view_area.x + in_uv.x * view_area.z, view_area.y + in_uv.y * view_area.w);
    vs_uv = in_uv;
}
