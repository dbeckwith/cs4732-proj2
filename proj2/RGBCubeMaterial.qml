import Qt3D.Core 2.0
import Qt3D.Render 2.0

// material for an RGB cube

Material {
    effect: Effect {
        techniques: [
            Technique {
                filterKeys: [
                    FilterKey {
                        id: forward
                        name: "renderingStyle"
                        value: "forward"
                    }
                ]
                // only works in OpenGL 3.1
                graphicsApiFilter {
                    api: GraphicsApiFilter.OpenGL
                    profile: GraphicsApiFilter.CoreProfile
                    majorVersion: 3
                    minorVersion: 1
                }
                renderPasses: RenderPass {
                    shaderProgram: ShaderProgram {
                        // use custom shaders
                        vertexShaderCode: loadSource("file:proj2/rgb_cube.vert")
                        fragmentShaderCode: loadSource("file:proj2/rgb_cube.frag")
                    }
                }
            }
        ]
    }
}
