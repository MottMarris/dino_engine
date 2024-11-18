import pygame

# import the scene class
from cubeMap import FlattenCubeMap
from scene import Scene

from lightSource import LightSource

from blender import load_obj_file

from BaseModel import DrawModelFromMesh

from shaders import *

from ShadowMapping import *

from sphereModel import Sphere

from skyBox import *

from environmentMapping import *

class ExeterScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        self.light = LightSource(self, position=[3., 13., 12.], Ia=[0.1,0.1,0.1])

        self.shaders='phong'

        # for shadow map rendering
        self.shadows = ShadowMap(light=self.light)
        self.show_shadow_map = ShowTexture(self, self.shadows)

        # draw a skybox for the horizon
        self.skybox = SkyBox(scene=self)

        self.show_light = DrawModelFromMesh(scene=self, M=poseMatrix(position=self.light.position, scale=0.2), mesh=Sphere(material=Material(Ka=[10,10,10])), shader=FlatShader())

        self.environment = EnvironmentMappingTexture(width=400, height=400)

        self.sphere = DrawModelFromMesh(scene=self, M=poseMatrix(), mesh=Sphere(), shader=EnvironmentShader(map=self.environment))


        # Add the two trexs spinning on the roof. Checking animation=True and setting their names to trex means 
        # they'll be animated with the trex animation i.e spinning in a circle around their own axis

        meshes = load_obj_file('models/trex.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=poseMatrix([-8.5,2.5,11.5],0,0.3), position=[-10,0,10], mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='trex', animation=True) for mesh in meshes]
        )

        meshes = load_obj_file('models/trex.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=poseMatrix([-8.5,2.5,-11],0,0.3), position=[-10,0,10], mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='trex', animation=True) for mesh in meshes]
        )

        # Add the static trex on the roof, hence animation is left as the default False.

        meshes = load_obj_file('models/trex.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-8,2.5,-1]), rotationMatrixY(np.pi/2)), scaleMatrix([0.3,0.3,0.3])), position=[-10,0,10], mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='trex') for mesh in meshes]
        )

        # Add Pterodactly circling the scene. Animation is True

        meshes = load_obj_file('models/pterodactyl.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([0,7,-5]), rotationMatrixY(np.pi/2)), scaleMatrix([0.3,0.3,0.3])), position=[-10,0,10], mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='pterodactyl', animation=True) for mesh in meshes]
        )

        # The surface that all the other models are placed on top of

        meshes = load_obj_file('models/surface.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([3,-4,0]),scaleMatrix([0.3,0.3,0.3])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='surface') for mesh in meshes]
        )

        # Add the two triceratops that are headbutting the phoneboxes onto the floor. Rotated to face the negative x direction 

        meshes = load_obj_file('models/tri.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-2,-4,-6]), rotationMatrixY(-np.pi/2)), scaleMatrix([0.6,0.6,0.6])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='tri', animation=True) for mesh in meshes]
        )


        meshes = load_obj_file('models/tri.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-2,-4,6]), rotationMatrixY(-np.pi/2)), scaleMatrix([0.6,0.6,0.6])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='tri', animation=True) for mesh in meshes]
        )

        # Add the two triceratops that are headbutting the phoneboxes onto the floor. Rotated to face the negative z direction

        meshes = load_obj_file('models/tri.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([10,-4,10]), rotationMatrixY(np.pi)), scaleMatrix([0.6,0.6,0.6])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='tri', animation=True) for mesh in meshes]
        )

        meshes = load_obj_file('models/tri.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([10,-4,0]), rotationMatrixY(np.pi)), scaleMatrix([0.6,0.6,0.6])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='tri', animation=True) for mesh in meshes]
        )

        # Add the three apartment buildings. Once the loop hits the windows (identified by material name _Windows), the loop skips it 
        # Then once all the other meshes have been added, the apartmen windows are added but they are given the environment mapping shader so they
        # can reflect the scene

        # The apartments furthest from big ben

        meshes = load_obj_file('models/apartments.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-11,-4,11]),scaleMatrix([0.25,0.25,0.25])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='apartments') for mesh in meshes if mesh.material.name != "Windows_"]
        )

        meshes = load_obj_file('models/apartments.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-11,-4,11]),scaleMatrix([0.25,0.25,0.25])), mesh=mesh, shader=EnvironmentShader(map=self.environment), name='apartmentWindows') for mesh in meshes if mesh.material.name == "Windows_"]
        )

        # The apartments in the middle

        meshes = load_obj_file('models/apartments.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-11,-4,0]),scaleMatrix([0.25,0.25,0.25])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='apartments') for mesh in meshes if mesh.material.name != "Windows_"] 
        )

        meshes = load_obj_file('models/apartments.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-11,-4,0]),scaleMatrix([0.25,0.25,0.25])), mesh=mesh, shader=EnvironmentShader(map=self.environment), name='apartmentWindows') for mesh in meshes if mesh.material.name == "Windows_"]
        )

        # The apartments closest to big ben

        meshes = load_obj_file('models/apartments.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-11,-4,-11]),scaleMatrix([0.25,0.25,0.25])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='apartments') for mesh in meshes if mesh.material.name != "Windows_"]
        )

        meshes = load_obj_file('models/apartments.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-11,-4,-11]),scaleMatrix([0.25,0.25,0.25])), mesh=mesh, shader=EnvironmentShader(map=self.environment), name='apartmentWindows') for mesh in meshes if mesh.material.name == "Windows_"]
        )

        # Add the big ben model

        meshes = load_obj_file('models/bigben.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([3.5,-4,-20]),scaleMatrix([0.15,0.15,0.15])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='bigBen') for mesh in meshes]
        )

        # Add the road on the left of the scene

        meshes = load_obj_file('models/road.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-2,-4,-0.4]),scaleMatrix([0.2,0.2,0.182])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='leftRoad') for mesh in meshes]
        )

        # And the road on the right

        meshes = load_obj_file('models/road.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([8.5,-4,-0.4]),scaleMatrix([0.2,0.2,0.182])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='rightRoad') for mesh in meshes]
        )

        # Add a static phonebox

        meshes = load_obj_file('models/phonebox.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=poseMatrix(position=[-5,-3.7,0], orientation=0,scale=0.2), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='phonebox') for mesh in meshes]
        )

        # Add the two phoneboxes that are headbutted onto the ground labelled phonebox

        meshes = load_obj_file('models/phonebox.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-5,-3.7,6]),scaleMatrix([0.25,0.25,0.25])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='phonebox', animation=True) for mesh in meshes]
        )

        meshes = load_obj_file('models/phonebox.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-5,-3.7,-6]),scaleMatrix([0.25,0.25,0.25])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='phonebox', animation=True) for mesh in meshes]
        )

        # Add the phoneboxes that are headbutted into the sky. The phonebox2 name differetiates these two types and gives them
        # different animation is the animate() function

        meshes = load_obj_file('models/phonebox.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=poseMatrix(position=[10,-3.7,-3], orientation=0,scale=0.2), position=[5,-3.5,0], mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='phonebox2', animation=True) for mesh in meshes]
        )

        meshes = load_obj_file('models/phonebox.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=poseMatrix(position=[10,-3.7,7], orientation=0,scale=0.2), position=[5,-3.5,0], mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='phonebox2', animation=True) for mesh in meshes]
        )

        # Add the thames river

        meshes = load_obj_file('models/thames.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([3,-4.6,1]),scaleMatrix([0.3,0.25,0.1])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='thames') for mesh in meshes]
        )

        # Add the glass buildings on the right of the scene. Here we do the same thing as the apartments where the windows of the buildings
        # are given the environment mapping shader so they reflect the scene

        meshes = load_obj_file('models/multibuilding.obj')
        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([3,-4,0]),scaleMatrix([1,1,1])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='multibuilding') for mesh in meshes if mesh.material.name != "windows"]
        )

        self.add_models_list(
            [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([3,-4,0]),scaleMatrix([1,1,1])), mesh=mesh, shader=EnvironmentShader(map=self.environment), name='multibuildingWindows') for mesh in meshes if mesh.material.name == "windows"]
        )

        # this object allows to visualise the flattened cube

        self.flattened_cube = FlattenCubeMap(scene=self, cube=self.environment)

        self.show_texture = ShowTexture(self, Texture('lena.bmp'))

    def draw_shadow_map(self):
        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for model in self.models:
            model.draw()


    def draw_reflections(self):
        self.skybox.draw()

        for model in self.models:
            model.draw()



    def draw(self, framebuffer=False):
        '''
        Draw all models in the scene
        :return: None
        '''

        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # when using a framebuffer, we do not update the camera to allow for arbitrary viewpoint.
        if not framebuffer:
            self.camera.update()

        # first, we draw the skybox
        self.skybox.draw()

        # render the shadows
        self.shadows.render(self)

        # when rendering the framebuffer we ignore the reflective object
        if not framebuffer:

            self.environment.update(self)

            # if enabled, show flattened cube
            self.flattened_cube.draw()

            # if enabled, show texture
            self.show_texture.draw()

            self.show_shadow_map.draw()

        # then we loop over all models in the list and draw them
        for model in self.models:
            model.draw()


        self.show_light.draw()

        # once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # we draw on a different buffer than the one we display,
        # and flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

    def keyboard(self, event):
        '''
        Process additional keyboard events for this demo.
        '''
        Scene.keyboard(self, event)

        if event.key == pygame.K_c:
            if self.flattened_cube.visible:
                self.flattened_cube.visible = False
            else:
                print('--> showing cube map')
                self.flattened_cube.visible = True

        if event.key == pygame.K_t:
            if self.show_texture.visible:
                self.show_texture.visible = False
            else:
                print('--> showing texture map')
                self.show_texture.visible = True

        if event.key == pygame.K_s:
            if self.show_shadow_map.visible:
                self.show_shadow_map.visible = False
            else:
                print('--> showing shadow map')
                self.show_shadow_map.visible = True

        if event.key == pygame.K_1:
            print('--> using Flat shading')
            self.bunny.use_textures = True
            self.bunny.bind_shader('flat')

        if event.key == pygame.K_2:
            print('--> using Phong shading')
            self.bunny.use_textures = True
            self.bunny.bind_shader('phong')

        elif event.key == pygame.K_4:
            print('--> using original texture')
            self.bunny.shader.mode = 1

        elif event.key == pygame.K_6:
            self.bunny.mesh.material.alpha += 0.1
            print('--> bunny alpha={}'.format(self.bunny.mesh.material.alpha))
            if self.bunny.mesh.material.alpha > 1.0:
                self.bunny.mesh.material.alpha = 0.0

        elif event.key == pygame.K_7:
            print('--> no face culling')
            glDisable(GL_CULL_FACE)

        elif event.key == pygame.K_8:
            print('--> glCullFace(GL_FRONT)')
            glEnable(GL_CULL_FACE)
            glCullFace(GL_FRONT)

        elif event.key == pygame.K_9:
            print('--> glCullFace(GL_BACK)')
            glEnable(GL_CULL_FACE)
            glCullFace(GL_BACK)

        elif event.key == pygame.K_BACKQUOTE:
            if glIsEnabled(GL_DEPTH_TEST):
                print('--> disable GL_DEPTH_TEST')
                glDisable(GL_DEPTH_TEST)
            else:
                print('--> enable GL_DEPTH_TEST')
                glEnable(GL_DEPTH_TEST)


if __name__ == '__main__':
    # initialises the scene object
    scene = ExeterScene()

    # starts drawing the scene
    scene.run()
