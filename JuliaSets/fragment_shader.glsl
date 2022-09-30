#version 430

out vec4 fragColor;

uniform vec2 resolution;
uniform float time;
uniform float pi;
uniform float cR;
uniform float cI;
uniform float zoom;
uniform float offsetX;
uniform float offsetY;


const float MAX = 100.0;


vec2 eul_to_euc(vec2 eul){
    return vec2(cos(eul.y)*eul.x, sin(eul.y)*eul.x);
}

vec2 euc_to_eul(vec2 euc){
    float angle = 2.0*atan(euc.y/(euc.x + length(euc)));
    while(angle > 2.0*pi){
        angle -= 2.0*pi;
    }
    return vec2(length(euc), angle);
}

vec2 conjugate_euc(vec2 z){
    return vec2(z.x, -z.y);
}

vec2 conjugate_eul(vec2 z){
    float angle = z.y + pi;
    if(angle > 2.0*pi){
        angle -= 2.0*pi;
    }
    return vec2(z.x, angle);
}

vec2 mult_eul(vec2 z1, vec2 z2){
    return vec2(z1.x*z2.x, z1.y + z2.y);
}

vec2 mult_euc(vec2 z1, vec2 z2){
    return vec2(z1.x*z2.x - z1.y*z2.y, z1.x*z2.y + z1.y*z2.x);
}

vec2 pow_eul(vec2 z, float expon){
    return vec2(pow(z.x, expon), z.y*expon);
}

vec2 pow_euc(vec2 z, float expon){
    return eul_to_euc(pow_eul(euc_to_eul(z), expon));
}






float mandel(vec2 uv, float t){
    vec2 offset = vec2(offsetX, offsetY);
    vec2 z = zoom*(uv) + offset;
    float iter = 0.0;
    vec2 c = vec2(cR, cI);
    float R = 2.0;

    for (float i; i<MAX;i++){
        z = pow_euc(z, 3.0) + c;
        
        
        if (dot(z, z) > R*R) return iter/MAX;
        iter++;
    }
    return dot(z,z)/(R*R);
}


void main(){
    vec2 uv = (gl_FragCoord.xy - 0.5 * resolution.xy)/(resolution.y*2);
    vec3 col = vec3(0.0);
    float m = mandel(uv, time);
    

    col += m;
    col = pow(col, vec3(0.5));
    col *= vec3(0.97, 0.48, 0.25);
    if (length(uv) < 0.001){
        col = vec3(1.0);
    }

    fragColor = vec4(col, 1.0);
}