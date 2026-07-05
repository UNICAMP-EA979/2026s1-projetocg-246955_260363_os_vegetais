#ifndef LIBRARY_SPECULAR

#define PI 3.14159265359

//Calcula a refletância especular da superfície utilizando o modelo de Blinn-Phong
vec3 specularReflectance(vec3 fresnel, vec3 normal, vec3 halfAngle, vec3 viewDirection, vec3 lightDirection, float roughness)
{
    float smoothness = 1 - roughness;
    float alpha = pow(8192, smoothness);

    float normalHalf = max(dot(halfAngle, normal), 0);
    float normalView = max(dot(normal, viewDirection), 0.0001); // para evitar divisão por 0
    float lightNormal = max(dot(normal, lightDirection), 0.0001);

    return (fresnel * (alpha + 2) / (8 * PI) * pow(normalHalf, alpha)) / (normalView * lightNormal);
}

#define LIBRARY_SPECULAR
#endif