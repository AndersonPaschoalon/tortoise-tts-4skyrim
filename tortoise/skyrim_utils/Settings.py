
class ModelPresets:
    """
    Some COOL presets of settings I found for Tortoise tts experimenting.
    ---- Tortoise Explanation ----

    temperature: Increase this value slightly to make the output more varied and less predictable. This can help add expressiveness.

    length_penalty: Decrease this value to allow for longer, more elaborate expressions which are often characteristic of theatrical performances.

    repetition_penalty: Decrease this value slightly to allow for some repetition which can be a feature of dramatic speech.

    top_p: Increase this value to include more tokens in the cumulative probability mass, which can help in creating more varied and expressive speech.

    cond_free_k: Increase this value to make the speech more influenced by the given conditions, enhancing the dramatic effect.

    diffusion_temperature: Increase this value to add more randomness and variability to the diffusion process, which can enhance expressiveness.

    ---- ChatGPT Tutorial ----
    # Temperature:

    * Purpose: Controls the randomness of predictions by scaling the logits before applying softmax.
    * Effect: A higher temperature results in more random outputs, while a lower temperature results in more deterministic outputs.
    * Typical Range: 0.0 to 1.0 (values >1.0 are less common).

    # Length Penalty:

    * Purpose: Adjusts the preference for longer or shorter sequences during generation.
    * Effect: Higher values penalize longer sequences, promoting shorter outputs. Lower values can encourage longer outputs.
    * Typical Range: >0 (values around 1.0 are common).

    # Repetition Penalty:

    * Purpose: Penalizes repeating the same word/phrase.
    * Effect: Higher values reduce the likelihood of repeating the same tokens, promoting diversity in output.
    * Typical Range: >1 (commonly around 1.2 to 2.0).

    # Top-p (Nucleus Sampling):

    * Purpose: Filters out the least likely tokens, keeping only the top p cumulative probability mass.
    * Effect: Controls the trade-off between diversity and quality of generated text. Lower values result in more conservative, higher-quality text, while higher values allow for more diversity.
    * Typical Range: 0.0 to 1.0 (values like 0.8 or 0.9 are common).

    # Cond Free K (Conditional Free k):

    * Purpose: Specific to models that allow controlling for certain conditions or features.
    * Effect: Adjusts how much the condition influences the generation.
    * Typical Range: Varies based on implementation.

    # Diffusion Temperature:

    * Purpose: Similar to temperature in standard generation but specific to models using a diffusion process for generation.
    * Effect: Controls the randomness of the diffusion process, affecting the smoothness or variability of the generated output.
    * Typical Range: Varies based on implementation.
    """

    @staticmethod
    def default():
        return {
            'temperature': .8,
            'length_penalty': 1.0,
            'repetition_penalty': 2.0,
            'top_p': .8,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def high_expressiveness():
        return {
            'temperature': 1.0,
            'length_penalty': 0.8,
            'repetition_penalty': 1.5,
            'top_p': .8,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def top_p_expressive():
        return {
            'temperature': .8,
            'length_penalty': 1.0,
            'repetition_penalty': 2.0,
            'top_p': 0.95,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def sad():
        """
        sad: Higher repetition penalty for more repetition, lower temperature.
        """
        return {
            'temperature': .7,
            'length_penalty': 1.0,
            'repetition_penalty': 2.5,
            'top_p': .85,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def angry():
        """
        anger: Uses the top_p_expressive() preset with slight modifications.
        """
        return {
            'temperature': .9,
            'length_penalty': 1.0,
            'repetition_penalty': 1.8,
            'top_p': 0.95,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def happy():
        """
        happy: Slightly higher temperature and lower repetition penalty for expressiveness.
        """
        return {
            'temperature': .85,
            'length_penalty': 0.9,
            'repetition_penalty': 1.5,
            'top_p': .9,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def disgust():
        """
        disgust: Similar to neutral but with slight modifications.
        """
        return {
            'temperature': .75,
            'length_penalty': 1.1,
            'repetition_penalty': 2.0,
            'top_p': .85,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def puzzled():
        """
        puzzled: Higher temperature for more variability.
        """
        return {
            'temperature': .9,
            'length_penalty': 1.2,
            'repetition_penalty': 1.5,
            'top_p': .9,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def fear():
        """
        fear: High temperature and condition-free to enhance dramatic effect.
        """
        return {
            'temperature': 1.0,
            'length_penalty': 0.8,
            'repetition_penalty': 1.5,
            'top_p': .8,
            'cond_free_k': 2.5,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def hurt():
        """
        hurt: Similar to sad but slightly different parameters.
        """
        return {
            'temperature': .7,
            'length_penalty': 1.0,
            'repetition_penalty': 2.5,
            'top_p': .85,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def surprise():
        """
        surprise: High temperature for variability and expressiveness.
        """
        return {
            'temperature': .95,
            'length_penalty': 0.9,
            'repetition_penalty': 1.5,
            'top_p': .9,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def sing():
        """
        sing: Higher temperature and lower length penalty for more fluidity.
        """
        return {
            'temperature': 1.0,
            'length_penalty': 0.8,
            'repetition_penalty': 1.5,
            'top_p': .95,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def confident():
        """
        confident: Balanced parameters for a confident tone.
        """
        return {
            'temperature': .85,
            'length_penalty': 1.0,
            'repetition_penalty': 1.5,
            'top_p': .9,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def curious():
        """
        curious: Higher temperature and length penalty for variability.
        """
        return {
            'temperature': .9,
            'length_penalty': 1.1,
            'repetition_penalty': 1.5,
            'top_p': .9,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def frustrated():
        """
        frustrated: Balanced but with higher repetition penalty.
        """
        return {
            'temperature': .9,
            'length_penalty': 1.0,
            'repetition_penalty': 2.0,
            'top_p': .9,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def amused():
        """
        amused: Similar to happy but slightly different parameters.
        """
        return {
            'temperature': .9,
            'length_penalty': 1.0,
            'repetition_penalty': 1.5,
            'top_p': .9,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0
        }

    @staticmethod
    def get_preset(emotion: str):
        presets = {
            'neutral': ModelPresets.default(),
            'anger': ModelPresets.angry(),
            'happy': ModelPresets.happy(),
            'disgust': ModelPresets.disgust(),
            'puzzled': ModelPresets.puzzled(),
            'sad': ModelPresets.sad(),
            'fear': ModelPresets.fear(),
            'hurt': ModelPresets.hurt(),
            'surprise': ModelPresets.surprise(),
            'sing': ModelPresets.sing(),
            'confident': ModelPresets.confident(),
            'curious': ModelPresets.curious(),
            'frustrated': ModelPresets.frustrated(),
            'amused': ModelPresets.amused()
        }

        return presets.get(emotion, ModelPresets.default())()


class TortoiseApiSettings:

    @staticmethod
    def default():
        return {
            "use_deepspeed": True,
            "kv_cache": True,
            "half": True,
            "produce_debug_state": False,
            "seed": None,
            "cvvp_amount": 0,
            'preset': 'slow',
            'default_candidates': 4,
        }



