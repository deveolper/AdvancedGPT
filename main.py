"""
TODO:

1. Finish the existing classes
    1. See code
2. Remove sources after generation
    1. Maybe replace with [google information](https://google.com/source) to make sure the model can access the data and the name?
3. Implement the lyrics engine
    1. Check multiple lyrics at once for performance
4.  Support image generation
    1. Somehow get a prompt from the language model
    2. Ask the model what model to use
    3. Generate using known code
5.  Support image to text
    [img2text](https://huggingface.co/tasks/image-to-text)
6.  Support image editing
    [img2img](https://huggingface.co/docs/diffusers/using-diffusers/img2img)
    [inpaint](https://huggingface.co/docs/diffusers/using-diffusers/inpaint)
    [depth2img](https://huggingface.co/docs/diffusers/using-diffusers/depth2img)
    [sdxlInpaint](https://huggingface.co/docs/diffusers/using-diffusers/sdxl#inpainting)

    ```py
    inpaintPipe = AutoPipelineForInpainting(generatePipe)
    pipe(
        prompt=positivePrompt,
        image=initialImage,
        mask_image=maskImage
    ).images[0].save("somewhere.png")
    ```
7. Context sliding
8. Interactive model
    1. Ask model what kind of action would be needed, optionally jump to step 4
    2. Perform the action
    3. Go back to step 1
    4. Generate response
9. Add markdown
10. Postprocessing like a sanity check or something, regenerate response when the output is believed to be garbage
11. Performance improvements are going to be very, very needed
    1. Fewer prompts
        1. Ask model which engines are needed (all at once)
        2. Check multiple notes at once, many notes can fit in a single prompt
        3. Put stuff in SQL-database to allow query powered access
    2. Use less capable model whenever good enough
12. Change temperature when needed. Increase when the model is not giving the desired output
13. Find more prompt templates
"""
# Internal
from AdvancedGPT import AdvancedGPT

# External
import ctransformers


SYSTEM_MSG = None


def main():
    model = ctransformers.AutoModelForCausalLM.from_pretrained(
        "language_models",
        model_type="llama",
        model_file="llama-2-7b-chat.Q4_0.gguf",
        config=ctransformers.AutoConfig(
            ctransformers.Config(
                stream=True,
                temperature=0.9,
                max_new_tokens=32768,
                threads=16,
                context_length=32768,
                # last_n_tokens=32768
            )
        ),
        local_files_only=True
    )

    gpt = AdvancedGPT(model)

    history = ""

    while True:
        prompt = input("User: ")
        
        history = gpt.addInstruction(history, prompt, SYSTEM_MSG)

        print("GPT:", end="")

        for token in gpt.ask(history):
            print(token, end="", flush=True)
            history += token


if __name__ == "__main__":
    main()
