#version 430

const int MAX_LIGHTS = 32;

readonly buffer lighting_data {
    int light_count;
    vec4 lights[];
};

uniform sampler2D albedo;

in vec2 vs_pos;
in vec2 vs_uv;

out vec4 fs_colour;

void main() {
    vec4 light = vec4(0.0);
    for (int i = 0; i < MAX_LIGHTS; i++){
        if (i >= light_count) break;
        int idx = i * 2;
        vec4 light_colour = lights[idx];
        vec4 light_data = lights[idx + 1];
        vec2 diff = vs_pos - light_data.xy;

        float strength = dot(diff, diff);

        light += light_data.z * light_colour / dot(diff, diff);
    }

    fs_colour = vec4(texture(albedo, vs_uv), 1.0);
}
