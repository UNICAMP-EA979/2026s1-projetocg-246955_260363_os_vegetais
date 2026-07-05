#ifndef LIBRARY_DIFUSE

#define PI 3.14159265359

//Calcula a refletância difusa da superfície utilizando o modelo de Lambert
vec3 diffuseReflectance(vec3 fresnel, vec3 baseColor, float metallic)
{
    vec3 pss = mix(baseColor, vec3(0.0), metallic);
    return (1.0 - fresnel) * pss / PI;
}

#define LIBRARY_DIFUSE
#endif