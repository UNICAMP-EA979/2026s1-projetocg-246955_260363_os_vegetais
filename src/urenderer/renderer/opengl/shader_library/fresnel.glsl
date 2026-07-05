#ifndef LIBRARY_FRESNEL

/// Calcula a refletância de Fresnel
vec3 fresnelReflectance(vec3 baseColor, float metallic, vec3 halfAngle, vec3 lightDirection)
{
    vec3 F0 = mix(vec3(0.04), baseColor, metallic);

    float lightHalf = max(dot(halfAngle, lightDirection), 0.0);
    return F0 + (1.0 - F0) * pow(1.0 - lightHalf, 5.0);
}

#define LIBRARY_FRESNEL
#endif