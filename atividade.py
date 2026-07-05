from collections import deque

import numpy as np
import urenderer
from OpenGL import GL
from urenderer.node import Node
from urenderer.renderer.opengl import Material, Texture


def update_cube(node: Node, deltaTime: float, time_since_start: float) -> None:

    # Posição = dv/dt -> posição_t = posição_{t-1}+DeltaT*v
    center: np.array = node.center
    position = node.translation

    r = position-center

    if not hasattr(update_cube, 'orbit_axis'): # variável estática. 
        right = np.array([1.0, 0.0, 0.0])
        axis = np.cross(r, right)
        axis_norm = np.linalg.norm(axis)
        axis = axis / axis_norm
        update_cube.orbit_axis = axis # eixo árbitrário perpendicular ao plano de órbita (que contém r)

    omega = update_cube.orbit_axis * node.angular_velocity
    
    # velocidade tangencial, omega x r
    v = np.cross(omega, r)

    node.translation += deltaTime*v

    # Rotação = f(tempo)
    time_since_start /= 10
    t = time_since_start - int(time_since_start)
    node.rotation[0] = 0
    node.rotation[1] = -360*node.angular_velocity*t
    node.rotation[2] = 0


# Podemos dar um nome a cena
NOME_DA_CENA = "minha_cena"

if __name__ == "__main__":
    urenderer.utils.clear_workdir(NOME_DA_CENA)
    renderer = urenderer.renderer.OpenGLRenderer(1920, 1080)
    renderer.background_color = np.array([0, 0, 0, 1], np.float32)
    runtime = urenderer.application.Runtime(
        renderer, name=NOME_DA_CENA)

    # Configuramos a luz ambiente da cena
    renderer.ambient_color = np.array([0.3, 0.3, 0.3], dtype=np.float32)

    # Carregamos o shader e texturas
    shader = urenderer.renderer.Shader(
        "assets/vertex.vs", "assets/05-fragment.fs")
    
    whiteTextureR = Texture(255*np.ones((1, 1), np.uint8), GL.GL_RED, GL.GL_R8)
    blackTextureR = Texture(np.zeros((1, 1), np.uint8), GL.GL_RED, GL.GL_R8)

    whiteTexture = Texture(255*np.ones((1, 1, 3), np.uint8),
                           GL.GL_RGB, GL.GL_RGB)
    blackTexture = Texture(np.zeros((1, 1, 3), np.uint8),
                           GL.GL_RGB, GL.GL_RGB)
    
    rockBasecolor = Texture.load_file("assets/Rock035_1K-JPG/Rock035_1K-JPG_Color.jpg",
                                      srgb=True, drop_alpha=True)
    rockRoughness = Texture.load_file("assets/Rock035_1K-JPG/Rock035_1K-JPG_Roughness.jpg",
                                      drop_alpha=True)

    materialSphere = Material(shader)
    materialSphere.set_texture(0, "baseColorTexture", rockBasecolor)
    materialSphere.set_texture(1, "metallicTexture", blackTextureR)
    materialSphere.set_texture(2, "roughnessTexture", rockRoughness)
    materialSphere.set_uniform("emissionColor", np.array([0.0, 0.0, 0.0], dtype=np.float32))

    materialCube = Material(shader)
    materialCube.set_texture(0, "baseColorTexture", whiteTexture)
    materialCube.set_texture(1, "metallicTexture", blackTextureR)
    materialCube.set_texture(2, "roughnessTexture", whiteTextureR)
    materialCube.set_uniform("emissionColor", np.array([0.5, 0.5, 0.5], dtype=np.float32))
    
    '''
    metalBaseColor = Texture.load_file("materials/Metal048A_1K-JPG/Metal048A_1K-JPG_Color.jpg",
                                       srgb=True, drop_alpha=True)
    metalMetallic = Texture.load_file(
        "materials/Metal048A_1K-JPG/Metal048A_1K-JPG_Metalness.jpg", drop_alpha=True)
    metalRoughness = Texture.load_file(
        "materials/Metal048A_1K-JPG/Metal048A_1K-JPG_Roughness.jpg", drop_alpha=True)

    materialMetal = urenderer.renderer.opengl.Material(shader)
    materialMetal.set_texture(0, "baseColorTexture", metalBaseColor)
    materialMetal.set_texture(1, "metallicTexture", metalMetallic)
    materialMetal.set_texture(2, "roughnessTexture", metalRoughness)
    '''
    # Carregamos a cena (ou poderia ser criada com primitivas)
    sphere = urenderer.node.Node()
    sphere.translation = np.array([0, 0, -5], np.float64)
    sphere.render_data["mesh"] = urenderer.geometry.mesh.get_mesh_sphere()
    sphere.render_data["material"] = materialSphere
    runtime.scene.add_child(sphere)

    center = sphere.translation

    cube = urenderer.node.Node()
    cube.translation = np.array([1.5, 1.5, -7], np.float64)
    cube.rotation = np.array([0, -30, 0], np.float64)
    cube.render_data["mesh"] = urenderer.geometry.mesh.get_mesh_cube()
    cube.render_data["material"] = materialCube
    cube.center = center
    cube.angular_velocity = 0.5
    cube.callbacks = [update_cube]
    runtime.scene.add_child(cube)

    # Podemos alterar propriedades da câmera
    runtime.camera.vertical_fov = 90.0

    # Adicionamos luzes a cena

    light = urenderer.node.Light(urenderer.node.LightType.POINT)
    light.light_intensity = 5.0
    cube.add_child(light)

    # Renderizamos a cena

    video = True
    if video:
        # Renderização salvando video
        # Podemos ajustar os parâmetros para alterar o tamanho ou frequência de sampling
        runtime.loop(n=None, capture=np.arange(0, 4000, 40, dtype=np.int32))
        urenderer.utils.image_to_video(NOME_DA_CENA, fps=30)
        urenderer.utils.clear_workdir(NOME_DA_CENA, image_only=True)
    else:
        # Renderização salvando frames
        runtime.loop(capture=[1])
